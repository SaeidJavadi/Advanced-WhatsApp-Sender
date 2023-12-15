import csv
import os
import sys
import re
import sqlite3
import xlrd
import requests
import time
import json
from PyQt5.QtGui import QBrush, QTextCursor, QColor, QRegExpValidator, QIcon, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPoint, QRegExp, QAbstractTableModel
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from pytz import timezone
from jdatetime import datetime as dt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog, QDesktopWidget
from wasender import Ui_MainWindow
import icons_rc
from browserCtrl import Web
import logging
import logging.config
from logging.handlers import SocketHandler
import pythonjsonlogger.jsonlogger
from src import dpi
from src import logcolor

# config
if not os.path.exists(fr'.\src\logs'):
    os.mkdir(fr'.\src\logs')
logging.config.fileConfig(fr"src\logging.ini", disable_existing_loggers=True)
log = logging.getLogger(__name__)
try:
    socket_handler = SocketHandler("127.0.0.1", 19996)
except:
    pass
log.addHandler(socket_handler)
# config ends


class Main():

    def __init__(self):
        super(Main, self).__init__()
        app = QApplication(sys.argv)
        self.__LICENS__ = True
        self.__VERSION__ = '1.0'
        self.cv = 0
        self.Net = None
        self.User = True
        log.info(fr"===== Program Runing {self.__VERSION__} =====")
        self.insert = NetWork(version=self.__VERSION__)
        self.insert.start()
        # self.insert.Checker.connect(self.qthreadInsert)
        self.userChck()

        self.MainWindow = myQMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.center()
        font_db2 = QFontDatabase()
        font_id2 = font_db2.addApplicationFont(r"fonts\MesloLGS NF.ttf")
        font_db2.applicationFontFamilies(font_id2)
        with open("./src/lang/translations.json", encoding="utf8") as f:
            self.lang = json.load(f)
        self.ln = self.lang["translatables"]
        self.languageConf()
        self.cln = self.ui.langs.currentText()   # current language
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
        # forms init
        self.initGenerate()
        self.initImport()
        self.initAccountList()

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
        self.ui.langs.currentIndexChanged.connect(self.languageSet)
        self.languageSet()

        self.MainWindow.show()
        sys.exit(app.exec_())

    def languageConf(self):
        self.ui.langs.clear()
        for i, l in enumerate(self.lang["languages"]):
            self.ui.langs.addItem("")
            self.ui.langs.setItemText(i, l)
            if i == 0:
                self.ui.langs.setCurrentIndex(i)

    def languageSet(self):
        self.cln = self.ui.langs.currentText()
        log.debug(fr"change language to `{self.cln}`")
        try:
            self.ui.btn_import.setText(self.ln["btn_import"][self.cln])
            self.ui.btn_import.setToolTip(self.ln["btn_import_ttp"][self.cln])
            self.ui.btn_gnarate.setText(self.ln["btn_gnarate"][self.cln])
            self.ui.btn_gnarate.setToolTip(self.ln["btn_gnarate_ttp"][self.cln])
            self.ui.btn_export.setText(self.ln["btn_export"][self.cln])
            self.ui.btn_export.setToolTip(self.ln["btn_export_ttp"][self.cln])
            self.ui.btn_clear.setText(self.ln["btn_clear"][self.cln])
            self.ui.btn_clear.setToolTip(self.ln["btn_clear_ttp"][self.cln])
            self.ui.btn_acclist.setText(self.ln["btn_acclist"][self.cln])
            self.ui.btn_acclist.setToolTip(self.ln["btn_acclist_ttp"][self.cln])
            self.ui.btn_start.setText(self.ln["btn_start"][self.cln])
            self.ui.btn_start.setToolTip(self.ln["btn_start_ttp"][self.cln])
            self.ui.btn_stop.setText(self.ln["btn_stop"][self.cln])
            self.ui.btn_stop.setToolTip(self.ln["btn_stop_ttp"][self.cln])
            self.ui.whatsAppNumbers.setText(self.ln["whatsAppNumbers"][self.cln])
            self.ui.label_count_txt.setText(self.ln["label_count_txt"][self.cln])
            self.ui.label_count_txt_3.setText(self.ln["label_count_txt_3"][self.cln])
            self.ui.label_count_txt_4.setText(self.ln["label_count_txt_4"][self.cln])
            self.ui.label_count_txt_5.setText(self.ln["label_count_txt_5"][self.cln])
            self.ui.textBrowser.setText(self.ln["textBrowser"][self.cln])
            self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(
                self.ui.tab_Analyz), self.ln["start_tab_a"][self.cln])
            self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(self.ui.tab_msg), self.ln["start_tab_m"][self.cln])
            self.ui.start_tab.setTabText(self.ui.start_tab.indexOf(self.ui.tab_img), self.ln["start_tab_i"][self.cln])
            self.ui.frame_LCD_label.setToolTip(self.ln["frame_LCD_label"][self.cln])
            self.ui.frame_LCD.setToolTip(self.ln["frame_LCD"][self.cln])
            self.ui.LogBox.setToolTip(self.ln["LogBox"][self.cln])
            self.ui.frame_msg.setToolTip(self.ln["frame_msg"][self.cln])
            self.ui.tab_Analyz.setToolTip(self.ln["tab_Analyz_ttp"][self.cln])
            self.ui.btn_close.setToolTip(self.ln["btn_close"][self.cln])
            self.ui.btn_min.setToolTip(self.ln["btn_min"][self.cln])
            self.ui.btn_maxmin.setToolTip(self.ln["btn_maxmin"][self.cln])
            self.ui.label.setText(self.ln["label"][self.cln])
            self.ui.textMSG.setToolTip(self.ln["textMSG"][self.cln])
            self.ui.label_2.setText(self.ln["label_2"][self.cln])
            self.ui.label_3.setText(self.ln["label_3"][self.cln])
            self.ui.sleepMax.setToolTip(self.ln["sleepMax"][self.cln])
            self.ui.sleepMin.setToolTip(self.ln["sleepMin"][self.cln])
            self.ui.label_11.setText(self.ln["label_11"][self.cln])
            self.ui.label_10.setText(self.ln["label_10"][self.cln])
            self.ui.sleepMax_I.setToolTip(self.ln["sleepMax"][self.cln])
            self.ui.sleepMin_I.setToolTip(self.ln["sleepMin"][self.cln])
            self.ui.label_caption.setText(self.ln["label_caption"][self.cln])
            self.ui.caption.setToolTip(self.ln["caption_ttp"][self.cln])
            self.ui.btn_img.setText(self.ln["btn_img"][self.cln])
            self.ui.btn_img.setToolTip(self.ln["btn_img_ttp"][self.cln])
            self.ui.tab_msg.setToolTip(self.ln["tab_msg"][self.cln])
            self.ui.tab_img.setToolTip(self.ln["tab_img"][self.cln])
            self.ui.areaCode.setToolTip(self.ln["areaCode"][self.cln])
            self.ui.areaCode.setPlaceholderText(self.ln["areacode_hldr"][self.cln])
            self.ui.langs.setToolTip(self.ln["langs"][self.cln])
        except:
            log.exception("")
        try:
            self.fia.btn_importaccount.setText(self.ln["fia_btn_importaccount"][self.cln])
            self.fia.btn_importaccount.setToolTip(self.ln["fia_btn_importaccount_ttp"][self.cln])
            self.fia.btn_addnewtel.setPlaceholderText(self.ln["fia_btn_addnewtel_phdr"][self.cln])
            self.fia.label_2.setText(self.ln["fia_label_2"][self.cln])
            self.fia.btn_import_cancel.setText(self.ln["btn_cancel"][self.cln])
            self.fia.btn_import_cancel.setToolTip(self.ln["fia_btn_import_cancel_ttp"][self.cln])
        except:
            log.exception("")
        try:
            self.fi.label.setText(self.ln["fi_label"][self.cln])
            self.fi.btn_importFile.setText(self.ln["fi_btn_importFile"][self.cln])
            self.fi.btn_importFile.setToolTip(self.ln["fi_btn_importFile_ttp"][self.cln])
            self.fi.label_2.setText(self.ln["fi_label_2"][self.cln])
            self.fi.btn_importManual.setText(self.ln["fi_btn_importManual"][self.cln])
            self.fi.btn_importManual.setToolTip(self.ln["fi_btn_import_cancel_ttp"][self.cln])
            self.fi.btn_import_cancel.setText(self.ln["btn_cancel"][self.cln])
            self.fi.btn_import_cancel.setToolTip(self.ln["fi_btn_import_cancel_ttp"][self.cln])
            self.fi.manualNumber.setToolTip(self.ln["fi_manualNumber_ttp"][self.cln])
        except:
            log.exception("")
        try:
            self.frOM.label.setText(self.ln["frm_label"][self.cln])
            self.frOM.label_2.setText(self.ln["frm_label_2"][self.cln])
            self.frOM.generate_num.setToolTip(self.ln["frm_generate_num"][self.cln])
            self.frOM.generate_count.setToolTip(self.ln["frm_generate_count"][self.cln])
            self.frOM.btn_g_ok.setText(self.ln["frm_btn_g_ok"][self.cln])
            self.frOM.btn_g_ok.setToolTip(self.ln["frm_btn_g_ok_ttp"][self.cln])
            self.frOM.btn_g_cancel.setText(self.ln["btn_cancel"][self.cln])
            self.frOM.btn_g_cancel.setToolTip(self.ln["frm_btn_g_cancel_ttp"][self.cln])
        except:
            log.exception("")
        # try:
        #     self.ui.retranslateUi(MainWindow=self.MainWindow)
        # except:
        #     log.exception("")
        # try:
        #     self.fia.retranslateUi(self.formQImport)
        # except:
        #     log.exception("")
        # try:
        #     self.fi.retranslateUi(self.formQImport1)
        # except:
        #     log.exception("")
        # try:
        #     self.frOM.retranslateUi(self.generateForm)
        # except:
        #     log.exception("")

    def userChck(self):
        try:
            self.userStatus = NetWork(step=2, user=self.__LICENS__)
            self.userStatus.start()
            self.userStatus.Checker.connect(self.userChecker)
        except:
            log.exception("usr check")

    def checkVer(self, value):
        try:
            if value[0] != "last version":
                ver = value[0]
                link = value[1]
                self.msgError(
                    fr"""<html><head/><body><p align="center">نسخه جدید ({ver}) برنامه در دسترس است</p><p align="center">لطفا آن را <a href="{
                        link}"><span style=" text-decoration: underline; color:#0000ff;">دانلود</span></a> و نصب کنید</p></body></html>""",
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
            # QApplication.processEvents()
            global db
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.dbPath)
            db.open()
            # projectModel = QSqlQueryModel()
            self.projectModel = ColorfullSqlQueryModel()
            self.projectModel.setQuery(commandSQL, db)
            tel = self.ln["tb_header_tel"][self.cln]
            st = self.ln["tb_header_st"][self.cln]
            ress = self.ln["tb_header_ress"][self.cln]
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
                    log.debug("scroll")
            # QApplication.processEvents()
        except Exception as e:
            if hasattr(e, 'message'):
                log.exception(fr"{e.message}")
                errormsg = e.message
            else:
                log.debug(e)
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
                    with sqlite3.connect(fr"{self.dbPath}") as dbi:
                        log.debug("Connected to Database")
                        TableNow = self.Time()
                        table = fr"CREATE TABLE IF NOT EXISTS `{
                            TableNow}` (num INT PRIMARY KEY NOT NULL, status VARCHAR(50), res VARCHAR(12))"
                        dbi.execute(table)
                        log.debug("Table OK")
                        i = 1
                        for num in NUMBERS:
                            insert = fr"INSERT INTO `{TableNow}` (num,status) VALUES ('{num}','')"
                            dbi.execute(insert)
                            i += 1
                        dbi.commit()
                except:
                    try:
                        db.close()
                    except:
                        log.debug("error db")
                    try:
                        dbi.close()
                    except:
                        log.debug("error dbi", exc_info=True)
                    os.remove(self.dbPath)
                    with sqlite3.connect(fr"{self.dbPath}") as dbi:
                        log.debug("Connected to Database")
                        TableNow = self.Time()
                        table = fr"CREATE TABLE IF NOT EXISTS `{
                            TableNow}` (num INT PRIMARY KEY NOT NULL, status VARCHAR(50), res VARCHAR(12))"
                        dbi.execute(table)
                        log.debug("Table OK")
                        i = 1
                        for num in NUMBERS:
                            insert = fr"INSERT INTO `{TableNow}` (num,status) VALUES ('{num}','')"
                            dbi.execute(insert)
                            i += 1
                        dbi.commit()
                self.ui.LogBox.clear()
                self.ui.LogBox.appendPlainText("--- Numbers entered successfully ---")
                self.showNumberList(commandSQL=fr"select * from `{TableNow}`")
                self.ui.btn_clear.setEnabled(True)
            except:
                self.msgError(self.ln["listloader_err"][self.cln])
            try:
                dbi.close()
            except:
                pass
        else:
            log.debug("Not Selected File!")
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
        buttonY.setText(self.ln["msgerr_ok"][self.cln])
        box.setStyleSheet("""QMessageBox{\n
                          background-color:    #d9c9a3    ;\n
                          border: 3px solid   #ff0000  ;\n
                          border-radius:5px;\n
                          }\n
                          QLabel{\n
                          color:   %s  ;\n
                          font: 12pt \"Arial\";\n
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
                          font: 12pt \"Arial\";\n
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
        log.debug(number)
        if db.open():
            query = QSqlQuery()
            if self.ui.start_tab.currentIndex() == 0:
                query.exec_(fr"update `{TableNow}` set status = '✓', res = '☑' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 1:
                query.exec_(fr"update `{TableNow}` set status = '✓✓', res = '☑' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 2:
                query.exec_(fr"update `{TableNow}` set status = '✓✓✓', res = '☑' where num = '{number}'")
            self.showNumberList(commandSQL=fr"select * from `{TableNow}`", focus=self.reviewedCount)
        else:
            log.debug("wa Db Not Open")

    def nwaINS(self, number):
        log.debug(number)
        if db.open():
            query = QSqlQuery()
            if self.ui.start_tab.currentIndex() == 0:
                query.exec_(fr"update `{TableNow}` set status = '✓', res = '☒' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 1:
                query.exec_(fr"update `{TableNow}` set status = '✓✓', res = '☒' where num = '{number}'")
            elif self.ui.start_tab.currentIndex() == 2:
                query.exec_(fr"update `{TableNow}` set status = '✓✓✓', res = '☒' where num = '{number}'")
            self.showNumberList(commandSQL=fr"select * from `{TableNow}`", focus=self.reviewedCount)
        else:
            log.debug("nwa Db Not Open")

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
                    log.exception(fr"{e.message}")
                    errormsg = e.message
                else:
                    log.debug(e)
                    errormsg = e
                self.msgError(fr"{errormsg}")

    def stop_progress(self):
        log.debug("stop")
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
                log.debug(e.message)
                errormsg = e.message
            else:
                log.debug(e)
                errormsg = e
            self.msgError(fr"{errormsg}")

    def AnalyzNum(self):
        try:
            if db.open():
                # QApplication.processEvents()
                log.debug("Analyz OK")
                query = QSqlQuery()
                query.exec_(fr"select * from `{TableNow}` where status = ''")
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
                log.exception(e.message)
            else:
                log.debug(e)
            self.msgError(self.ln["analyz_err"][self.cln])

    def sendMsg(self, text):
        try:
            if db.open():
                # QApplication.processEvents()
                query = QSqlQuery()
                query.exec_(fr"select * from `{TableNow}` where status = '' or res = '☑'")
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
                log.exception(e.message)
            else:
                log.debug(e)
            self.msgError(self.ln["msg_err"][self.cln])

    def sendImg(self, path, caption=''):
        try:
            if db.open():
                # QApplication.processEvents()
                query = QSqlQuery()
                query.exec_(fr"select * from `{TableNow}` where status = '' or res = '☑'")
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
                log.exception(e.message)
            else:
                log.debug(e)
            self.msgError(self.ln["img_err"][self.cln])

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
        # self.User = value
        self.User = True
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
        self.RememberLogin = True

        log.info("Start")
        Net = self.ConnectionCheck()
        try:
            log.debug(fr"{Net} {self.User}")
            if db.open():
                if Net:
                    if self.User:
                        currentIndex = self.ui.start_tab.currentIndex()
                        if currentIndex == 0:
                            self.btnStatus()
                            self.ui.LogBox.appendPlainText(fr"-- Start analysis --")
                            self.AnalyzNum()
                        elif currentIndex == 1:
                            log.debug("message Tab")
                            text = self.ui.textMSG.toPlainText()
                            log.debug(text)
                            if text != '':
                                self.btnStatus()
                                self.ui.LogBox.appendPlainText(fr"-- Start Send Message --")
                                self.sendMsg(text)
                            else:
                                self.msgError(self.ln["inputxt_err"][self.cln])
                        elif currentIndex == 2:
                            log.debug('image tab')
                            if self.p != '':
                                caption = self.ui.caption.toPlainText()
                                self.ui.LogBox.appendPlainText(fr"-- Start Send Image --")
                                self.sendImg(path=self.p, caption=caption)
                                self.btnStatus()
                            else:
                                self.msgError(self.ln["inputimg_err"][self.cln])
                        else:
                            self.msgError()
                        if not self.RememberLogin:
                            lisT = os.listdir('temp')
                            import shutil
                            for f in lisT:
                                try:
                                    if f == 'temporary.data':
                                        continue
                                    os.remove(fr"temp/{f}")
                                except:
                                    try:
                                        os.rmdir(fr"temp/{f}")
                                    except:
                                        shutil.rmtree(fr"temp/{f}")
                                        continue
                                    continue
                    else:
                        self.msgError(self.ln["per_err"][self.cln], colorf='#1b6900')
                else:
                    self.msgError(self.ln["net_err"][self.cln])
        except:
            self.msgError(self.ln["ldlist_err"][self.cln])

    def export(self):
        try:
            if db.open():
                DeskTop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                appName = self.ui.label_appName.text()
                if not os.path.isdir(f'{DeskTop}/{appName}'):
                    os.mkdir(f'{DeskTop}/{appName}')
                query = QSqlQuery()
                query.exec_(fr"select * from `{TableNow}`")
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
                            writer.writerow([fr"{number}"])
                            # cSv.write(fr"{number}\n")
                self.msgError(errorText=self.ln["export_sucs"][self.cln], icon='Information', colorf="#214917")
        except Exception as e:
            if hasattr(e, 'message'):
                log.exception(e.message)
                errormsg = e.message
            else:
                log.debug(e)
                errormsg = e
            self.msgError(self.ln["export_err"][self.cln])

    def initGenerate(self):
        log.debug("init Generate")
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
        self.frOM.btn_g_cancel.clicked.connect(self.generateForm.close)
        self.frOM.btn_g_ok.clicked.connect(self.importGenerate)

    def generate(self):
        log.debug("btn generate")
        self.languageSet()
        self.generateForm.show()

    def importGenerate(self):
        firstNumber = self.frOM.generate_num.text()
        RangeNum = self.frOM.generate_count.text()
        if RangeNum == '':
            RangeNum = 10
        if firstNumber != '':
            if not len(firstNumber) < 9:
                path = fr"temp\generate-{self.Time()}.csv"
                log.debug(firstNumber, path)
                for i in range(int(RangeNum)):
                    with open(fr"{path}", 'a+') as g:
                        writer = csv.writer(g, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,
                                            lineterminator='\n')
                        writer.writerow([fr"{firstNumber}"])
                    firstNumber = int(firstNumber) + 1
                    # log.debug(firstNumber)
                self.generateForm.close()
                self.ListLoader(path)
                self.msgError(errorText=self.ln["listcreate_sucs"][self.cln], icon='Information', colorf="#214917")
                os.remove(path)
            else:
                self.msgError(self.ln["num_valid"][self.cln])
        else:
            self.msgError(self.ln["generate_err"][self.cln])

    def initImport(self):
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

    def importer(self):
        self.languageSet()
        self.formQImport1.show()

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
                log.debug(numLine)
                path = fr"temp\manualNumber-{self.Time()}.csv"
                for num in numLine:
                    if num == '':
                        continue
                    num = int(num)
                    with open(fr"{path}", 'a+') as g:
                        writer = csv.writer(g, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,
                                            lineterminator='\n')
                        writer.writerow([fr"{num}"])
                self.formQImport1.close()
                self.ListLoader(path)
                self.msgError(errorText=self.ln["load_sucs"][self.cln], icon='Information', colorf="#214917")
                os.remove(path)
            except:
                self.msgError(self.ln["num_load_err"][self.cln])
        else:
            self.msgError(self.ln["slctnums_err"][self.cln])

    def initAccountList(self):
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
        try:
            if not os.path.exists('./temp/cache'):
                os.makedirs('temp/cache/')
        except:
            os.makedirs('./temp/cache/')
        cacheList = os.listdir('temp/cache/')
        log.debug(cacheList)
        self.modelAcc = TableModel(cacheList)
        self.fia.accountsTable.setModel(self.modelAcc)
        # self.rowCount = self.modelAcc.rowCount()
        # self.fia.btn_importaccount.clicked.connect(self.addAccounts)
        # self.fia.btn_importaccount.setEnabled(False)
        self.fia.btn_importaccount.clicked.connect(lambda: self.msgError(
            errorText=self.ln["undefine_feature"][self.cln], icon="", colorf="#0013ff"))

    def accountsList(self):
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
            self.msgError(self.ln["acc_num"][self.cln])

    def clearList(self):
        try:
            log.debug("table reset")
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
                log.debug(img_path)
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
            log.debug("Checking internet connection failed, status code {0}.".format(
                e.response.status_code), exc_info=True)
            return False
        except requests.ConnectionError:
            log.debug("No internet connection available.", exc_info=True)
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
        log.debug('terminate thread')
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
