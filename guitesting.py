import sys
from PyQt5 import QtGui, QtWidgets, uic
import GuiStuff
import matplotlib.pyplot as plt

import random

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


class Ui(QtWidgets.QDialog):

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        ui = GuiStuff.Ui_MainWindow()
        ui.setupUi(mainWindow)

        #All event connections will go here


        ui.lineEdit_Time.editingFinished.connect(self.enterPress)
       # ui.lineEdit
        ui.lineEdit_
        mainWindow.show()
        sys.exit(app.exec_())

    #event functions go here.
    ''''
    def varibles(self):
    comp_a = {'L': lineEdit_Time, 'c1': lineEdit_Initial_Cost, 'Ma': lineEdit_A_Mode_2, 'Mb': lineEdit_B_Mode, 'c0': lineEdit_Operating_Cost, 'mub':lineEdit_Cost_Increment , 
    'mud': lineEdit_B_Mode, 'cv':lineEdit_FEF, 'gamma': x[0]}
    
     comp_b = {'L': lineEdit_Time_2, 'c1': lineEdit_Intital_Cost_2, 'Ma': lineEdit_A_Mode_3, 'Mb': lineEdit_B_Mode_2, 'c0': lineEdit_Operating_Cost_2, 'mub': lineEdit_Cost_Increment_2, 
     'mud': lineEdit_B_Mode_2, 'cv': lineEdit_FEF_2, 'gamma': x[1]}
    ''''

    def enterPress(self):

        print('hello')


if __name__ == '__main__':

    Ui()
    #main = GuiStuff.Ui_MainWindow()

