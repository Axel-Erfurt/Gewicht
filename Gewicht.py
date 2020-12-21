#!/usr/bin/python3
# -*- coding: utf-8 -*-
#########################################################
import csv, time
from PyQt5.QtCore import (QFile, QSize, Qt, QUrl, QDate, pyqtSignal)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QDesktopServices
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QVBoxLayout, QCalendarWidget, 
        QTableWidget, QTableWidgetItem, QLabel, QWidget, QInputDialog, QDateEdit)
from qcharts import (AreaChart, DataTable)
from os import path
#########################################################
mwidth = 900
mheight = 700

class PyDateEdit(QDateEdit):
    def __init__(self, *args):
        super(PyDateEdit, self).__init__(*args)
        self.setDisplayFormat("dddd, dd.MMMM yyyy")
        self.setDate(QDate.currentDate())
        self.setCalendarPopup(True)
        self.__cw = None
        self.__firstDayOfWeek = Qt.Monday
        self.__gridVisible = False
        self.__horizontalHeaderFormat = QCalendarWidget.ShortDayNames
        self.__navigationBarVisible = True

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon("waage.png"))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.myfile = 'Gewicht.csv'
        self.isChanged = False

        self.setStyleSheet(stylesheet(self))
        self.list = []
        self.date = ""
        self.time = ""
        self.setWindowTitle("Gewicht")

        self.tableview = QTableWidget()
        self.tableview.setColumnCount(3)
        self.tableview.cellChanged.connect(self.isModified)
        self.setHeaders()
        self.tableview.verticalHeader().setVisible(False)
        self.tableview.horizontalHeader().setVisible(False)
        self.tableview.setSelectionBehavior(self.tableview.SelectRows)
        self.tableview.setSelectionMode(self.tableview.SingleSelection)

        self.imageLabel = QLabel()

        self.mainWidget = QWidget()
 
        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableview)
        self.vbox.addWidget(self.imageLabel)

        self.mainWidget.setLayout(self.vbox)

        self.setCentralWidget(self.mainWidget)
        
        self.start_date = ""
        self.end_date = ""
        
        self.date_edit_start = PyDateEdit()
        self.date_edit_start.setToolTip("Startdatum")
        self.date_edit_start.setFixedWidth(200)
        self.date_edit_start.dateChanged.connect(self.editStartDate)
        
        self.date_edit_end = PyDateEdit()
        self.date_edit_end.setToolTip("Startdatum")
        self.date_edit_end.setFixedWidth(200)
        self.date_edit_end.dateChanged.connect(self.editEndDate)

        self.createToolBars()
        #self.createStatusBar()
        self.setGeometry(0, 30, mwidth, mheight)
        self.show()
        if QFile.exists(self.myfile):
            print("file exists")
            self.loadCsvOnOpen()
        else:
            print("file not exists")
            self.setHeaders()
            self.addRow("")
            
        if self.tableview.rowCount() > 0:
            
            sd = self.tableview.item(0, 3).text()
            ed = self.tableview.item(self.tableview.rowCount()-1, 3).text()
            #print(sd, ed)
            self.date_edit_start.setDate(QDate.fromString(sd, "yyyyMMdd"))
            self.date_edit_end.setDate(QDate.fromString(ed, "yyyyMMdd"))
            self.start_date = self.date_edit_start.date().toString("yyyyMMdd")
            self.end_date = self.date_edit_end.date().toString("yyyyMMdd")
            
    def editStartDate(self):
        ndate = self.date_edit_start.date().toString("dddd, dd.MMMM yyyy")
        sqldate = self.date_edit_start.date().toString("yyyyMMdd")
        print("Start Tag:", sqldate)
        self.start_date = sqldate
        self.updateChart()
        
    def editEndDate(self):
        ndate = self.date_edit_end.date().toString("dddd, dd.MMMM yyyy")
        sqldate = self.date_edit_end.date().toString("yyyyMMdd")
        print("End Tag:", sqldate)
        self.end_date = sqldate
        self.updateChart()

    def makeChart(self):
        if self.tableview.rowCount() > 0:
            self.showChart()

    def isModified(self):
        self.isChanged = True

    def setHeaders(self):
        self.tableview.horizontalHeader().setVisible(True)
        font = QFont()
        font.setPointSize(8)
        self.tableview.horizontalHeader().setFont(font)
        self.tableview.setColumnWidth(0, 190)
        self.tableview.setColumnWidth(1, 55)
        self.tableview.setColumnWidth(2, 180)
        self.tableview.setColumnWidth(3, 0)
        self.tableview.setHorizontalHeaderItem(0, QTableWidgetItem("Datum"))
        self.tableview.setHorizontalHeaderItem(1, QTableWidgetItem("kg"))
        self.tableview.setHorizontalHeaderItem(2, QTableWidgetItem("Bemerkungen"))
        self.tableview.setHorizontalHeaderItem(3, QTableWidgetItem("SQL Datum"))
        self.tableview.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tableview.hideColumn(3)
        self.tableview.setAlternatingRowColors(True)

    def showMessage(self, message):
        self.statusBar().showMessage(message)

    def closeEvent(self, event):
        if self.isChanged == True:
            self.writeCSV()
        event.accept()

    def createToolBars(self):
        self.tb = self.addToolBar("Buttons")
        self.tb.setToolButtonStyle(2)
        self.tb.setMovable(False)
        self.tb.setFloatable(False)
        self.tb.setIconSize(QSize(16, 16))
        self.btnAdd = QAction(QIcon.fromTheme('add'), "neuer Eintrag", self,
                statusTip="neue Messung",
                triggered=self.insertNewRow)
        self.tb.addAction(self.btnAdd)
        self.btnRemove = QAction(QIcon.fromTheme('edit-delete'), "Zeile löschen", self,
                statusTip="Zeile löschen",
                triggered=self.removeRow)
        self.tb.addAction(self.btnRemove)
        self.tb.addSeparator()
        
        self.folderAct = QAction(QIcon.fromTheme('folder'), "Programmordner öffnen", self,
                toolTip="Programmordner öffnen",
                triggered=self.openFolder)
        self.folderAct.setIconText("")
        self.tb.addAction(self.folderAct)
        self.tb.addSeparator()
        self.tb.addWidget(self.date_edit_start)
        self.tb.addWidget(self.date_edit_end)
        self.tb.addSeparator()
        self.updateAct = QAction(QIcon.fromTheme('view-refresh'), "", self,
                toolTip="Diagramm erneuern",
                triggered=self.updateChart)   
        self.tb.addAction(self.updateAct)
        
        
    def openFolder(self):
        myfolder = path.dirname(sys.argv[0])
        QDesktopServices.openUrl(QUrl.fromLocalFile(myfolder))

    def createStatusBar(self):
        self.statusBar().showMessage("Willkommen", 0)

    def loadCsvOnOpen(self):
        filename = self.myfile
        if QFile.exists(filename):
#            f = open(filename, 'r', encoding='utf-8')
            f = open(filename, 'r')
            self.tableview.setRowCount(0)
            self.tableview.setColumnCount(3)
            for rowdata in csv.reader(f, delimiter='\t'):
                row = self.tableview.rowCount()
                self.tableview.insertRow(row)
                if len(rowdata) == 0:
                    self.tableview.setColumnCount(len(rowdata) + 1)
                else:
                    self.tableview.setColumnCount(len(rowdata))
                for column, data in enumerate(rowdata):
                    item = QTableWidgetItem(data)
                    self.tableview.setItem(row, column, item)
            self.setTableAignment()

            self.tableview.horizontalHeader().setStretchLastSection(True)
            self.setHeaders()
            self.tableview.resizeRowsToContents()
            last = self.tableview.rowCount() - 1
            self.tableview.selectRow(last)
            self.showChart()
            self.isChanged = False

    def setTableAignment(self):
        for x in range(self.tableview.rowCount()):
            self.tableview.item(x, 0).setTextAlignment(Qt.AlignRight)
            self.tableview.item(x, 1).setTextAlignment(Qt.AlignRight)
            self.tableview.item(x, 2).setTextAlignment(Qt.AlignCenter)

    def removeRow(self):
        row = self.selectedRow()
        self.tableview.removeRow(row)
        self.isChanged = True
        self.tableview.selectRow(row)
        self.makeChart()

    def selectedRow(self):
        if self.tableview.selectionModel().hasSelection():
            row =  self.tableview.selectionModel().selectedIndexes()[0].row()
            return int(row)
            
    def insertNewRow(self):
        dlg = QInputDialog()
        syst, ok = dlg.getDouble(self, 'neuer Eintrag', "Gewicht", 70.0)
        if ok:
            self.addRow(str(syst))
            self.makeChart()

    def addRow(self, syst):
        row = self.tableview.rowCount()
        self.tableview.insertRow(row)
        self.tableview.horizontalHeader().setStretchLastSection(True)
        
        column = 0
        newItem = QTableWidgetItem(time.strftime("%A, %d.%B %Y"))
        newItem.setTextAlignment(Qt.AlignRight)
        self.tableview.setItem(row,column, newItem)
        
        column = 1
        newItem = QTableWidgetItem(syst)
        newItem.setTextAlignment(Qt.AlignRight)
        self.tableview.setItem(row,column, newItem)
        
        column = 2
        newItem = QTableWidgetItem("")
        self.tableview.setItem(row,column, newItem)
        
        column = 3
        newItem = QTableWidgetItem(time.strftime("%Y%m%d"))
        self.tableview.setItem(row,column, newItem)
        
        self.isChanged = True
        last = self.tableview.rowCount() - 1
        self.tableview.selectRow(last)
        self.tableview.resizeRowsToContents()
        self.makeChart()

    def writeCSV(self):
        with open(self.myfile, 'w') as stream:
            print("saving", self.myfile)
            writer = csv.writer(stream, delimiter='\t')
            for row in range(self.tableview.rowCount()):
                rowdata = []
                for column in range(self.tableview.columnCount()):
                    item = self.tableview.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
        self.isChanged = False
        
    def updateChart(self):
        rowlist = []
        datelist = []
        for row in range(self.tableview.rowCount()):
            if int(self.tableview.item(row, 3).text()) >= int(self.start_date) \
            and int(self.tableview.item(row, 3).text()) <= int(self.end_date):
                rowlist.append(self.tableview.item(row, 1).text())
                datelist.append(self.tableview.item(row, 3).text())
        start = datelist[0][6:]
        print("start:", start)
        self.showChartUpdate(rowlist, start)
        
    def showChartUpdate(self, rowlist, start):
        first_item = int(start)
        table = DataTable()
        table.add_column('Tage')
    
        table.add_column('Gewicht')
    
        k = []

        for row in rowlist:
            item = row
            if item is not None:
                k.append(float(item))
            else:
                k.append(0)
    
        for x in range(len(k)):
            table.add_row([ x+first_item, k[x]])
    
    
        chart = AreaChart(table)
        chart.backgound_color = "blue"
        chart.set_horizontal_axis_column(0)
        chart.haxis_title = 'Tage'
        chart.vaxis_title = 'kg'
        chart.haxis_vmin = first_item
        chart.haxis_vmax = first_item + len(k) - 1
        chart.haxis_step = 1
    
        chart.vaxis_vmin = 60 # min kg
        chart.vaxis_vmax = 150 # max kg
        chart.vaxis_step = 10

        chartfile = 'gewicht.png'
        chart.save(chartfile, QSize(self.width() - 100, self.height() - 400), 100)

        myimage = QImage(chartfile)
        if myimage.isNull():
            self.showMessage("Cannot load %s." % chartfile)
            return
        self.imageLabel.setPixmap(QPixmap.fromImage(myimage))

    def showChart(self):
        first_item = int(self.tableview.item(0, 0).text().partition(", ")[2].partition(".")[0])
        print(first_item)
        table = DataTable()
        table.add_column('Tage')
    
        table.add_column('Gewicht')
    
        k = []

        for row in range(self.tableview.rowCount()):
            item = self.tableview.item(row, 1)
            if item is not None:
                k.append(float(item.text()))
            else:
                k.append(0)
    
        for x in range(len(k)):
            table.add_row([ x+first_item, k[x]])
    
    

        chart = AreaChart(table)
        chart.backgound_color = "blue"
        chart.set_horizontal_axis_column(0)
        chart.haxis_title = 'Tage'
        chart.vaxis_title = 'kg'
        chart.haxis_vmin = first_item
        chart.haxis_vmax = first_item + len(k) - 1
        chart.haxis_step = 1
    
        chart.vaxis_vmin = 60 # min kg
        chart.vaxis_vmax = 150 # max kg
        chart.vaxis_step = 10

        chartfile = 'gewicht.png'
        chart.save(chartfile, QSize(self.width() - 100, self.height() - 400), 100)

        myimage = QImage(chartfile)
        if myimage.isNull():
            self.showMessage("Cannot load %s." % chartfile)
            return
        self.imageLabel.setPixmap(QPixmap.fromImage(myimage))

def stylesheet(self):
        return """
        QTableWidget
        {
            border: 0.5px solid lightgrey;
            border-radius: 0px;
            font-size: 8pt;
            background-color: #e4eef6;
        }       
        QMainWindow
        {
            background: #e9e9e9;
        } 
        QToolBar
        {
            background: #e9e9e9;
        } 
    """

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
