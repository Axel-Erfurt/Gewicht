#!/usr/bin/python3
# -*- coding: utf-8 -*-
#########################################################
import csv
from PyQt5.QtCore import (QFile, QSize, Qt, QUrl, QDate)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QDesktopServices
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QLineEdit, QFileDialog, 
        QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QDateEdit, QDateTimeEdit, QComboBox)
from os import path
from subprocess import Popen, run
#########################################################

class PyDateEdit(QDateEdit):
    def __init__(self, *args):
        super(PyDateEdit, self).__init__(*args)
        self.setDisplayFormat("dddd, dd.MMMM yyyy")
        self.setDate(QDate.currentDate())
        self.setCalendarPopup(False)
        self.setDisplayFormat("dd.MM.yy")
        self.setStyleSheet(stylesheet(self))
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self:
            if QApplication.mouseButtons() == Qt.LeftButton:
                self.setSelectedSection(QDateTimeEdit.DaySection)
                return True
            else:
                return False
        else:
            return PyDateEdit.eventFilter(obj, event)
            
    def clearDate(self):
        self.findChild(QLineEdit).setText('')

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
        
        self.is_imported = False
        self.canGnuplot = False
        
        self.imgLabel = QLabel()
        self.createStatusBar()
        self.statusBar().hide()

        self.tableview = QTableWidget()
        self.tableview.setColumnCount(3)
        self.tableview.cellChanged.connect(self.isModified)
        self.setHeaders()
        self.tableview.verticalHeader().setVisible(False)
        self.tableview.horizontalHeader().setVisible(False)
        self.tableview.setSelectionBehavior(self.tableview.SelectRows)
        self.tableview.setSelectionMode(self.tableview.SingleSelection)

        self.setCentralWidget(self.tableview)
        
        self.start_date = "20000101"
        self.end_date = QDate.currentDate().toString("yyyyMMdd")
        
        self.date_edit_start = PyDateEdit()
        self.date_edit_start.setToolTip("Startdatum")
        self.date_edit_start.setFixedWidth(200)
        self.date_edit_start.dateChanged.connect(self.editStartDate)
        
        self.date_edit_end = PyDateEdit()
        self.date_edit_end.setToolTip("Startdatum")
        self.date_edit_end.setFixedWidth(200)
        self.date_edit_end.dateChanged.connect(self.editEndDate)

        self.createToolBars()
        self.show()
        if QFile.exists(self.myfile):
            print("file exists")
            self.loadCsvOnOpen()
        else:
            print("file not exists")
            self.setHeaders()
            self.addRow("")

    def setDatesFromTable(self):
        self.canGnuplot = False
        if self.tableview.rowCount() > 0:
            sd = self.tableview.item(0, 0).text()
            ed = self.tableview.item(self.tableview.rowCount() - 1, 0).text()
            self.date_edit_end.setDate(QDate.fromString(ed, "dddd, dd.MMMM yyyy")) 
            self.date_edit_start.setDate(QDate.fromString(sd, "dddd, dd.MMMM yyyy"))     
            #self.canGnuplot = True      
            
    def editStartDate(self):
        self.canGnuplot = False
        self.end_date = self.date_edit_end.date().toString("yyyyMMdd")
        sqldate = self.date_edit_start.date().toString("yyyyMMdd")
        self.start_date = sqldate
        self.updateTable()
        self.canGnuplot = True
        #self.updateImage()

        
    def editEndDate(self):
        self.canGnuplot = False
        self.start_date = self.date_edit_start.date().toString("yyyyMMdd")
        sqldate = self.date_edit_end.date().toString("yyyyMMdd")
        self.end_date = sqldate
        print("Start Tag:", self.start_date, "End Tag:", self.end_date)
        self.updateTable()
        self.canGnuplot = True
        #self.updateImage()
        
    def isModified(self):
        self.canGnuplot = False
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
        if self.isChanged == True and self.is_imported == False:
            self.writeCSV()
        event.accept()

    def createToolBars(self):
        self.tb = self.addToolBar("Buttons")
        self.tb.setToolButtonStyle(2)
        self.tb.setMovable(False)
        self.tb.setFloatable(False)
        self.tb.setIconSize(QSize(16, 16))
        self.btnAdd = QAction(QIcon.fromTheme('add'), "neuer Eintrag", self,
                toolTip="neue Messung",
                triggered=self.insertNewRow)
        self.tb.addAction(self.btnAdd)
        self.btnRemove = QAction(QIcon.fromTheme('edit-delete'), "Zeile löschen", self,
                toolTip="Zeile löschen",
                triggered=self.removeRow)
        self.tb.addAction(self.btnRemove)
        self.tb.addSeparator()
        
        self.folderAct = QAction(QIcon.fromTheme('folder'), "", self,
                toolTip="Programmordner öffnen",
                triggered=self.openFolder)
        self.folderAct.setIconText("Programmordner öffnen")
        self.tb.addAction(self.folderAct)

        ### Import
        self.importAct = QAction(QIcon.fromTheme('document-open'), "", self,
                toolTip="CSV importieren",
                triggered=self.importCSV)
        self.importAct.setIconText("Import")
        self.tb.addAction(self.importAct)

        ### Export Zeitraum
        self.exportAct = QAction(QIcon.fromTheme('document-save-as'), "", self,
                toolTip="Zeitraum als CSV exportieren",
                triggered=self.exportCSV)
        self.exportAct.setIconText("Export")
        self.tb.addAction(self.exportAct)
        
        self.addToolBarBreak(Qt.TopToolBarArea)      
        self.tbd = self.addToolBar("Date")
        self.tbd.setMovable(False)
        self.tbd.setFloatable(False)
        self.tbd.setIconSize(QSize(16, 16))  
        self.tbd.addWidget(self.date_edit_start)
        self.tbd.addSeparator()
        self.tbd.addWidget(self.date_edit_end)
        self.tbd.addSeparator()
        ### externes Diagramm
        self.extern = QAction(QIcon("gnuplot_icon"), "", self, 
                                toolTip="externes Diagramm öffnen", 
                                triggered = self.callGnuplotExtern)    
        self.extern.setIconText("externes Diagramm öffnen")
        self.tbd.addAction(self.extern)
        ### internes Diagramm
        self.btnChart = QAction(QIcon("plot_icon"), "Diagramm anzeigen", self, 
                                toolTip="internes Diagramm anzeigen/ausblenden", 
                                triggered = self.toggleChart)
        self.tbd.addSeparator()
        self.btnChart.setIconText("Diagramm anzeigen")
        self.tbd.addAction(self.btnChart)  
        
        ### ComboBox Jahre
        self.btnYears = QComboBox()
        self.btnYears.setFixedWidth(80)
        self.btnYears.currentIndexChanged.connect(self.toggleYear)
        self.tbd.addWidget(self.btnYears)          

    def toggleYear(self):
        if self.tableview.rowCount() > 0 and self.btnYears.currentIndex() > 0:
            if self.btnYears.currentIndex() == self.btnYears.count() - 1:
                print("alle")
                for row in range(self.tableview.rowCount() - 1):
                    self.tableview.showRow(row)
                self.setDatesFromTable()
                self.callGnuplot()
            else:
                ed = f'{self.btnYears.currentText()}1231'
                sd = f'{self.btnYears.currentText()}0101'
                self.canGnuplot = False
                self.date_edit_start.setDate(QDate.fromString(sd, "yyyyMMdd"))
                self.date_edit_end.setDate(QDate.fromString(ed, "yyyyMMdd"))
                self.canGnuplot = True
                self.callGnuplot()
            self.tableview.scrollToTop()
  
    def toggleChart(self):
        if self.btnChart.text() == "Diagramm anzeigen":
            self.statusBar().show()
            self.btnChart.setText("Diagramm ausblenden")
            self.btnChart.setIcon(QIcon("plot_icon_dis"))
            self.updateImage()
        else:
            self.btnChart.setText("Diagramm anzeigen")
            self.statusBar().hide()
            self.btnChart.setIcon(QIcon("plot_icon"))
        
    def callGnuplot(self):
        #self.imgLabel.hide()
        if self.tableview.rowCount() > 0 and self.canGnuplot == True:
            liste = []
            for row in range(self.tableview.rowCount()):
                if int(self.tableview.item(row, 3).text()) >= int(self.start_date) \
                and int(self.tableview.item(row, 3).text()) <= int(self.end_date):
                    self.tableview.showRow(row)
                    tag = self.tableview.item(row, 3).text()
                    gew = self.tableview.item(row, 1).text()
                    liste.append(f"{tag}\t{gew}")
                else:
                    self.tableview.hideRow(row)
            temp_file = 'zeitraum.csv'
            gnuplot_file = 'preview_intern.gnuplot'
            with open(temp_file , 'w') as f:
                f.write('\n'.join(liste))
                f.close()
                
            cmd = "gnuplot"
            if run([cmd, gnuplot_file]):
                print("gnuplot intern finished")
                self.updateImage()
                
    def updateImage(self):
        print("update Image")
        myimage = QImage("messung_intern.png")
        if myimage.isNull():
            self.showMessage("Cannot load messung_intern.png")
            return
        else:
            self.imgLabel.setPixmap(QPixmap.fromImage(myimage))
            self.imgLabel.show()
    
    # externes Diagramm 
    def callGnuplotExtern(self):
        if self.tableview.rowCount() > 0 and self.canGnuplot == True:
            liste = []
            for row in range(self.tableview.rowCount()):
                if int(self.tableview.item(row, 3).text()) >= int(self.start_date) \
                and int(self.tableview.item(row, 3).text()) <= int(self.end_date):
                    self.tableview.showRow(row)
                    tag = self.tableview.item(row, 3).text()
                    gew = self.tableview.item(row, 1).text()
                    liste.append(f"{tag}\t{gew}")
                else:
                    self.tableview.hideRow(row)
            temp_file = 'zeitraum.csv'
            gnuplot_file = 'preview_extern.gnuplot'
            with open(temp_file , 'w') as f:
                f.write('\n'.join(liste))
                f.close()
                
            cmd = "gnuplot"
            run([cmd, "-p", gnuplot_file])

    def updateTable(self):
        for row in range(self.tableview.rowCount()):
            if int(self.tableview.item(row, 3).text()) >= int(self.start_date) \
            and int(self.tableview.item(row, 3).text()) <= int(self.end_date):
                self.tableview.showRow(row)
            else:
                self.tableview.hideRow(row)
        self.tableview.selectRow(0)
        self.callGnuplot()

    def openFolder(self):
        myfolder = path.dirname(sys.argv[0])
        QDesktopServices.openUrl(QUrl.fromLocalFile(myfolder))

    def createStatusBar(self):
        #self.statusBar().showMessage("Willkommen", 0)
        self.statusBar().addWidget(self.imgLabel)

    def loadCsvOnOpen(self):
        self.canGnuplot = False
        filename = self.myfile
        if QFile.exists(filename):
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
            self.isChanged = False
            ### Combobox füllen
            yearList = []
            for row in range(self.tableview.rowCount() - 1):
                yearList.append(self.tableview.item(row, 3).text()[:4])
            mylist = sorted(list(set(yearList)))
            self.btnYears.addItem("Jahre")
            self.btnYears.addItems(mylist)
            self.setDatesFromTable()
            self.btnYears.addItem("alles")

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

    def selectedRow(self):
        if self.tableview.selectionModel().hasSelection():
            row =  self.tableview.selectionModel().selectedIndexes()[0].row()
            return int(row)
            
    def insertNewRow(self):
        dlg = QInputDialog()
        last = self.tableview.item(self.tableview.rowCount() - 1, 1).text()
        syst, ok = dlg.getDouble(self, 'neuer Eintrag', "Gewicht", float(last))
        if ok:
            self.addRow(str(syst))

    def addRow(self, syst):
        row = self.tableview.rowCount()
        if row > 0:
            lastdate = self.tableview.item(self.tableview.rowCount() - 1, 0).text()
            self.tableview.insertRow(row)
            self.tableview.horizontalHeader().setStretchLastSection(True)
        
            column = 0
            print("lastdate: ", lastdate)
            d = QDate.fromString(lastdate, "dddd, dd.MMMM yyyy")
            dt = d.addDays(1)
            sqldate = dt.toString("yyyyMMdd")
            newItem = QTableWidgetItem(dt.toString("dddd, dd.MMMM yyyy"))
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
            newItem = QTableWidgetItem(sqldate)
            self.tableview.setItem(row,column, newItem)
            
            self.isChanged = True
            last = self.tableview.rowCount() - 1
            self.tableview.selectRow(last)
        else:
            self.tableview.setColumnCount(4)
            self.tableview.hideColumn(3)
            lastdate = QDate.currentDate().toString("dddd, dd.MMMM yyyy")
            self.tableview.insertRow(0)
            self.tableview.horizontalHeader().setStretchLastSection(True)
            newItem = QTableWidgetItem(QDate.currentDate().toString("dddd, dd.MMMM yyyy"))
            newItem.setTextAlignment(Qt.AlignRight)
            self.tableview.setItem(row,0, newItem)
            sqlItem = QTableWidgetItem(QDate.currentDate().toString("yyyyMMdd"))
            self.tableview.setItem(row,3, sqlItem)

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
        
    def exportCSV(self):
        daterange = f'{self.date_edit_start.text().replace(".", "_")}-{self.date_edit_end.text().replace(".", "_")}'
        filename = f"Gewicht_{daterange}"
        print(filename)
        exportfile, _ = QFileDialog.getSaveFileName(self, "Zeitraum speichern", f'QDir.homePath()/{filename}.csv',
                                                "CSV Dateien (*.csv)")
        if (exportfile != ""):
            with open(exportfile, 'w') as stream:
                print("saving", self.myfile)
                writer = csv.writer(stream, delimiter='\t')
                for row in range(self.tableview.rowCount()):
                    ### nur Zeilen die angezeigt werden
                    if int(self.tableview.item(row, 3).text()) >= int(self.start_date) \
                    and int(self.tableview.item(row, 3).text()) <= int(self.end_date):                   
                        rowdata = []
                        for column in range(self.tableview.columnCount()):
                            item = self.tableview.item(row, column)
                            if item is not None:
                                rowdata.append(item.text())
                            else:
                                rowdata.append('')
                        writer.writerow(rowdata)
            self.isChanged = False        
            
    def importCSV(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Import CSV", "","CSV Dateien (*.csv)")
        if filename:
            f = open(filename, 'r')
            self.tableview.setRowCount(0)
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
            self.isChanged = False
            self.is_imported = True
            self.setDatesFromTable()
            ### Combobox füllen
            yearList = []
            for row in range(self.tableview.rowCount() - 1):
                yearList.append(self.tableview.item(row, 3).text()[:4])
            mylist = sorted(list(set(yearList)))
            self.btnYears.addItem("Jahre")
            self.btnYears.addItems(mylist)
            self.btnYears.addItem("alles")
            #self.setDatesFromTable()
                
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
        QDateEdit
        {
            font-size: 8pt;
        }
    """

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    geo = app.desktop().screenGeometry()
    print(geo)
    mainWin = MainWindow()
    mainWin.setGeometry(0, 0, 900, geo.height() - 60)
    sys.exit(app.exec_())
