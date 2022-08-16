import csv
import os
import dpi
import sys
import re
import sqlite3
import xlrd
import requests
import time
from PyQt5.QtGui import QBrush, QTextCursor, QColor, QRegExpValidator, QIcon, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPoint, QRegExp, QAbstractTableModel
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from pytz import timezone
from jdatetime import datetime as dt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog, QDesktopWidget
from wasender import Ui_MainWindow
import icons_rc
from browserCtrl import Web


class Main():

    def __init__(self):
        super(Main, self).__init__()
        app = QApplication(sys.argv)
        self.__LICENS__ = True
        self.__VERSION__ = '1.0'
        self.cv = 0
        self.Net = None
        self.User = None

        self.insert = NetWork(version=self.__VERSION__)
        self.insert.start()
        # self.insert.Checker.connect(self.qthreadInsert)
        self.userChck()

        self.MainWindow = myQMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.center()

        font_db = QFontDatabase()
        font_db1 = QFontDatabase()
        font_db2 = QFontDatabase()
        font_id = font_db.addApplicationFont(r"fonts\african.ttf")
        font_db.applicationFontFamilies(font_id)
        font_id1 = font_db1.addApplicationFont(r"fonts\B Nazanin.ttf")
        font_db1.applicationFontFamilies(font_id1)
        font_id2 = font_db2.addApplicationFont(r"fonts\MesloLGS NF.ttf")
        font_db2.applicationFontFamilies(font_id2)

        if not os.path.exists('temp'):
            os.mkdir('temp')
        self.dbPath = r"./temp/temporary.data"
        self.reviewedCount = 0
        self.MainWindow.setWindowFlags(self.MainWindow.windowFlags() | Qt.FramelessWindowHint)
        self.MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.btn_close.clicked.connect(self.MainWindow.close)
        self.ui.btn_maxmin.clicked.connect(self.maxmin)
        self.ui.btn_min.clicked.connect(self.MainWindow.showMinimized)
        self.ui.btn_export.clicked.connect(self.export)
        self.ui.btn_gnarate.clicked.connect(self.generate)
        self.ui.btn_clear.clicked.connect(self.clearList)
        self.ui.btn_img.clicked.connect(self.selectIMG)
        self.ui.lb_version.setText(self.__VERSION__)
        regex = QRegExp("^(?!0+$)[0-9]+$")
        self.validator = QRegExpValidator(regex)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/main/icon.ico"), QIcon.Normal, QIcon.Off)
        self.MainWindow.setWindowIcon(icon)

        self.oldPos = self.MainWindow.pos()
        self.areaCode = self.ui.areaCode.text()
        self.RememberLogin = True
        self.ui.sleepMin.setValidator(self.validator)
        self.ui.sleepMin.setMaxLength(4)
        self.ui.sleepMax.setValidator(self.validator)
        self.ui.sleepMax.setMaxLength(4)
        self.p = ''
        self.ui.btn_import.clicked.connect(self.importer)
        self.ui.btn_acclist.clicked.connect(self.accountsList)
        self.ui.btn_start.clicked.connect(self.StarT)
        self.ui.btn_stop.clicked.connect(self.stop_progress)
        self.ui.LogBox.setReadOnly(True)
        self.ui.LogBox.setTextInteractionFlags(Qt.NoTextInteraction)  # non-selectable Text in QPlainTextEdit
        self.ui.lang.currentIndexChanged.connect(self.languageSet)
        self.language = self.ui.lang.currentText()
        self.languageSet()

        self.MainWindow.show()
        sys.exit(app.exec_())

    def languageSet(self):
        self.language = self.ui.lang.currentText()
        if self.language == 'EN':
            try:
                self.ui.btn_import.setText('Load')
                self.ui.btn_import.setToolTip('Loading numbered lists')
                self.ui.btn_gnarate.setText('Generator')
                self.ui.btn_gnarate.setToolTip('Created from a number range')
                self.ui.btn_export.setText('Export')
                self.ui.btn_export.setToolTip('Get output from program results')
                self.ui.btn_clear.setText('Clear')
                self.ui.btn_clear.setToolTip('Clear the list of numbers')
                self.ui.btn_acclist.setText('Accounts List')
                self.ui.btn_start.setText('Start')
                self.ui.btn_stop.setText('Stop')
                self.ui.whatsAppNumbers.setText('Numbers List')
                self.ui.label_count_txt.setText('Total')
                self.ui.label_count_txt_3.setText('Reviewed')
                self.ui.label_count_txt_4.setText('Successful')
                self.ui.label_count_txt_5.setText('Unsuccessful')
                self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(self.ui.tab_Analyz), 'Number analysis')
                self.ui.textBrowser.setText(
                    'You can use the number analysis feature to check your list of numbers to identify numbers that have WhatsApp accounts.')
                self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(self.ui.tab_msg), 'Text Message')
                self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(self.ui.tab_img), 'Image')
                self.ui.frame_LCD_label.setToolTip('Instant app review statistics')
                self.ui.frame_LCD.setToolTip('Instant app review statistics')
                self.ui.LogBox.setToolTip('Program activity report')
                self.ui.btn_start.setToolTip('Start the program')
                self.ui.btn_stop.setToolTip('Stop the program')
                self.ui.frame_msg.setToolTip('List of numbers that are checked in the program')
                self.ui.tab_Analyz.setToolTip('Number list analysis')
                self.ui.btn_close.setToolTip('Close the app')
                self.ui.btn_min.setToolTip('to make it least')
                self.ui.btn_maxmin.setToolTip('Application window mode')
                self.ui.label.setText('Text message')
                self.ui.textMSG.setToolTip('The text of your message to send')
                self.ui.label_2.setText('Interrupt time of each post between ')
                self.ui.label_3.setText('&')
                self.ui.label_4.setText('Seconds are set')
                self.ui.sleepMax.setToolTip('Most downtime')
                self.ui.sleepMin.setToolTip('Shortest downtime')
                self.ui.label_11.setText('Interrupt time of each post between ')
                self.ui.label_10.setText('&')
                self.ui.label_12.setText('Seconds are set')
                self.ui.sleepMax_I.setToolTip('Seconds are set')
                self.ui.sleepMin_I.setToolTip('Shortest downtime')
                self.ui.label_caption.setText('Enter your caption if needed:')
                self.ui.caption.setToolTip('Caption of your desired image')
                self.ui.btn_img.setText('Select image')
                self.ui.btn_img.setToolTip('Select an image to send')
                self.ui.tab_msg.setToolTip('Send text message')
                self.ui.tab_img.setToolTip('Send image')
                self.ui.areaCode.setToolTip('Your Country Area Code')
                self.ui.lang.setToolTip('Set the program language')
                self.fia.btn_importaccount.setToolTip('Select number to load')
                self.fia.btn_import_cancel.setToolTip(
                    'Cancelation of Number loading operations')
            except:
                pass
            try:
                self.fia.btn_addnewtel.setPlaceholderText('New Account Number')
                self.fia.btn_importaccount.setText('Add new account')
                self.fia.label_2.setText('List of saved accounts:')
                self.fia.btn_import_cancel.setText('Cancel')
            except:
                pass
            try:
                self.fi.label.setText('Upload phone number from file:')
                self.fi.btn_importFile.setText('Seect File')
                self.fi.btn_importFile.setToolTip('Select file to Loading')
                self.fi.label_2.setText('Manually enter phone number:')
                self.fi.btn_importManual.setText('loading')
                self.fi.btn_importManual.setToolTip('Loading entered numbers')
                self.fi.btn_import_cancel.setText('Cancel')
                self.fi.btn_import_cancel.setToolTip('Cancel number loading operation')
                self.fi.manualNumber.setToolTip('Enter your phone numbers and separate them with a line break (Enter)')
            except:
                pass
            try:
                self.frOM.label.setText('First issue:')
                self.frOM.label_2.setText('Number of creations:')
                self.frOM.generate_num.setToolTip('Enter your first desired number without 0')
                self.frOM.generate_count.setToolTip('Enter the number you want to create the list of numbers')
                font = QFont()
                font.setFamily("Arial")
                font.setPointSize(14)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.frOM.generate_num.setFont(font)
                self.frOM.generate_count.setFont(font)
                self.frOM.btn_g_ok.setText('Confirmation')
                self.frOM.btn_g_ok.setToolTip('Create list')
                self.frOM.btn_g_cancel.setText('Cancel')
                self.frOM.btn_g_cancel.setToolTip('Cancel operations')
            except:
                pass
        else:
            try:
                self.ui.retranslateUi(MainWindow=self.MainWindow)
            except:
                pass
            try:
                self.fia.retranslateUi(self.formQImport)
            except:
                pass
            try:
                self.fi.retranslateUi(self.formQImport1)
            except:
                pass
            try:
                self.frOM.retranslateUi(self.generateForm)
            except:
                pass

    def userChck(self):
        try:
            self.userStatus = NetWork(step=2, user=self.__LICENS__)
            self.userStatus.start()
            self.userStatus.Checker.connect(self.userChecker)
        except Exception as e:
            print(e)

    def checkVer(self, value):
        try:
            if value[0] != "last version":
                ver = value[0]
                link = value[1]
                self.msgError(
                    f"""<html><head/><body><p align="center">نسخه جدید ({ver}) برنامه در دسترس است</p><p align="center">لطفا آن را <a href="{link}"><span style=" text-decoration: underline; color:#0000ff;">دانلود</span></a> و نصب کنید</p></body></html>""",
                    colorf="#034a0d")
        except:
            pass

    def maxmin(self):
        if self.ui.btn_maxmin.text() == '类':
            self.MainWindow.showMaximized()
            self.ui.btn_maxmin.setText('缾')
        elif self.ui.btn_maxmin.text() == '缾':
            self.MainWindow.setWindowState(Qt.WindowNoState)
            self.ui.btn_maxmin.setText('类')

    def showNumberList(self, commandSQL, focus=0):
        try:
            QApplication.processEvents()
            global db
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.dbPath)
            db.open()
            # projectModel = QSqlQueryModel()
            self.projectModel = ColorfullSqlQueryModel()
            self.projectModel.setQuery(commandSQL, db)
            if self.language == 'EN':
                tel = 'Number'
                st = 'Status'
                ress = 'Result'
            else:
                tel = 'شماره'
                st = 'وضعیت'
                ress = 'نتیجه'
            self.projectModel.setHeaderData(0, Qt.Horizontal, tel)
            self.projectModel.setHeaderData(1, Qt.Horizontal, st)
            self.projectModel.setHeaderData(2, Qt.Horizontal, ress)
            self.ui.tableview_numbers.setModel(self.projectModel)
            self.rowCount = self.projectModel.rowCount()
            # self.tableResult = projectModel
            red = []
            green = []
            for i in range(self.rowCount):
                res = self.projectModel.record(i).value("res")
                if res == '☑':
                    green.append(i)
                elif res == '☒':
                    red.append(i)
            self.projectModel.setRowsToBeColored(red=red, green=green)
            if focus != 0:
                self.index = self.projectModel.index(focus, 2)
                if (self.index.isValid()):
                    self.ui.tableview_numbers.scrollTo(self.index)
                    self.ui.tableview_numbers.selectRow(focus)
                    print("scroll")
            QApplication.processEvents()
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
                errormsg = e.message
            else:
                print(e)
                errormsg = e
            self.msgError(infor=errormsg)

    def Time(self):
        tz = timezone('Asia/Tehran')
        timeZ = dt.now(tz)
        # last_time = int(time.time())   ## now timestamp
        timeZ = timeZ.strftime("%Y%m%d%H%M%S")
        return timeZ

    def ListLoader(self, path):
        self.ui.btn_export.setEnabled(False)
        if path:
            NUMBERS = []
            type = path.split('.')[-1]
            if type == 'csv':
                with open(path, 'r+') as csvF:
                    numbers = csv.reader(csvF)
                    for number in numbers:
                        for num in number:
                            try:
                                self.areaCode = int(self.ui.areaCode.text())
                            except:
                                pass
                            try:
                                n = int(num)
                                if len(str(num)) >= 9:
                                    s98 = re.compile(fr"^{self.areaCode}", re.I)
                                    s0 = re.compile('^0', re.I)
                                    if s98.search(num):
                                        pass
                                    elif s0.search(num):
                                        num = re.sub('^0', fr"{self.areaCode}", num)
                                    else:
                                        num = fr"{self.areaCode}{num}"
                                    n = int(num)
                                    NUMBERS.append(n)
                            except:
                                continue
            elif type == 'xlsx' or type == 'xls':
                try:
                    xlrd.xlsx.ensure_elementtree_imported(False, None)
                    xlrd.xlsx.Element_has_iter = True
                except:
                    pass
                wb = xlrd.open_workbook(path)
                sheet = wb.sheet_by_index(0)
                for c in range(sheet.ncols):
                    for r in range(sheet.nrows):
                        nume = sheet.cell_value(r, c)
                        try:
                            self.areaCode = int(self.ui.areaCode.text())
                        except:
                            pass
                        try:
                            num = str(int(nume))
                            if len(str(num)) >= 9:
                                s98 = re.compile(fr"^{self.areaCode}", re.I)
                                s0 = re.compile('^0', re.I)
                                if s98.search(num):
                                    pass
                                elif s0.search(num):
                                    num = re.sub('^0', fr"{self.areaCode}", num)
                                else:
                                    num = fr"{self.areaCode}{num}"
                                n = int(num)
                                NUMBERS.append(n)
                        except:
                            continue
            NUMBERS = set(NUMBERS)
            self.ui.lcdNumber_allCount.display(len(NUMBERS))
            try:
                global TableNow
                try:
                    with sqlite3.connect(f"{self.dbPath}") as dbi:
                        print("Connected to Database")
                        TableNow = self.Time()
                        table = f"CREATE TABLE IF NOT EXISTS `{TableNow}` (num INT PRIMARY KEY NOT NULL, status VARCHAR(50), res VARCHAR(12))"
                        dbi.execute(table)
                        print("Table OK")
                        i = 1
                        for num in NUMBERS:
                            insert = f"INSERT INTO `{TableNow}` (num,status) VALUES ('{num}','')"
                            dbi.execute(insert)
                            i += 1
                        dbi.commit()
                except:
                    try:
                        db.close()
                    except:
                        print("error db")
                    try:
                        dbi.close()
                    except:
                        print("error dbi")
                    os.remove(self.dbPath)
                    with sqlite3.connect(f"{self.dbPath}") as dbi:
                        print("Connected to Database")
                        TableNow = self.Time()
                        table = f"CREATE TABLE IF NOT EXISTS `{TableNow}` (num INT PRIMARY KEY NOT NULL, status VARCHAR(50), res VARCHAR(12))"
                        dbi.execute(table)
                        print("Table OK")
                        i = 1
                        for num in NUMBERS:
                            insert = f"INSERT INTO `{TableNow}` (num,status) VALUES ('{num}','')"
                            dbi.execute(insert)
                            i += 1
                        dbi.commit()
                self.ui.LogBox.clear()
                self.ui.LogBox.appendPlainText("--- Numbers entered successfully ---")
                self.showNumberList(commandSQL=f"select * from `{TableNow}`")
                self.ui.btn_clear.setEnabled(True)
            except:
                if self.language == 'EN':
                    msg = "Error loading numbers! \nTry again"
                else:
                    msg = "ارور در بارگذاری شماره ها !\nمجدد تلاش کنید"
                self.msgError(msg)
            try:
                dbi.close()
            except:
                pass
        else:
            print("Not Selected File!")
            pass

    def msgError(self, errorText='مشکلی پیش آمده است !!!', icon='', colorf="#ff0000"):
        box = QMessageBox()
        if icon == '':
            box.setIcon(QMessageBox.Warning)
        else:
            box.setIcon(QMessageBox.Information)
        box.setWindowTitle('ارور')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/main/icon.ico"), QIcon.Normal, QIcon.Off)
        box.setWindowIcon(icon)
        box.setText(errorText)
        box.setStandardButtons(QMessageBox.Yes)
        buttonY = box.button(QMessageBox.Yes)
        if self.language == 'EN':
            tx = "       OK       "
        else:
            tx = "       تایید       "
        buttonY.setText(tx)
        box.setStyleSheet("""QMessageBox{\n
                          background-color:    #d9c9a3    ;\n
                          border: 3px solid   #ff0000  ;\n
                          border-radius:5px;\n
                          }\n
                          QLabel{\n
                          color:   %s  ;\n
                          font: 13pt \"B Nazanin\";\n
                          font-weight: bold;\n
                          border:no;\n
                          }\n
                          \n
                          QPushButton:hover:!pressed\n
                          {\n
                            border: 2px dashed rgb(255, 85, 255);\n
                              background-color:  #e4e7bb ;\n
                              color:  #9804ff ;\n
                          }\n
                          QPushButton{\n
                          background-color:  #a2fdc1 ;\n
                          font: 12pt \"B Nazanin\";\n
                          font-weight: bold;\n
                              color:  #ff0000 ;\n
                          border: 2px solid  #8b00ff ;\n
                          border-radius: 8px;\n
                          }""" % colorf)
        box.setWindowFlags(box.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        box.exec_()

    def lcdNumber_reviewed(self, counter):
        self.reviewedCount = counter
        if not self.stopProgress:
            self.ui.lcdNumber_reviewed.display(counter)

    def lcdNumber_wa(self, value):
        if not self.stopProgress:
            self.ui.lcdNumber_wa.display(value)

    def lcdNumber_nwa(self, value):
        if not self.stopProgress:
            self.ui.lcdNumber_nwa.display(value)

    def programLog(self, log):
        if not self.stopProgress:
            self.ui.LogBox.appendPlainText(log)
            self.ui.LogBox.moveCursor(QTextCursor.End)

    def waINS(self, number):
        print(number)
        if db.open():
            query = QSqlQuery()
            if self.ui.start_tab.currentIndex() == 0:
                query.exec_(f"update `{TableNow}` set status = '✓', res = '☑' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 1:
                query.exec_(f"update `{TableNow}` set status = '✓✓', res = '☑' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 2:
                query.exec_(f"update `{TableNow}` set status = '✓✓✓', res = '☑' where num = '{number}'")
            self.showNumberList(commandSQL=f"select * from `{TableNow}`", focus=self.reviewedCount)
        else:
            print("wa Db Not Open")

    def nwaINS(self, number):
        print(number)
        if db.open():
            query = QSqlQuery()
            if self.ui.start_tab.currentIndex() == 0:
                query.exec_(f"update `{TableNow}` set status = '✓', res = '☒' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 1:
                query.exec_(f"update `{TableNow}` set status = '✓✓', res = '☒' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 2:
                query.exec_(f"update `{TableNow}` set status = '✓✓✓', res = '☒' where num = '{number}'")
            self.showNumberList(commandSQL=f"select * from `{TableNow}`", focus=self.reviewedCount)
        else:
            print("nwa Db Not Open")

    def EndWork(self, msg=''):
        if not self.stopProgress:
            self.ui.btn_start.setEnabled(True)
            self.ui.btn_stop.setEnabled(False)
            self.ui.btn_import.setEnabled(True)
            self.ui.btn_gnarate.setEnabled(True)
            self.ui.start_tab.setEnabled(True)
            self.ui.btn_export.setEnabled(True)
            self.ui.btn_clear.setEnabled(True)
            try:
                self.ui.LogBox.appendPlainText(msg)
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                    errormsg = e.message
                else:
                    print(e)
                    errormsg = e
                self.msgError(f"{errormsg}")

    def stop_progress(self):
        print("stop")
        self.EndWork()
        self.stopProgress = True
        entText = "-- Stop running --"
        self.ui.LogBox.appendPlainText(entText)
        try:
            if self.ui.start_tab.currentIndex() == 0:
                self.AnalyzThread.stop()
            elif self.ui.start_tab.currentIndex() == 1:
                self.MsgThread.stop()
            elif self.ui.start_tab.currentIndex() == 2:
                self.ImgThread.stop()
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
                errormsg = e.message
            else:
                print(e)
                errormsg = e
            self.msgError(f"{errormsg}")

    def AnalyzNum(self):
        try:
            if db.open():
                # QApplication.processEvents()
                print("Analyz OK")
                query = QSqlQuery()
                query.exec_(f"select * from `{TableNow}` where status = ''")
                numList = []
                while query.next():
                    num = query.value(0)
                    numList.append(num)
                self.AnalyzThread = Web(counter_start=0, step='A', numList=numList, Remember=self.RememberLogin)
                self.AnalyzThread.start()
                self.AnalyzThread.lcdNumber_reviewed.connect(self.lcdNumber_reviewed)
                self.AnalyzThread.lcdNumber_wa.connect(self.lcdNumber_wa)
                self.AnalyzThread.lcdNumber_nwa.connect(self.lcdNumber_nwa)
                self.AnalyzThread.Log.connect(self.programLog)
                self.AnalyzThread.wa.connect(self.waINS)
                self.AnalyzThread.nwa.connect(self.nwaINS)
                self.AnalyzThread.EndWork.connect(self.EndWork)
                self.stopProgress = False
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            if self.language == 'EN':
                msg = "Error in number analysis"
            else:
                msg = "خطا در آنالیز شماره ها"
            self.msgError(msg)

    def sendMsg(self, text):
        try:
            if db.open():
                # QApplication.processEvents()
                query = QSqlQuery()
                query.exec_(f"select * from `{TableNow}` where status = '' or res = '☑'")
                numList = []
                while query.next():
                    num = query.value(0)
                    numList.append(num)
                sleepMin = self.ui.sleepMin.text()
                sleepMax = self.ui.sleepMax.text()
                if sleepMin != '':
                    sleepMin = int(sleepMin)
                else:
                    sleepMin = 3
                if sleepMax != '':
                    sleepMax = int(sleepMax)
                else:
                    sleepMax = 6
                self.MsgThread = Web(counter_start=0, step='M', numList=numList, sleepMin=sleepMin, sleepMax=sleepMax,
                                     text=text, Remember=self.RememberLogin)
                self.MsgThread.start()
                self.MsgThread.lcdNumber_reviewed.connect(self.lcdNumber_reviewed)
                self.MsgThread.lcdNumber_wa.connect(self.lcdNumber_wa)
                self.MsgThread.lcdNumber_nwa.connect(self.lcdNumber_nwa)
                self.MsgThread.Log.connect(self.programLog)
                self.MsgThread.wa.connect(self.waINS)
                self.MsgThread.nwa.connect(self.nwaINS)
                self.MsgThread.EndWork.connect(self.EndWork)
                self.stopProgress = False
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            if self.language == 'EN':
                msg = "Error sending text message!"
            else:
                msg = "خطا در ارسال پیام متنی !"
            self.msgError(msg)

    def sendImg(self, path, caption=''):
        try:
            if db.open():
                # QApplication.processEvents()
                query = QSqlQuery()
                query.exec_(f"select * from `{TableNow}` where status = '' or res = '☑'")
                numList = []
                while query.next():
                    num = query.value(0)
                    numList.append(num)
                sleepMin = self.ui.sleepMin_I.text()
                sleepMax = self.ui.sleepMax_I.text()
                if sleepMin != '':
                    sleepMin = int(sleepMin)
                else:
                    sleepMin = 3
                if sleepMax != '':
                    sleepMax = int(sleepMax)
                else:
                    sleepMax = 6
                self.ImgThread = Web(counter_start=0, step='I', numList=numList, sleepMin=sleepMin, sleepMax=sleepMax,
                                     text=caption, path=path, Remember=self.RememberLogin)
                self.ImgThread.start()
                self.ImgThread.lcdNumber_reviewed.connect(self.lcdNumber_reviewed)
                self.ImgThread.lcdNumber_wa.connect(self.lcdNumber_wa)
                self.ImgThread.lcdNumber_nwa.connect(self.lcdNumber_nwa)
                self.ImgThread.Log.connect(self.programLog)
                self.ImgThread.wa.connect(self.waINS)
                self.ImgThread.nwa.connect(self.nwaINS)
                self.ImgThread.EndWork.connect(self.EndWork)
                self.stopProgress = False
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            if self.language == 'EN':
                msg = "Error sending image!"
            else:
                msg = "خطا در ارسال تصویر !"
            self.msgError(msg)

    def btnStatus(self, status='l'):
        '''
        disable or enable btns after strat app work
        '''
        if status == 'l':
            self.ui.lcdNumber_nwa.display(0)
            self.ui.lcdNumber_wa.display(0)
            self.ui.lcdNumber_reviewed.display(0)
            self.ui.LogBox.clear()
            self.ui.btn_start.setEnabled(False)
            self.ui.btn_stop.setEnabled(True)
            self.ui.btn_import.setEnabled(False)
            self.ui.btn_clear.setEnabled(False)
            self.ui.btn_gnarate.setEnabled(False)
            self.ui.start_tab.setEnabled(False)

    def userChecker(self, value):
        print(f"user {value}")
        self.User = value
        return self.User

    def qthreadInsert(self, value):
        try:
            self.insert.stop()
        except:
            pass

    def StarT(self):
        try:
            self.userChck()
        except:
            pass
        # self.RememberLogin = self.ui.RememberLoginStatus.isChecked()
        self.RememberLogin = True
        self.RememberLogin = True
        print("Start")
        Net = self.ConnectionCheck()
        try:
            print(Net, self.User)
            if db.open():
                if Net:
                    if self.ui.areaCode.text() != '':
                        if self.User:
                            currentIndex = self.ui.start_tab.currentIndex()
                            if currentIndex == 0:
                                self.btnStatus()
                                self.ui.LogBox.appendPlainText(f"-- Start analysis --")
                                self.AnalyzNum()
                            elif currentIndex == 1:
                                print("message Tab")
                                text = self.ui.textMSG.toPlainText()
                                print(text)
                                if text != '':
                                    self.btnStatus()
                                    self.ui.LogBox.appendPlainText(f"-- Start Send Message --")
                                    self.sendMsg(text)
                                else:
                                    if self.language == 'EN':
                                        msg = "Enter the text of your message first"
                                    else:
                                        msg = "ابتدا متن پیام خود را وارد کنید"
                                    self.msgError(msg)
                            elif currentIndex == 2:
                                print('image tab')
                                if self.p != '':
                                    caption = self.ui.caption.toPlainText()
                                    self.ui.LogBox.appendPlainText(f"-- Start Send Image --")
                                    self.sendImg(path=self.p, caption=caption)
                                    self.btnStatus()
                                else:
                                    if self.language == 'EN':
                                        msg = "First select your image to send"
                                    else:
                                        msg = "ابتدا تصویر خود را برای ارسال انتحاب کنید"
                                    self.msgError(msg)
                            else:
                                self.msgError()
                            if not self.RememberLogin:
                                lisT = os.listdir('temp')
                                import shutil
                                for f in lisT:
                                    try:
                                        if f == 'temporary.data':
                                            continue
                                        os.remove(f"temp/{f}")
                                    except:
                                        try:
                                            os.rmdir(f"temp/{f}")
                                        except:
                                            shutil.rmtree(f"temp/{f}")
                                            continue
                                        continue
                        else:
                            if self.language == 'EN':
                                msg = "You do not have permission to use the app!"
                            else:
                                msg = "شما مجوز استفاده از برنامه را ندارید!"
                            self.msgError(msg, colorf='#1b6900')
                    else:
                        if self.language == 'EN':
                            msg = "Please enter your country code"
                        else:
                            msg = "لطفا کد کشور خود را وارد کنید"
                        self.msgError(msg, colorf=' #ff3a0f ')
                else:
                    if self.language == 'EN':
                        msg = "You are not connected to the Internet! \nMake sure you are connected to the Internet."
                    else:
                        msg = "شما به اینترنت متصل نمی باشید!\nاز اتصال خود به اینترنت اطمینان حاصل فرمایید."
                    self.msgError(msg)
        except:
            if self.language == 'EN':
                msg = "First, load your list of numbers."
            else:
                msg = "ابتدا لیست شماره های خود را بارگذاری کنید."
            self.msgError(msg)

    def export(self):
        try:
            if db.open():
                DeskTop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                appName = self.ui.label_appName.text()
                if not os.path.isdir(f'{DeskTop}/{appName}'):
                    os.mkdir(f'{DeskTop}/{appName}')
                query = QSqlQuery()
                query.exec_(f"select * from `{TableNow}`")
                while query.next():
                    number = query.value(0)
                    status = query.value(1)
                    res = query.value(2)
                    FileName = "Export-"
                    if status == '✓':
                        FileName = 'Analyz-'
                    elif status == '✓✓':
                        FileName = 'SentMSG-'
                    elif status == '✓✓✓':
                        FileName = 'SentIMG-'
                    else:
                        continue
                    if res == '☑':
                        with open(fr"{DeskTop}\{appName}\{FileName}{TableNow}.csv", 'a+', encoding='utf8') as cSv:
                            writer = csv.writer(cSv, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,
                                                lineterminator='\n')
                            writer.writerow([f"{number}"])
                            # cSv.write(f"{number}\n")
                if self.language == 'EN':
                    msg = "Data extraction was successful."
                else:
                    msg = "استخراج اطلاعات با موفقیت انجام شد."
                self.msgError(errorText=msg, icon='Information', colorf="#214917")
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
                errormsg = e.message
            else:
                print(e)
                errormsg = e
            if self.language == 'EN':
                msg = "Could not find item to extract from list."
            else:
                msg = "موردی برای استخراج از لیست یافت نشد"
            self.msgError(msg)

    def generate(self):
        if self.ui.areaCode.text() != '':
            print("generate")
            from generate import Ui_Form
            self.frOM = Ui_Form()
            self.generateForm = QDialog()
            self.generateForm.setModal(True)
            self.generateForm.setWindowFlags(self.generateForm.windowFlags() | Qt.FramelessWindowHint)
            self.generateForm.setAttribute(Qt.WA_TranslucentBackground)
            icon = QIcon()
            icon.addPixmap(QPixmap(":/main/icon.ico"), QIcon.Normal, QIcon.Off)
            self.generateForm.setWindowIcon(icon)
            self.frOM.setupUi(self.generateForm)
            self.frOM.generate_num.setValidator(self.validator)
            self.frOM.generate_num.setMaxLength(10)
            self.frOM.generate_count.setValidator(self.validator)
            self.frOM.generate_count.setMaxLength(5)
            self.frOM.btn_g_ok.setFocus()
            self.languageSet()
            self.generateForm.show()
            self.frOM.btn_g_cancel.clicked.connect(self.generateForm.close)
            self.frOM.btn_g_ok.clicked.connect(self.importGenerate)
        else:
            if self.language == 'EN':
                msg = "Please enter your country code"
            else:
                msg = "لطفا کد کشور خود را وارد کنید"
            self.msgError(msg, colorf=' #ff3a0f ')

    def importGenerate(self):
        firstNumber = self.frOM.generate_num.text()
        RangeNum = self.frOM.generate_count.text()
        if RangeNum == '':
            RangeNum = 10
        if firstNumber != '':
            if not len(firstNumber) < 10:
                path = f"temp\generate-{self.Time()}.csv"
                print(firstNumber, path)
                for i in range(int(RangeNum)):
                    with open(f"{path}", 'a+') as g:
                        writer = csv.writer(g, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,
                                            lineterminator='\n')
                        writer.writerow([f"{firstNumber}"])
                    firstNumber = int(firstNumber) + 1
                    # print(firstNumber)
                self.generateForm.close()
                self.ListLoader(path)
                if self.language == 'EN':
                    msg = "List created successfully."
                else:
                    msg = "لیست با موفقیت ایجاد شد."
                self.msgError(errorText=msg, icon='Information', colorf="#214917")
                os.remove(path)
            else:
                if self.language == 'EN':
                    msg = "The first number must be 10 digits"
                else:
                    msg = "اولین شماره باید 10 رقم باشد"
                self.msgError(msg)
        else:
            if self.language == 'EN':
                msg = "You must enter the first number you want."
            else:
                msg = "باید اولین شماره مورد نظر خود را وارد کنید."
            self.msgError(msg)

    def importer(self):
        if self.ui.areaCode.text() != '':
            print("import")
            if self.cv == 0:
                self.cv = 1
                self.checkVERSION = NetWork(step=1, version=self.__VERSION__)
                self.checkVERSION.start()
                self.checkVERSION.cuurentVersion.connect(self.checkVer)
            from importNumber import Ui_Form
            self.fi = Ui_Form()
            self.formQImport1 = QDialog()
            self.formQImport1.setModal(True)
            self.formQImport1.setWindowFlags(self.formQImport1.windowFlags() | Qt.FramelessWindowHint)
            self.formQImport1.setAttribute(Qt.WA_TranslucentBackground)
            self.fi.setupUi(self.formQImport1)
            icon = QIcon()
            icon.addPixmap(QPixmap(":/main/icon.ico"), QIcon.Normal, QIcon.Off)
            self.formQImport1.setWindowIcon(icon)
            self.fi.btn_import_cancel.clicked.connect(self.formQImport1.close)
            self.fi.btn_importFile.clicked.connect(self.btn_import)
            self.fi.btn_importManual.clicked.connect(self.importManual)
            self.languageSet()
            self.formQImport1.show()
        else:
            if self.language == 'EN':
                msg = "Please enter your country code"
            else:
                msg = "لطفا کد کشور خود را وارد کنید"
            self.msgError(msg, colorf=' #ff3a0f ')

    def btn_import(self):
        options = QFileDialog.Options()
        UserDesk = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        num_path, _ = QFileDialog.getOpenFileName(caption="", directory=UserDesk,
                                                  filter="Excel Files (*.xlsx | *.xls | *.csv)", options=options)
        try:
            if num_path:
                self.formQImport1.close()
        except:
            pass
        self.ListLoader(num_path)

    def importManual(self):
        nums = self.fi.manualNumber.toPlainText()
        if nums != '':
            try:
                numLine = nums.split('\n')
                numLine = set(numLine)
                print(numLine)
                path = f"temp\manualNumber-{self.Time()}.csv"
                for num in numLine:
                    if num == '':
                        continue
                    num = int(num)
                    with open(f"{path}", 'a+') as g:
                        writer = csv.writer(g, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,
                                            lineterminator='\n')
                        writer.writerow([f"{num}"])
                self.formQImport1.close()
                self.ListLoader(path)
                if self.language == 'EN':
                    msg = "List loaded successfully."
                else:
                    msg = "لیست با موفقیت بارگذاری شد."
                self.msgError(errorText=msg, icon='Information', colorf="#214917")
                os.remove(path)
            except:
                if self.language == 'EN':
                    msg = "Error entering phone number! \nPlease make sure the numbers are entered correctly."
                else:
                    msg = 'خطا در ورود شماره تلفن!\nلطفا در نحوه صحیح ورود شماره ها دقت کنید.'
                self.msgError(msg)
        else:
            if self.language == 'EN':
                msg = "You must select the desired phone number, or enter it manually."
            else:
                msg = 'باید شماره تلفن های مورد نظر خود را انتخاب، یا دستی وارد کنید.'
            self.msgError(msg)

    def accountsList(self):
        '''
        Qwidget accounst list show
        '''
        from accuonts import Ui_Form
        self.fia = Ui_Form()
        self.formQImport = QDialog()
        self.formQImport.setModal(True)
        self.formQImport.setWindowFlags(self.formQImport.windowFlags() | Qt.FramelessWindowHint)
        self.formQImport.setAttribute(Qt.WA_TranslucentBackground)
        self.fia.setupUi(self.formQImport)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/main/icon.ico"), QIcon.Normal, QIcon.Off)
        self.formQImport.setWindowIcon(icon)
        self.fia.btn_import_cancel.clicked.connect(self.formQImport.close)
        self.fia.btn_importaccount.clicked.connect(self.addAccounts)
        try:
            if not os.path.exists('./temp/cache'):
                os.makedirs('temp/cache/')
        except:
            os.makedirs('./temp/cache/')
        cacheList = os.listdir('temp/cache/')
        print(cacheList)
        self.modelAcc = TableModel(cacheList)
        self.fia.accountsTable.setModel(self.modelAcc)
        # self.rowCount = self.modelAcc.rowCount()
        self.fia.btn_importaccount.setEnabled(False)
        self.languageSet()
        self.formQImport.show()

    def addAccounts(self):
        '''
        Add new account to my account list , with get text account name from user
        '''
        newaccountName = self.fia.btn_addnewtel.text()
        if newaccountName != '':
            self.addAccount = Web(step='Add', path=newaccountName, Remember=True)
            self.addAccount.start()
        else:
            if self.language == 'EN':
                msg = "Please enter your new account number to save."
            else:
                msg = "لطفا شماره اکانت جدید خود را برای ذخیره وارد کنید."
            self.msgError(msg)

    def clearList(self):
        try:
            print("table reset")
            self.projectModel.deleteLater()
        except:
            pass

    def selectIMG(self):
        options = QFileDialog.Options()
        UserDesk = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        img_path, _ = QFileDialog.getOpenFileName(caption="", directory=UserDesk,
                                                  filter="Image Files (*.jpg | *.jpeg | *.png)", options=options)
        self.p = img_path
        try:
            if img_path:
                print(img_path)
                imgName = img_path.split('/')[-1]
                img = QPixmap(img_path)
                img1 = img.scaled(120, 120, Qt.KeepAspectRatio)
                self.ui.imgShow.setPixmap(img1)
                self.ui.imgName.setText(imgName)
        except:
            pass

    def ConnectionCheck(self, url='https://py.pord.ir/ip/', timeout=5):
        try:
            req = requests.get(url, timeout=timeout)
            req.raise_for_status()
            return True
        except requests.HTTPError as e:
            print("Checking internet connection failed, status code {0}.".format(
                e.response.status_code))
            return False
        except requests.ConnectionError:
            print("No internet connection available.")
            return False


class myQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class LoadingText(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(LoadingText, self).__init__(parent)
        self.setWindowTitle("Loading...")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setStyleSheet('''QLabel{color:#ff0000;}''')
        self.time_to_wait = timeout
        self.setText("wait (closing automatically in {0} secondes.)".format(timeout))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.time_to_wait -= 1
        self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


class ColorfullSqlQueryModel(QSqlQueryModel):
    def __init__(self, dbcursor=None):
        super(ColorfullSqlQueryModel, self).__init__()
        self.red = []
        self.green = []

    def setRowsToBeColored(self, red=None, green=None):
        if red != None:
            self.red = red
        if green != None:
            self.green = green

    def data(self, index, role):
        row = index.row()
        if role == Qt.BackgroundRole and row in self.red:
            return QBrush(QColor('#FC500B'))
        if role == Qt.BackgroundRole and row in self.green:
            return QBrush(QColor('#AEF77E'))
        return QSqlQueryModel.data(self, index, role)


class NetWork(QThread):
    cuurentVersion = pyqtSignal(object)
    Checker = pyqtSignal(bool)

    def __init__(self, parent=None, step=0, version=None, user=None, pw=0):
        super(NetWork, self).__init__(parent)
        self.version = version
        self.step = step
        self.user = user
        self.pw = pw

    def Time(self):
        tz = timezone('Asia/Tehran')
        timeZ = dt.now(tz)
        # last_time = int(time.time())   ## now timestamp
        timeZ = timeZ.strftime("%Y%m%d%H%M%S")
        return timeZ

    def STATUS(self, user=None, pw=0):
        print('check user')
        self.Checker.emit(True)
        return ''

    def insertMember(self, version):
        pass

    def run(self):
        if self.step == 0:
            self.insertMember(self.version)
        elif self.step == 1:
            pass
            # self.checkVersion(self.version)
        elif self.step == 2:
            self.STATUS(user=self.user, pw=self.pw)

    def stop(self):
        print('terminate thread')
        self.terminate()


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 1

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            return "*"


if __name__ == '__main__':
    run = Main()
    # from multiprocessing import Process
    # p1 = Process(target=Main)
    # srv = NetWork()
    # p2 =Process(target=srv.insertMember,args=('1.0',))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
