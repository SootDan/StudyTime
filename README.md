# StudyTime
## Video Demo:
TBD  
  
## Description
WIP  
  
### Current Features:
- SQLite Database  
- Terminal Statistics Output
  
### To-Do:
WIP  
  
### Current Bugs:
- User input not clean, causes crashing
  
## About
### Documentation
My main goal for this app was creating easily readable and clean code. I focused on making sure the variables were type safe and the methods/classes had proper doc strings that explained their use succinctly. I felt particularly inspired by the strong type safety of C#, which I have been using a lot for personal projects recently.  
I started out making an SQL database that sorted each subject into its own respective table. I noticed that the output strings were cluttering up my code, so I offloaded them to a json file. Then I formatted the SQL database into a readable string using pandas.  
Cleaned the code and tried to optimise it into smaller, more readable bits. Made SQL more modular; it now supports multiple databases at the same time if needed.  
Enums served to declutter the SQL within the code.
  
### Creator
This project is created and maintained solely by myself.  
  
## Sources
[SQLite Python Documentation](https://docs.python.org/3/library/sqlite3.html)  
[SQLite Time Documentation](https://www.sqlite.org/lang_datefunc.html)  
[Pandas Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html#pandas.read_sql_query)  
[Creating Arch Packages](https://wiki.archlinux.org/title/Creating_packages)  