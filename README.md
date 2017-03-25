# Welcome to The ARL-Project!  
**_GUI for Rotorcraft Tradespace Exploration_**

**Program:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AWESOME NAME HERE
**Version:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pre-Alpha  
**Release Date:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;March 25, 2017

---

## README Contents

1. Configuration Used
2. Contributing to the GUI

---

### 1. **Configuration Used**
  * Python 2.7.6
  * Qt Version 5.6.2
  * Qt Designer 5.6.2 
    * Qt Designer is included with Anaconda, located in ```C:\Wherever_You_Installed\Anaconda2\Library\bin\designer.exe```
  * ```pyuic5.bat```
    * Also included with Anaconda, located in ```C:\Wherever_You_Installed\Anaconda2\Library\bin\pyuic5.bat```

### 2. **Contributing to the GUI**
  * Qt Designer saves files with the extension ```.ui```.
  * It is necessary to convert the ```.ui``` file to the ```.py``` extension for use with Python.
  * The ```pyuic5.bat``` file handles this conversion.
  * Usage:
```
C:\Your_Development_Branch\Directory>pyuic5.bat GuiStuff.ui > GuiStuff.py
```
  * In the above example, ```GuiStuff.ui``` is the file to be converted, and ```GuiStuff.py``` is the  destination file. Here, the ```.ui``` file is located in the current working directory, and the ```.py``` is created in the current working directory. Otherwise, the directories must be specified.
  * The ```pyuic5.bat``` file can be run from any directory. 
  * After the above procedure, edit ```guitesting.py``` to change any backend features.
  * Finally, edit ```ash_re_ca_testGraph.py``` to change the methods to calculate optimal reliability investments.