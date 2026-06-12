# Overview
This package implements a linear solver (PuLP) for solution systems with mixed component types. It is intended for use in finding mixtures of solvents where some components are specified by molarity (salts, additives) and others by absolute volume- or volume fraction-based quantities (solvent mixtures).

# Solution setup
For some specified final composition $\vec{v}_{\text{final}}$ and $\vec{m}_{\text{final}}$, the goal is to find the set of volume fractions $\vec{v}_{\text{components}}$ of some minimal set of the electrolytes available that yield the final composition. The available electrolyte solutions are represented as a volume fraction matrix, $\bold{S}$, and a molarity matrix, $\bold{M}$, such that
$$\bold{S}\vec{v}_{\text{components}}=\vec{v}_{\text{final}},$$ and 
$$\bold{M}\vec{v}_{\text{components}}=\vec{m}_{\text{final}}$$
where $M_{i,j}$ is the concentration (mol/L) of component $i$ in available electrolyte $j$, and $S_{i,j}$ is the volume fraction of component $i$ in available electrolyte $j$. 

This system is then solved using a linear optimizer that aims to use as few electrolytes as possible to mix the final composition.

## Example
Given a vial of pure water and a vial of 5M saltwater, 
$$\bold{S} = \begin{bmatrix} 1.0 & 1.0 \\ 0.0 & 0.0 \end{bmatrix}$$
$$\bold{M} = \begin{bmatrix} 0.0 & 0.0 \\ 0.0 & 5.0 \end{bmatrix}$$

# Assumptions and approximations
- Excess molar volume is assumed to be zero (i.e., the volume of a mixture is the same as the sum of its components' volumes). The uncertainty of the error introduced by this approximation increases with the complexity of the consituent solvents. For chemically similar solvents (e.g., all aqueous solutions), this error is not expected to be large.
    - TODO: calculate some cases of large $|\bar{V}^E(x_i)|$ to determine what magnitude of error this could induce in the worst cases.
- In principle, all three component types (`v`, `s`, `a`) could be treated in the same solution step if the densities and molecular weights (MW) of each solution were known. This would allow substances to be used as both core solution components and trace additives. ```pubchempy```, the package used to look up the SMILES string, could be used to retrieve MW, but the densities would be much trickier (temperature dependence and solution effects would require complex thermodynamic models).
    - The current treatment is analogous to how these mixtures might be handled experimentally: a "50 vol% mixture of acetone and chloroform" refers to a mixture in which an equal amount of both acetone and chloroform were added. This is different, however, than the mixture having a volume fraction of 