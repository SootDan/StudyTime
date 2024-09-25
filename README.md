# StudyTime
## Video Demo:
TBD  
  
## Description
StudyTime is an easy-to-use app that tracks statistics of your studying data on subjects of your choice. You may have several databanks at once and also optionally set deadlines. StudyTime then calculates the average necessary amount of studying per day, week, and month to achieve your set goal.  
StudyTime is free and open source and targets Android, Linux, and Windows and is available in English as well as German. The Linux version comes with an optional CLI version. 
  
### Current Features:
- SQLite Database  
- Terminal Statistics Output  
  
### Current Bugs:
- User input not clean, causes crashing  
  
## About
### Documentation
My main goal for this app was creating easily readable and clean code. I focused on making sure the variables were type safe and the methods/classes had proper doc strings that explained their use succinctly. I felt particularly inspired by the strong type safety of C#, which I have been using a lot for personal projects recently.  
I started out making an SQL database that sorted each subject into its own respective table. I noticed that the output strings were cluttering up my code, so I offloaded them to a json file. Then I formatted the SQL database into a readable string.  
Cleaned the code and tried to optimise it into smaller, more readable bits. Made SQL more modular; it now supports multiple databases at the same time if needed.  
Enums served to declutter the SQL within the code.  
I added a German language option. At this point, I started experimenting with a basic GUI using Qt Designer with PyQt6. However, I still wanted to maintain a CLI version in case anybody preferred that. To do this, I started a major code refactoring process that lets both GUI and CLI import from the same code without repetition.  
I decided to switch to pandas at this point.  This allowed me to format the data easily and well. Then, I added the function to create deadlines for individual subjects; the app will then calculate the average hours required per day, week, and month. Of course, one may choose not to set a deadline at all.  
The main code is now working and able to be used during studies; however, I wanted to go further. Now, I wanted to start giving the ability to manipulate the data within and edit the SQL tables as fit.
  
### Creator
This project is created and maintained solely by myself.  
  
## Sources
[Creating Arch Packages](https://wiki.archlinux.org/title/Creating_packages)  
[SQLite Python Documentation](https://docs.python.org/3/library/sqlite3.html)  
[SQLite Time Documentation](https://www.sqlite.org/lang_datefunc.html)  
[Glob Documentation](https://docs.python.org/3/library/glob.html#glob.escape)  
[Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/general_functions.html)  
[Python Datetime Documentation](https://docs.python.org/3/library/time.html#module-time)  
[Python Enum Documentation](https://docs.python.org/3/howto/enum.html)  
[QtDesigner Tutorial](https://youtu.be/tJQdfwAohlw?si=7eDugUCnUDzqasO2)  
