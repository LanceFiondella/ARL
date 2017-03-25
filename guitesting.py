import sys
import os
import time
import numpy
import pandas
from PyQt5 import QtGui, QtWidgets, uic
import GuiStuff #import the GUI layout

import ash_re_ca_testGraph as func #import the reliability functions


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random



class Ui(QtWidgets.QMainWindow, GuiStuff.Ui_MainWindow):

    def __init__(self):
        #initialization functions go here (including globals for this file):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = GuiStuff.Ui_MainWindow()
        self.ui.setupUi(self)
        self.df = []
        self.columnNum = 0

        #All event connections will go here:
        self.ui.SelectFileButton.clicked.connect(self.selectFile) #select xls file for import
        self.ui.RunButton.pressed.connect(self.updateText) #helper function to display 'running' while running application
        self.ui.RunButton.clicked.connect(self.enterPress) #main function that sets up and runs program


    #event functions go here:

    def updateText(self):
        # helper function to display 'running' while running application

        if len(self.df):
            self.ui.RunButton.setText("Running")
    def enterPress(self):
        # main function that sets up and runs program
        if len(self.df):

            #set up variables
            self.setVariablesFromDisplay()
            func.df = self.df
            func.component = int(self.ui.lineEdit_Components.text())
            func.budget = int(self.ui.lineEdit_Budget.text())
            func.eps = float(self.ui.lineEdit_Epsilon.text())

            #run operations
            func.ahs_Ca()

            #display results in table field
            self.columnNum = max(len(func.etaData), len(func.AvailabilityData))
            self.ui.tableWidget.setColumnCount(self.columnNum)
            self.ui.tableWidget.setRowCount(2)
            self.ui.tableWidget.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem("etaData With Differential Evolution"))
            self.ui.tableWidget.setVerticalHeaderItem(1, QtWidgets.QTableWidgetItem("Availability Data With Differential Evolution"))

            for q in range(0, self.columnNum):
                self.ui.tableWidget.setItem(0, q, QtWidgets.QTableWidgetItem(str(func.etaData[q])))
                self.ui.tableWidget.setItem(1, q, QtWidgets.QTableWidgetItem(str(func.AvailabilityData[q])))

            #display plots in plot window
            rfg = reliFleet_graph()
            rag = reliAvail_graph()
            afg = availFleet_graph()

            self.ui.plotGrid_1.addWidget(rag)
            self.ui.plotGrid_2.addWidget(rfg)
            self.ui.plotGrid_3.addWidget(afg)

            #update text after completion
            self.ui.RunButton.setText("RUN")

    def selectFile(self):
        #This function will open the excel sheet that contains the data
        self.ui.fileDlg = QtWidgets.QFileDialog()
        filename = self.ui.fileDlg.getOpenFileName(self, 'Open Excel file', os.getcwd(),"Excel files (*.xls *.xlsx)")
        self.df = pandas.read_excel(filename[0])
        self.displayVariables()

    def displayVariables(self):
        #update the text boxes to display the variables read from the excel sheet
        self.ui.lineEdit_L_1.setText(str(self.df['L'].values[0]))
        self.ui.lineEdit_Ma_1.setText(str(self.df['Ma'].values[0]))
        self.ui.lineEdit_Mb_1.setText(str(self.df['Mb'].values[0]))
        self.ui.lineEdit_mud_1.setText(str(self.df['mud'].values[0]))
        self.ui.lineEdit_mub_1.setText(str(self.df['mub'].values[0]))
        self.ui.lineEdit_c1_1.setText(str(self.df['c1'].values[0]))
        self.ui.lineEdit_c0_1.setText(str(self.df['c0'].values[0]))
        self.ui.lineEdit_MTTRi_1.setText(str(self.df['MTTRi'].values[0]))

        self.ui.lineEdit_L_2.setText(str(self.df['L'].values[1]))
        self.ui.lineEdit_Ma_2.setText(str(self.df['Ma'].values[1]))
        self.ui.lineEdit_Mb_2.setText(str(self.df['Mb'].values[1]))
        self.ui.lineEdit_mud_2.setText(str(self.df['mud'].values[1]))
        self.ui.lineEdit_mub_2.setText(str(self.df['mub'].values[1]))
        self.ui.lineEdit_c1_2.setText(str(self.df['c1'].values[1]))
        self.ui.lineEdit_c0_2.setText(str(self.df['c0'].values[1]))
        self.ui.lineEdit_MTTRi_2.setText(str(self.df['MTTRi'].values[1]))

        self.ui.lineEdit_L_3.setText(str(self.df['L'].values[2]))
        self.ui.lineEdit_Ma_3.setText(str(self.df['Ma'].values[2]))
        self.ui.lineEdit_Mb_3.setText(str(self.df['Mb'].values[2]))
        self.ui.lineEdit_mud_3.setText(str(self.df['mud'].values[2]))
        self.ui.lineEdit_mub_3.setText(str(self.df['mub'].values[2]))
        self.ui.lineEdit_c1_3.setText(str(self.df['c1'].values[2]))
        self.ui.lineEdit_c0_3.setText(str(self.df['c0'].values[2]))
        self.ui.lineEdit_MTTRi_3.setText(str(self.df['MTTRi'].values[2]))

        self.ui.lineEdit_L_4.setText(str(self.df['L'].values[3]))
        self.ui.lineEdit_Ma_4.setText(str(self.df['Ma'].values[3]))
        self.ui.lineEdit_Mb_4.setText(str(self.df['Mb'].values[3]))
        self.ui.lineEdit_mud_4.setText(str(self.df['mud'].values[3]))
        self.ui.lineEdit_mub_4.setText(str(self.df['mub'].values[3]))
        self.ui.lineEdit_c1_4.setText(str(self.df['c1'].values[3]))
        self.ui.lineEdit_c0_4.setText(str(self.df['c0'].values[3]))
        self.ui.lineEdit_MTTRi_4.setText(str(self.df['MTTRi'].values[3]))


    def setVariablesFromDisplay(self):
        self.df['L'].values[0] = int(self.ui.lineEdit_L_1.text())
        self.df['Ma'].values[0] = int(self.ui.lineEdit_Ma_1.text())
        self.df['Mb'].values[0] = int(self.ui.lineEdit_Mb_1.text())
        self.df['mud'].values[0] = float(self.ui.lineEdit_mud_1.text())
        self.df['mub'].values[0] = int(self.ui.lineEdit_mub_1.text())
        self.df['c1'].values[0] = int(self.ui.lineEdit_c1_1.text())
        self.df['c0'].values[0] = int(self.ui.lineEdit_c0_1.text())
        self.df['MTTRi'].values[0] = int(self.ui.lineEdit_MTTRi_1.text())

        self.df['L'].values[1] = int(self.ui.lineEdit_L_2.text())
        self.df['Ma'].values[1] = int(self.ui.lineEdit_Ma_2.text())
        self.df['Mb'].values[1] = int(self.ui.lineEdit_Mb_2.text())
        self.df['mud'].values[1] = float(self.ui.lineEdit_mud_2.text())
        self.df['mub'].values[1] = int(self.ui.lineEdit_mub_2.text())
        self.df['c1'].values[1] = int(self.ui.lineEdit_c1_2.text())
        self.df['c0'].values[1] = int(self.ui.lineEdit_c0_2.text())
        self.df['MTTRi'].values[1] = int(self.ui.lineEdit_MTTRi_2.text())

        self.df['L'].values[2] = int(self.ui.lineEdit_L_3.text())
        self.df['Ma'].values[2] = int(self.ui.lineEdit_Ma_3.text())
        self.df['Mb'].values[2] = int(self.ui.lineEdit_Mb_3.text())
        self.df['mud'].values[2] = float(self.ui.lineEdit_mud_3.text())
        self.df['mub'].values[2] = int(self.ui.lineEdit_mub_3.text())
        self.df['c1'].values[2] = int(self.ui.lineEdit_c1_3.text())
        self.df['c0'].values[2] = int(self.ui.lineEdit_c0_3.text())
        self.df['MTTRi'].values[2] = int(self.ui.lineEdit_MTTRi_3.text())

        self.df['L'].values[3] = int(self.ui.lineEdit_L_4.text())
        self.df['Ma'].values[3] = int(self.ui.lineEdit_Ma_4.text())
        self.df['Mb'].values[3] = int(self.ui.lineEdit_Mb_4.text())
        self.df['mud'].values[3] = float(self.ui.lineEdit_mud_4.text())
        self.df['mub'].values[3] = int(self.ui.lineEdit_mub_4.text())
        self.df['c1'].values[3] = int(self.ui.lineEdit_c1_4.text())
        self.df['c0'].values[3] = int(self.ui.lineEdit_c0_4.text())
        self.df['MTTRi'].values[3] = int(self.ui.lineEdit_MTTRi_4.text())


#Plotting functions are created as separate classes
class CanvasTemplate(FigureCanvas):
    #prototype or creating a plot
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class reliFleet_graph(CanvasTemplate):

    def compute_initial_figure(self):
        self.axes.plot(func.xaxis,
                       func.etaData)
        self.axes.set_xlabel('Investment in reliability')
        self.axes.set_ylabel('Fleet Size')


class reliAvail_graph(CanvasTemplate):

    def compute_initial_figure(self):

        self.axes.plot(func.xaxis,
                       func.AvailabilityData)
        self.axes.set_xlabel('Investment in reliability')
        self.axes.set_ylabel('System Availability (A)')


class availFleet_graph(CanvasTemplate):

    def compute_initial_figure(self):

        self.axes.plot(func.AvailabilityData,
                       func.etaData)
        self.axes.set_xlabel('System Availability (A)')
        self.axes.set_ylabel('Fleet Size')



class graph_Cost_Investment(CanvasTemplate):

    def compute_initial_figure(self):

        self.axes.plot(func.set_comp_temp[1], func.set_comp_temp[2])
        self.axes.set_xlabel('INVESTMENT')
        self.axes.set_ylabel('COST')


if __name__ == '__main__':
    #This is the first operation  to be run on startup.
    #AKA the 'Main' function
    app = QtWidgets.QApplication(sys.argv)
    GUI = Ui()
    ui = GuiStuff.Ui_MainWindow()
    GUI.show()
    sys.exit(app.exec_())
