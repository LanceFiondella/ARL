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
        if len(fname[0]) > 0:
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
        
        self.resultDialog = ResultWindow(self.arl)
        self.resultDialog.show()
    

    
    
    
   
 
 
 
class ResultWindow(QDialog):
    """
    Defines the Results window
    """
    def __init__(self, arl):
        super(ResultWindow, self).__init__()
        self.arl = arl
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.genTabs())
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 800, 600)
    
    def genTabs(self):
        """
        Generates top level tabs
        """
        self.tabs = QTabWidget()
        self.tabs.addTab(self.genSLATab(), 'Subsystem Level Assessment')
        self.tabs.addTab(self.genFSTab(), 'Optimal subsystem investment to maximize fleet size')
        self.tabs.addTab(self.genAVTab(), 'Optimal subsystem investment to maximize availability')
        
        return self.tabs
    
    def genSLATab(self):
        """
        Generates contents of Subsystem Level Assessment tab
        """
        self.SLATab = QWidget()
        self.SLAlayout = QVBoxLayout(self.SLATab)
        self.SLAcomboBox = QComboBox()
        self.SLAcomboBox.addItems(['Impact of investment', 'Availability'])
        
        self.SLAcomboBox.activated.connect(self.SLAdata)
        self.SLAtabs = QTabWidget()
        
        self.SLAlayout.addWidget(self.SLAcomboBox)
        self.SLAlayout.addWidget(self.SLAtabs)
        self.SLAdata(0)
        
        #self.SLATab.setLayout(layout)
        return self.SLATab
    
    def SLAdata(self, select):
        """
        Handles the Subsystem Level Assessment tab's drop down menu
        """
        gammas = np.linspace(0, self.arl.ba, num = self.arl.intermediate)
        plot = QWidget()
        #layout.addWidget(self.SLAcomboBox)
        table = QWidget()
        
        if select == 0:
            self.arl.get_lc_costs(gammas)
            plot.setLayout(self.genPlot(xlabel = "Investment in reliability $\gamma_i$", 
                         ylabel = "Subsystem Lifecycle Cost ($C_i$)", 
                         title ="Impact of investment in reliability improvement\n on subsystem lifecycle cost",
                         gammas = gammas,
                         y = self.arl.lc_cost))
            table.setLayout(self.genTable(y =  self.arl.lc_cost,
                                          gammas = gammas,
                           labels = ['Investment in reliability']))
            
        elif select == 1:
            self.arl.get_comp_avail(gammas)
            plot.setLayout(self.genPlot(xlabel = "Investment in reliability $\gamma_i$", 
                        ylabel = "Availability", 
                        title ="Impact of investment in reliability improvement\n on subsystem availability",
                        gammas = gammas,
                        y = self.arl.comp_avail))
            table.setLayout(self.genTable(y =  self.arl.comp_avail,
                                          gammas = gammas,
                           labels = ['Investment in reliability']))
        self.SLAtabs.clear()
        self.SLAtabs.addTab(plot, "Plot")
        self.SLAtabs.addTab(table, "Table")

    def genFSTab(self):
        """
        Generates contents of 'Optimal subsystem investment to maximize fleet size' tab
        """
        self.FSTab = QWidget()
        layout = QVBoxLayout()
        self.FScomboBox = QComboBox()
        self.FScomboBox.addItems(['Marginal Utility of Subsystems', 'System Availability'] )
        self.FScomboBox.activated.connect(self.FSdata)
        self.FStabs = QTabWidget()
       
        
        layout.addWidget(self.FScomboBox)
        layout.addWidget(self.FStabs)
        self.FSdata(0)
        self.FSTab.setLayout(layout)
        return self.FSTab
    
    def FSdata(self, select):
        """
        Handles 'Optimal subsystem investment to maximize fleet size' tab's dropdown menu
        """
        gammas = np.linspace(0, self.arl.ba, num = self.arl.intermediate)
        plot = QWidget()
        table = QWidget()
        
        if select == 0:
            self.arl.get_marg_util(gammas)
            plot.setLayout(self.genPlot(gammas = gammas,
                                        y = self.arl.marg_util,
                                        xlabel = "Investment in reliability $\gamma_i$", 
                                        ylabel = "Fleet Size", 
                                        title ="Marginal utility of subsystem reliability investment\n on fleet size"))
            table.setLayout(self.genTable(y = self.arl.marg_util,
                                          gammas = gammas,
                                          labels = ['Investment in reliability']))
        elif select ==1:
            self.arl.get_sys_avail()
            
            plot.setLayout(self.genPlot(gammas = gammas,
                                        y = self.arl.sys_avail_list,
                                        xlabel = "Investment in reliability $\gamma_i$",
                                        ylabel = "System Availability",
                                        title = "Impact of optimal investment in reliability\n improvement on system availability",
                                        components = False))
            table.setLayout(self.genTable(gammas = gammas,
                                          y = self.arl.sys_avail_list,
                                          labels = ['Investment in reliability', 'System Availability'],
                                          components = False))
            
        self.FStabs.clear()
        self.FStabs.addTab(plot, "Plot")
        self.FStabs.addTab(table, "Table")
    
    def genAVTab(self):
        self.AVTab = QWidget()
        layout = QVBoxLayout()
        self.AVcomboBox = QComboBox()
        self.AVcomboBox.addItems(['Investment in reliability vs. Fleet size', 'System availability vs. Fleet size'])
        self.AVcomboBox.activated.connect(self.AVdata)
        self.AVtabs = QTabWidget()
        
        layout.addWidget(self.AVcomboBox)
        layout.addWidget(self.AVtabs)
        self.AVdata(0)
        self.AVTab.setLayout(layout)
        return self.AVTab
    
    def AVdata(self, select):
        """
        Handles System avail tab's dropdown menu
        """
        gammas = np.linspace(0, self.arl.ba, num = self.arl.intermediate)
        plot = QWidget()
        table = QWidget()
        
        if select == 0:
            self.arl.get_fleet_size()
            plot.setLayout(self.genPlot(gammas = gammas,
                                        y = self.arl.opt_fleet_size,
                                        xlabel = "Investment in reliability $\gamma_i$",
                                        ylabel = "Fleet Size",
                                        title = "Impact of optimal investment in reliability\n improvement on fleet size",
                                        components = False))
            table.setLayout(self.genTable(gammas = gammas,
                                          y = self.arl.opt_fleet_size,
                                          labels = ['Investment in reliability', 'Fleet Size'],
                                          components = False))
        elif select == 1:
            self.arl.get_sys_avail()
            self.arl.get_fleet_size()
            plot.setLayout(self.genPlot(gammas = self.arl.sys_avail_list,
                                        y = self.arl.opt_fleet_size,
                                        xlabel = "Fleet Size",
                                        ylabel = "System Availability (A)",
                                        title = "Optimal availability and fleet size for various investments",
                                        components = False))
            table.setLayout(self.genTable(gammas = self.arl.sys_avail_list,
                                          y = self.arl.opt_fleet_size,
                                          labels = ['System Availability', 'Fleet Size'],
                                          components = False))


        self.AVtabs.clear()
        self.AVtabs.addTab(plot, "Plot")
        self.AVtabs.addTab(table, "Table")
    
    
    def genPlot(self, components= True, **kwargs):
        fig, ax1 = plt.subplots(1, 1)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
        
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        if components:
            for i, idx in enumerate(self.arl.componentIndices):
                ax1.step(kwargs['gammas'], kwargs['y'][i], label="Component {}".format(idx+1))
        else:
            ax1.step(kwargs['gammas'], kwargs['y'])
            
        ax1.set_xlabel(kwargs['xlabel'])
        ax1.set_ylabel(kwargs['ylabel'])
        ax1.set_title(kwargs['title']) 
        ax1.legend()
        canvas.draw()
        layoutfig = QVBoxLayout()
        layoutfig.addWidget(toolbar)
        layoutfig.addWidget(canvas, 1)
        plt.tight_layout()
        return layoutfig
    
    def genTable(self,components= True, **kwargs):
        labels = kwargs['labels']
        gammas = kwargs['gammas']
        layout = QVBoxLayout()
        resultTable = QTableWidget()
        
        resultTable.setRowCount(len(gammas))
        
        if components:
            resultTable.setColumnCount(len(self.arl.componentIndices) + 1)
            for i, idx in enumerate(self.arl.componentIndices):
                labels.append('Component {}'.format(idx))
                lifecycle_costs = kwargs['y'][i]
                for j, cost in enumerate(lifecycle_costs):
                    c = QTableWidgetItem()
                    c.setText(str(cost))
                    resultTable.setItem(j, i+1, c)
        else:
            resultTable.setColumnCount(2)
            data = kwargs['y']
            for j, cost in enumerate(data):
                c = QTableWidgetItem()
                c.setText(str(cost))
                resultTable.setItem(j, 1, c)
        
        
        for i, gamma in enumerate(gammas):
                g = QTableWidgetItem()
                g.setText(str(int(gamma)))
                resultTable.setItem(i, 0, g)
        
        resultTable.setHorizontalHeaderLabels(labels)
        layout.addWidget(resultTable)
        return layout