from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from core.arl import ARL
import sys
import pandas as pd
import numpy as np
import math
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        

    def initUI(self):
        self.df = None
        self.component_list = None
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('ARL Tool')
        self.initMenuBar()
        self.main = self.mainWidget()
        self.setCentralWidget(self.main)
        self.show()
    
    def initMenuBar(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl-Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)
        openProjectAction = QAction('&Import Data',self)
        openProjectAction.setShortcut('Ctrl-O')
        openProjectAction.setStatusTip('Imports data from a file')
        openProjectAction.triggered.connect(self.openProject)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openProjectAction)
        fileMenu.addAction(exitAction)

    def closeEvent(self, event):
        qApp.quit()

    def openProject(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File','.', filter='*.xlsx')
        self.df = pd.read_excel(fname[0])
        self.populateTable()
    
    def populateTable(self):
        self.budgetText.setText(str(self.df['B'].iloc[0]))
        self.baText.setText(str(self.df['BA'].iloc[0]))
        self.LText.setText(str(self.df['L'].iloc[0]))
        self.cviText.setText(str(self.df['cv'].iloc[0]))
        
        total_components = len(self.df.index)
        self.dataTable.setColumnCount(total_components)
        
        for component in range(total_components):
            c1 = QTableWidgetItem()
            c1.setText(str(self.df['c1'].iloc[component]))
            self.dataTable.setItem(0, component, c1)
            
            ma = QTableWidgetItem()
            ma.setText(str(self.df['Ma'].iloc[component]))
            self.dataTable.setItem(1, component, ma)
            
            mb = QTableWidgetItem()
            mb.setText(str(self.df['Mb'].iloc[component]))
            self.dataTable.setItem(2, component, mb)
            
            c0 = QTableWidgetItem()
            c0.setText(str(self.df['c0'].iloc[component]))
            self.dataTable.setItem(3, component, c0)
            
            mub = QTableWidgetItem()
            mub.setText(str(self.df['mub'].iloc[component]))
            self.dataTable.setItem(4, component, mub)
            
            mud = QTableWidgetItem()
            mud.setText(str(self.df['mud'].iloc[component]))
            self.dataTable.setItem(5, component, mud)
            
            mttri = QTableWidgetItem()
            mttri.setText(str(self.df['MTTRi'].iloc[component]))
            self.dataTable.setItem(6, component, mttri)
            
            
    def getTableData(self):
        self.df['B'].iloc[0] = float(self.budgetText.text())
        self.df['BA'].iloc[0] = float(self.baText.text())
        self.df['L'].iloc[0] = float(self.LText.text())
        self.df['cv'].iloc[0] = float(self.cviText.text())
        
        #total_components = len(self.df.index)
        #self.dataTable.setColumnCount(total_components)
        total_components = self.dataTable.columnCount()
        
        for component in range(total_components):
            c1 = self.dataTable.item(0, component)
            self.df['c1'].iloc[component] = float(c1.text())
            
            ma = self.dataTable.item(1, component)
            self.df['Ma'].iloc[component] = float(ma.text())
            
            
            mb = self.dataTable.item(2, component)
            self.df['Mb'].iloc[component] = float(mb.text())
                        
            c0 = self.dataTable.item(3, component)
            self.df['c0'].iloc[component] = float(c0.text())
                        
            mub = self.dataTable.item(4, component)
            self.df['mub'].iloc[component] = float(mub.text())
                        
            mud = self.dataTable.item(5, component)
            self.df['mud'].iloc[component] = float(mud.text())
                        
            mttri = self.dataTable.item(6, component)
            self.df['MTTRi'].iloc[component] = float(mttri.text())
            
            
        

    def mainWidget(self):
        main = QWidget()
        mainLayout = QVBoxLayout()
        
        inputs = self.generateInputLayout()
        self.dataTable = self.generateDataTable()
        buttons = self.generateButtonLayout()
        
        
        
        mainLayout.addLayout(inputs)
        mainLayout.addWidget(self.dataTable)
        mainLayout.addLayout(buttons)
        main.setLayout(mainLayout)
        
        return main
    
    def addCol(self):
        self.dataTable.setColumnCount(self.dataTable.columnCount() + 1)
    
    def generateButtonLayout(self):
        layout = QVBoxLayout()
        buttonAdd = QPushButton('Add Component')
        buttonAdd.clicked.connect(self.addCol)
        
        self.buttonCompute = QPushButton('Compute')
        self.buttonCompute.clicked.connect(self.compute)
        
        layout.addWidget(buttonAdd, 0, Qt.AlignRight)
        layout.addWidget(self.buttonCompute, 0, Qt.AlignRight)
        
        return layout
    
    
    def generateInputLayout(self):
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)
        
        layout.addWidget(QLabel('Budget (B)'), 0, 0)
        self.budgetText = QLineEdit('100000')
        layout.addWidget(self.budgetText, 0, 1)
        
        layout.addWidget(QLabel('Overall subsystem reliability investment (B<sub>A</sub> &lt; B)'), 1, 0)
        self.baText = QLineEdit('1000')
        layout.addWidget(self.baText, 1, 1)
        
        layout.addWidget(QLabel('System Lifecycle (L)'), 2, 0)
        self.LText = QLineEdit('')
        layout.addWidget(self.LText, 2, 1)
        
        layout.addWidget(QLabel('C<sub>vi</sub>'), 3, 0)
        self.cviText = QLineEdit('')
        layout.addWidget(self.cviText, 3, 1)
        
        layout.addWidget(QLabel('Components to be considered (separated by commas)'), 4, 0)
        self.compText = QLineEdit('1, 2')
        layout.addWidget(self.compText, 4, 1)
        
        layout.addWidget(QLabel('Number of intermediate points to be calculated'), 5, 0)
        self.interText = QLineEdit('20')
        layout.addWidget(self.interText, 5, 1)
        
        return layout
    
    def generateDataTable(self):
        dataTable = QTableWidget()
        dataTable.setRowCount(7)
        dataTable.setColumnCount(2)
        
        dataTable.setVerticalHeaderLabels(['Replacement Cost (c1)','A-Mode Failure Rate (Ma)', 'B-Mode Failure Rate (Mb)', 'Operating Cost (c0)', u'B-Mode Failure Rate (\u03BC b)', u'B-Mode Fixed-effectiveness factor (\u03BC d)', 'Mean Time to Repair (MTTRi)'])
        
        return dataTable
    
    def compute(self):
        print('Compute')
        self.buttonCompute.setText('Working..')
        self.getTableData()
        self.arl = ARL(self.df, [int(i)-1 for i in str.split(str(self.compText.text()), ',')], int(self.interText.text()))
        self.arl.avail_ = []
        self.arl.eta_ = []
        self.arl.budget_ = []
        
        if len(self.df):
            #self.arl.data = self.df
            #arl.componentIndices = [int(i)-1 for i in str.split(str(self.compText.text()), ',')]
            #arl.budget = int(float(self.budgetText.text()))
            #arl.ba = int(float(self.baText.text()))
            #arl.eps = 0.001
            self.optimal_investment = self.arl.mysticCompute()
            
            self.showResultWindow()
            self.buttonCompute.setText('Compute')
            
    
    def showResultWindow(self):
        self.resultDialog = QDialog()
        layout = QVBoxLayout()
        
        
        self.generateComboBox()
        xAxisLength = self.generateXAxisBox()
        
        self.tabs = QTabWidget()
        self.generateTabs(0)
        
        layout.addWidget(self.comboBox)
        #layout.addLayout(xAxisLength)
        layout.addWidget(self.tabs)
        
        self.resultDialog.setLayout(layout)
        self.resultDialog.show()
    
    def generateXAxisBox(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Availability improvement budget limit'))
        self.baLimitTextBox = QLineEdit(str(self.arl.ba))
        self.recomputeButton = QPushButton('Recompute')
        self.recomputeButton.clicked.connect(self.recompute)
        layout.addWidget(self.baLimitTextBox)
        layout.addWidget(self.recomputeButton)
        return layout
    
    def recompute(self):
        self.arl.ba = int(self.baLimitTextBox.text())
        self.generateTabs(self.comboBox.currentIndex())
    
    def generateComboBox(self):
        self.comboBox = QComboBox()
        self.comboBox.addItem('Impact of investment')
        self.comboBox.addItem('Availability')
        self.comboBox.addItem('Marginal Utility of Subsystems')
        self.comboBox.addItem('System Availability')
        self.comboBox.addItem('Investment in reliability vs. Fleet size')
        self.comboBox.addItem('System availability vs. Fleet size')
        self.comboBox.currentIndexChanged.connect(self.generateTabs)
        #return comboBox
    
    
    def generateTabs(self, index):
        #print(index)
        self.tabs.clear()
        self.plotWidget = QWidget()
        self.tableWidget = QWidget()
        self.plotLayout = self.plotFig(index)
        self.plotWidget.setLayout(self.plotLayout)
               
        self.tableLayout = self.genTable(index)
        self.tableWidget.setLayout(self.tableLayout)
        
        self.tabs.addTab(self.plotWidget, 'Plot')
        self.tabs.addTab(self.tableWidget, 'Data Table')
        
        #return self.tabs
    
    def genTable(self, index):
        layout = QVBoxLayout()
        gammas = np.linspace(0, self.arl.ba, num = self.arl.intermediate)
        resultTable = QTableWidget()
        resultTable.setColumnCount(len(self.arl.componentIndices) + 1)
        resultTable.setRowCount(len(gammas))
        for i, gamma in enumerate(gammas):
                g = QTableWidgetItem()
                g.setText(str(int(gamma)))
                resultTable.setItem(i, 0, g)
        if index == 0:
            labels = ['Investment in reliability']
            for i, idx in enumerate(self.arl.componentIndices):
                labels.append('Component {}'.format(idx))
                lifecycle_costs = self.arl.lc_cost[i]
                for j, cost in enumerate(lifecycle_costs):
                    c = QTableWidgetItem()
                    c.setText(str(cost))
                    resultTable.setItem(j, i+1, c)
            resultTable.setHorizontalHeaderLabels(labels)
        elif index ==1:
            labels = ['Investment in reliability']
            for i, idx in enumerate(self.arl.componentIndices):
                labels.append('Component {}'.format(idx))
                comp_avail = self.arl.comp_avail[i]
                for j, mu in enumerate(comp_avail):
                    c = QTableWidgetItem()
                    c.setText(str(mu))
                    resultTable.setItem(j, i+1, c)
            resultTable.setHorizontalHeaderLabels(labels)
        elif index == 2:
            labels = ['Investment in reliability']
            for i, idx in enumerate(self.arl.componentIndices):
                labels.append('Component {}'.format(idx))
                marg_util = self.arl.marg_util[i]
                for j, mu in enumerate(marg_util):
                    c = QTableWidgetItem()
                    c.setText(str(mu))
                    resultTable.setItem(j, i+1, c)
            resultTable.setHorizontalHeaderLabels(labels)
        elif index == 3:    
            labels = ['Investment in reliability', 'System Availability']
            sys_avail = self.arl.sys_avail_list
            for i, mu in enumerate(sys_avail):
                c = QTableWidgetItem()
                c.setText(str(mu))
                resultTable.setItem(i, 1, c)
            resultTable.setHorizontalHeaderLabels(labels)
        elif index == 4:
            labels = ['Investment in reliability', 'Fleet Size']
            fleet_size = self.arl.opt_fleet_size
            for i, mu in enumerate(fleet_size):
                c = QTableWidgetItem()
                c.setText(str(mu))
                resultTable.setItem(i, 1, c)
            resultTable.setHorizontalHeaderLabels(labels)
        elif index == 5:
            labels = ['System Availability', 'Fleet Size']
            sys_avail = self.arl.sys_avail_list
            fleet_size = self.arl.opt_fleet_size
            for i, mu in enumerate(fleet_size):
                c = QTableWidgetItem()
                c.setText(str(mu))
                resultTable.setItem(i, 1, c)
                d = QTableWidgetItem()
                d.setText(str(sys_avail[i]))
                resultTable.setItem(i, 0, d)
            resultTable.setHorizontalHeaderLabels(labels)
        layout.addWidget(resultTable)
        return layout
    
    def plotFig(self, index):
        gammas = np.linspace(0, self.arl.ba, num = self.arl.intermediate)
        #gammas = list(zip(*self.optimal_investment))
        #print(gammas)
        fig, ax1 = plt.subplots(1, 1)
        #ax1 = fig.add_subplot(111)
        
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
        
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        
        
        if index == 0:
            self.arl.get_lc_costs(gammas)
            for i, idx in enumerate(self.arl.componentIndices):
                ax1.plot(gammas, self.arl.lc_cost[i], label="Component {}".format(idx+1))
            ax1.set_xlabel("Investment in reliability $\gamma_i$")
            ax1.set_ylabel("Subsystem Lifecycle Cost ($C_i$)")
            ax1.set_title("Impact of investment in reliability improvement\n on subsystem lifecycle cost")
        elif index == 1:
            self.arl.get_comp_avail(gammas)
            for i, idx in enumerate(self.arl.componentIndices):
                ax1.plot(gammas, self.arl.comp_avail[i], label="Component {}".format(idx+1))
            ax1.set_xlabel("Investment in reliability $\gamma_i$")
            ax1.set_ylabel("Availability")
            ax1.set_title("Impact of investment in reliability improvement\n on subsystem availability")
        elif index == 2:
            self.arl.get_marg_util(gammas)
            for i, idx in enumerate(self.arl.componentIndices):
                ax1.step(gammas, self.arl.marg_util[i], label="Component {}".format(idx+1))
            ax1.set_xlabel("Investment in reliability $\gamma_i$")
            ax1.set_ylabel("Fleet Size")
            ax1.set_title("Marginal utility of subsystem reliability investment\n on fleet size")
        elif index == 3:
            self.arl.get_sys_avail()
            plotline = self.arl.sys_avail_list
            ax1.plot(gammas, plotline)
            ax1.set_xlabel("Investment in reliability $\gamma_i$")
            ax1.set_ylabel("System Availability")
            ax1.set_title("Impact of optimal investment in reliability\n improvement on system availability")
        elif index == 4:
            self.arl.get_fleet_size()
            plotline = self.arl.opt_fleet_size
            ax1.plot(gammas, plotline)
            ax1.set_xlabel("Investment in reliability $\gamma_i$")
            ax1.set_ylabel("Fleet Size")
            ax1.set_title("Impact of optimal investment in reliability\n improvement on fleet size")
        elif index == 5:
            self.arl.get_sys_avail()
            self.arl.get_fleet_size()
            ax1.plot(self.arl.sys_avail_list, self.arl.opt_fleet_size)
            ax1.set_xlabel("Fleet Size")
            ax1.set_ylabel("System Availability (A)")
            ax1.set_title("Optimal availability and fleet size for various investments")
        
        ax1.legend()
        canvas.draw()
        layoutfig = QVBoxLayout()
        layoutfig.addWidget(toolbar)
        layoutfig.addWidget(canvas, 1)
        plt.tight_layout()
        return layoutfig
        