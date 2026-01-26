# How to use these docs

Before consulting the documentation, make sure to read BatteryLab's main README, even if the system has already been installed. It is useful to know how the system was installed. 

The purpose of this directory is to preserve knowledge about the system as it is developed. If someone has previously encountered an issue, it should have been documented somewhere in this directory. As a review, the directory can be searched using the ```grep``` command
```bash
    $ grep -r "phrase" .
```
where the '-r' flag stands for 'recursive' (search through subdirectories as well), the "phrase" specifies what keyword or phrase should be found, and "." indicates the current directory as the start point of the search. Note that grep will not search files or directories outside of this directory. For example, if you execute this command in /Research/BatteryLab/docs/how_to, it will not search through /Research/BatteryLab/docs/troubleshooting.

New documents should be placed inside one of the available subfolders:

1. known_issues
    - descriptions of ongoing problems and records of attempted solutions
2. troubleshooting
    - descriptions of previously observed errors and how to resolve them
3. how_to
    - walkthroughs for common processes

In each folder, any one issue/process should have its own markdown document with a clear enough name for someone to find their issue from the file navigator.
