"""Core module for solvency package.

This module contains an `Electrolyte` class and an `e_solver` function. 
The `Electrolyte` class represents an electrolyte formulation, including solvents,
salts, and additives, along with their concentrations. The `e_solver` function
takes a bank of candidate electrolytes and a target final formulation, and uses 
linear programming to find a mixture of candidates that matches the target composition.
"""
from typing import Dict, Optional, List
import numpy as np

# Optional dependency; only used when fetching SMILES from PubChem.
try:
    import pubchempy as pcp
except Exception:
    print("Warning: pubchempy not available, PubChem lookups will be disabled.")
    pcp = None

import pulp

# Simple in-memory cache to avoid repeated PubChem lookups.
_SMILES_CACHE: Dict[str, str] = {}

class Electrolyte:
    """Represent an electrolyte / solvent blend.

    Parameters
    - name: user-facing name
    - volume: total volume (uL). Can be None for "formulation only" objects.
    - v: dict of solvent_name -> volume fraction (will be normalized if needed)
    - s: dict of salt_name -> molarity
    - a: dict of additive_name -> molarity
    - local_smiles: optional mapping name->smiles for offline use / tests
    """

    def __init__(
        self,
        name: str,
        volume: Optional[float] = None,
        v: Optional[Dict[str, float]] = None,
        s: Optional[Dict[str, float]] = None,
        a: Optional[Dict[str, float]] = None,
        local_smiles: Optional[Dict[str, str]] = None,
        use_pubchem: bool = False,
    ) -> None:
        v = v or {}
        s = s or {}
        a = a or {}

        if volume is not None:
            if not isinstance(volume, (int, float)) or volume <= 0:
                raise ValueError("volume must be a positive number or None")

        # Normalize solvent fractions if they don't already sum to 1.
        v_sum = sum(v.values())
        if v_sum == 0 and v:
            raise ValueError("Sum of solvent fractions is zero")
        if v_sum != 0:
            self.v = {k: float(val) / v_sum for k, val in v.items()}
        else:
            self.v = {}

        self.name = name
        self.s = {k: float(val) for k, val in s.items()}
        self.a = {k: float(val) for k, val in a.items()}
        self.volume = float(volume) if volume is not None else None

        # Allow tests and offline usage by providing a small
        # local_smiles dict. If not present, optionally use PubChem.
        self._local_smiles = local_smiles or {}
        self._use_pubchem = use_pubchem

        # Store SMILES-mapped dicts for unambiguous identification.
        self.v_smiles = {self.get_smiles(k): frac for k, frac in self.v.items()}
        self.s_smiles = {self.get_smiles(k): conc for k, conc in self.s.items()}
        self.a_smiles = {self.get_smiles(k): conc for k, conc in self.a.items()}

    def get_smiles(self, name: str) -> str:
        """Return a SMILES string for a compound name.

        Uses the local mapping if available; falls back to PubChem only if
        `use_pubchem=True` and the `pubchempy` package is installed.

        CONCEPT: (INFO) Caching external lookups prevents rate-limits and makes
        tests deterministic when a local map is provided.
        """
        if name in self._local_smiles:
            return self._local_smiles[name]

        if name in _SMILES_CACHE:
            return _SMILES_CACHE[name]

        if not self._use_pubchem or pcp is None:
            raise ValueError(
                f"SMILES for '{name}' not provided locally and PubChem disabled"
            )

        # Try three times to fetch from PubChem in case of transient issues.
        for _ in range(3):
            try:
                compounds = pcp.get_compounds(name, "name")
                break
            except Exception:
                continue
        else:
            raise ValueError(f"Failed to fetch SMILES for '{name}' from PubChem")

        if not compounds:
            raise ValueError(f"Compound '{name}' not found in PubChem")
        smiles = compounds[0].isomeric_smiles or compounds[0].canonical_smiles
        _SMILES_CACHE[name] = smiles
        return smiles

    def __repr__(self) -> str:
        return f"Electrolyte(name={self.name!r}, volume={self.volume!r})"

    def combine(self, other: "Electrolyte", new_name: Optional[str] = None) -> "Electrolyte":
        """Return a new Electrolyte representing the mixture of self and other."""

        if not isinstance(other, Electrolyte):
            raise ValueError("Can only combine with another Electrolyte")

        V1 = self.volume if self.volume is not None else 0.0
        V2 = other.volume if other.volume is not None else 0.0
        if (V1 + V2) > 0 and self.volume is not None and other.volume is not None:
            total_V = V1 + V2
        else:
            raise ValueError("Both electrolytes must have defined positive volumes to combine")

        if new_name is None:
            new_name = f"{self.name} + {other.name}"

        # Weighted average of solvent fractions and concentrations.
        new_v = {}
        for k in set(self.v.keys()).union(other.v.keys()):
            v1 = self.v.get(k, 0.0)
            v2 = other.v.get(k, 0.0)
            new_v[k] = (v1 * V1 + v2 * V2) / total_V

        new_s = {}
        for k in set(self.s.keys()).union(other.s.keys()):
            s1 = self.s.get(k, 0.0)
            s2 = other.s.get(k, 0.0)
            new_s[k] = (s1 * V1 + s2 * V2) / total_V

        new_a = {}
        for k in set(self.a.keys()).union(other.a.keys()):
            a1 = self.a.get(k, 0.0)
            a2 = other.a.get(k, 0.0)
            new_a[k] = (a1 * V1 + a2 * V2) / total_V

        # Compose a local_smiles mapping so the new object can be used offline.
        new_local_smiles = {**self._local_smiles, **other._local_smiles}

        return Electrolyte(
            name=new_name,
            volume=total_V,
            v=new_v,
            s=new_s,
            a=new_a,
            local_smiles=new_local_smiles,
            use_pubchem=self._use_pubchem or other._use_pubchem,
        )

    def __add__(self, other: "Electrolyte") -> "Electrolyte":
        """Operator overload that calls `combine` with a default name.
        """
        return self.combine(other)


def e_solver(
    electrolyte_bank: List[Electrolyte],
    final_formulation: Electrolyte,
    big_m: float = 1000.0,
    eps: float = 1e-6,
) -> Optional[Dict[str, float]]:
    """Find a mixture of electrolytes that matches the final formulation.

    Returns solution_dict where solution_dict maps electrolyte name
    -> fraction of final mixture (sums to 1).
    """

    # Filter candidates that don't contain unexpected compounds.
    valid_candidates: List[Electrolyte] = []
    required_components = set()
    required_components.update(final_formulation.v_smiles.keys())
    required_components.update(final_formulation.s_smiles.keys())
    required_components.update(final_formulation.a_smiles.keys())

    # Identify candidates and make sure collectively they cover all required components.
    found = {comp: False for comp in required_components}
    for e in electrolyte_bank:
        # Candidate must not introduce solvents not in target
        if not set(e.v_smiles.keys()).issubset(final_formulation.v_smiles.keys()):
            continue
        # salts/additives must be subset of target salts/additives (treated interchangeably here)
        final_formulation_sa_keys = set(final_formulation.s_smiles.keys()).union(final_formulation.a_smiles.keys())
        if not set(e.s_smiles.keys()).issubset(final_formulation_sa_keys):
            continue
        if not set(e.a_smiles.keys()).issubset(final_formulation_sa_keys):
            continue
        valid_candidates.append(e)
        for comp in found.keys():
            if comp in e.v_smiles or comp in e.s_smiles or comp in e.a_smiles:
                found[comp] = True

    if not all(found.values()):
        missing = [c for c, ok in found.items() if not ok]
        raise ValueError(f"Missing components in bank: {missing}")

    n = len(valid_candidates)
    if n == 0:
        raise ValueError("No valid candidate electrolytes available")

    # Build compound lists
    S_compounds = list({c for e in valid_candidates for c in e.v_smiles.keys()})
    M_compounds = list({c for e in valid_candidates for c in set(e.s_smiles.keys()).union(e.a_smiles.keys())})

    S = np.zeros((len(S_compounds), n)) # volume fractions of each component (row) in each candidate (column)
    M = np.zeros((len(M_compounds), n)) #       molarities of each component (row) in each candidate (column)
    t1 = np.zeros(len(S_compounds))     # Goal volume fractions of each component in final formulation
    t2 = np.zeros(len(M_compounds))     # Goal molarities of each component in final formulation (salts and additives treated interchangeably here)

    for i, comp in enumerate(S_compounds):
        for j, e in enumerate(valid_candidates):
            S[i, j] = e.v_smiles.get(comp, 0.0)
        t1[i] = final_formulation.v_smiles.get(comp, 0.0)

    for i, comp in enumerate(M_compounds):
        for j, e in enumerate(valid_candidates):
            M[i, j] = e.s_smiles.get(comp, 0.0) + e.a_smiles.get(comp, 0.0)
        t2[i] = final_formulation.s_smiles.get(comp, 0.0) + final_formulation.a_smiles.get(comp, 0.0)

    prob = pulp.LpProblem("mixing_problem", pulp.LpMinimize)
    v_vars = [pulp.LpVariable(f"v_{j}", lowBound=0, upBound=1) for j in range(n)]
    e_bin = [pulp.LpVariable(f"e_{j}", cat="Binary") for j in range(n)]

    # Objective: prefer fewer electrolytes in the mixture (sparsity), but this is secondary to feasibility.
    prob += pulp.lpSum(e_bin)

    # Composition constraints
    for i in range(len(S_compounds)):
        prob += pulp.lpSum(S[i, j] * v_vars[j] for j in range(n)) == t1[i]
    for i in range(len(M_compounds)):
        prob += pulp.lpSum(M[i, j] * v_vars[j] for j in range(n)) == t2[i]

    # Fractions should sum to 1 (final mixture fully specified)
    prob += pulp.lpSum(v_vars) == 1.0

    # Link binary usage with fractions using Big-M and epsilon.
    for j in range(n):
        prob += v_vars[j] <= big_m * e_bin[j]
        prob += v_vars[j] >= eps * e_bin[j]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if prob.status != pulp.LpStatusOptimal:
        raise ValueError("No optimal solution found")

    solution = {valid_candidates[j].name: v_vars[j].varValue for j in range(n) if v_vars[j].varValue and v_vars[j].varValue > 0}

    return solution
