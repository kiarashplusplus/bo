from PyQt4 import QtCore, QtGui
import sys
import webbrowser
import requests
#import hoover
import json
import logging
import platform
import time
#from  icons_rc import *
#import eventlet
#eventlet.monkey_patch()
endpoint ="http://windows.blockedonline.net/"
version='2.0.0'
logging.addLevelName(logging.INFO, 'info')
logger = logging.getLogger(version)
logger.setLevel(logging.INFO)

#logglyhandler = hoover.LogglyHttpHandler(token='6bf8759b-eb06-4de5-be82-b098501b0e4a',secure=False)
#logglyhandler.setLevel(logging.WARNING)
#uname=', '.join(platform.uname())
#logglyformatter = logging.Formatter('{\"time": "%(asctime)s", "version":"%(name)s", "level":"%(levelname)s",' \
# '"error_number": "%(error_number)s", "message":"%(message)s", "uname":"%(uname)s", "uid":"%(uid)s", "other":"%(other)s"}' )
 
#logglyhandler.setFormatter(logglyformatter)

#logger.addHandler(logglyhandler)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(276, 188)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())  
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(_fromUtf8(" QScrollBar:vertical  {\n"
"     border: 2px solid #FFF5EE;\n"
"     background: #FFF;\n"
"     width: 15px;\n"
"     margin: 22px 0 22px 0;\n"
" }\n"
" QScrollBar::handle:vertical  {\n"
"     background: #5abcce;\n"  
"     min-height: 20px;\n"
" }\n"
" QScrollBar::add-line:vertical  {\n"
"     background: #FFF;\n"
"     height: 20px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" \n"
" QScrollBar::sub-line:vertical  {\n"
"     background: #FFF;\n"
"     height: 20px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical  {\n"
"     border: 2px solid #5abcce;\n"
"     width: 3px;\n"
"     height: 3px;\n"
"     background: white;\n"
" }\n"
" \n"
"\n"
"QDialog {\n"
"    background: #fbfbfb ;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    background: #FFF;\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 2px solid #5abcce;\n"
"    width:40px;\n"
"}\n"
"\n"
"QTextBrowser {\n"
"    background: #FFF;\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 2px solid #FFF5EE;\n"
"    width:40px;\n"
"}\n"
"\n"
"\n"
"QPushButton{\n"
"  padding: 4px 12px;\n"
"\n"
"  color: #FFF;\n"
"  background: #5abcce;\n"
"  border-color: #5abcce;\n"
"\n"
"border: 2px solid #5abcce;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"  padding: 4px 12px;\n"
"\n"
"  color: #5abcce;\n"
"  background: #FFFFFF;\n" 
"  border-color: #FFFFFF;\n"
"\n"
"border: 2px solid #5abcce;\n"
"}\n"
"\n"
"QComboBox  {\n"
"    color:#000;\n"
"    border: 1px solid #5abcce;\n"
"    background:#FFF;\n"
"    padding: 1px 18px 1px 3px;\n"
"}\n"
"\n"
"QComboBox:disabled  {\n"
"    color:#d9d9d9;\n"
"    border: 1px solid #d9d9d9;\n"
"    background:#eeeeee;\n"
"    padding: 1px 18px 1px 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down:disabled  {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: #d9d9d9;\n"
"    border-left-style: solid; \n"
"\n"
"}\n"
"\n"
"QComboBox::drop-down  {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: #5abcce;\n"
"    border-left-style: solid; \n"
"\n"
"}\n"
" \n"
"QComboBox QAbstractItemView  {\n"
"   border: 2px solid #5abcce;\n"
"    background: #FFF;\n"
"    selection-background-color: #FFF;\n"
"    selection-color: #000;\n"
"    outline: 1px solid #5abcce;\n"
"}\n"
"\n"
"\n"
""))
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setInputMask(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setFont(font)
        self.label_3.setOpenExternalLinks( True )
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed) 
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.pushButton = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Blocked Online", None))
        self.label.setText(_translate("Dialog", "Your location", None))
        self.label_2.setText(_translate("Dialog", "Your email", None))
        self.lineEdit.setText(_translate("Dialog", "Optional", None))
        self.label_3.setText(_translate("Dialog", "Please acknowledge BlockedOnline <a href = \"http://www.blockedonline.com/about\">Terms and Conditions</a>.", None))
        self.checkBox.setText(_translate("Dialog", "I have read and I agree with the Terms and Conditions.", None))
        self.pushButton.setText(_translate("Dialog", "Start", None))


class ConsoleWindowLogHandler(logging.Handler):
    def __init__(self, sigEmitter):
        super(ConsoleWindowLogHandler, self).__init__()
        self.sigEmitter = sigEmitter

    def emit(self, logRecord):
        message = str(logRecord.getMessage())
        self.sigEmitter.emit(QtCore.SIGNAL("logMsg(QString)"), message)
        self.sigEmitter.emit(QtCore.SIGNAL("logMsg(QString)"), "\n")


class RightClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "Edit", parent)

        openBrowser = QtGui.QAction(QtGui.QIcon(''), '&Investigate data on the web', self)        
        openBrowser.triggered.connect(self.photovaultWeb)
        self.addAction(openBrowser)

        exitAction = QtGui.QAction(QtGui.QIcon(''), '&Exit', self)        
        exitAction.triggered.connect(QtGui.QApplication.exit)
        exitAction.setIcon(QtGui.QIcon(":/icons/eye.ico"))

        self.addAction(exitAction)
        
    def photovaultWeb(self):
        webbrowser.open_new_tab( "http://www.blockedonline.com")

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        style = QtGui.qApp.style()
        self.setIcon(QtGui.QIcon(":/icons/eye.ico"))
        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

    # def welcome(self):
    #     self.showMessage("PhotoVault Uploader", "Your scheduler will run according to your settings.")
        
    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        #QtCore.QTimer.singleShot(10, self.welcome)

def logglier(msg, number=0, other=' '):
    print msg, number, other

    #settings = QtCore.QSettings('blockedonline', 'main')
    #q=settings.allKeys()
    #uid = " ".join(map(str, q))

    #logger.error(msg, extra={'uid':uid,'error_number':number, 'uname':uname, 'other':str(other)} )
    logger.error(msg) #extra={'uid':uid,'error_number':number, 'uname':uname, 'other':str(other)} )

def onewebsite(w):
    try:
        #with eventlet.Timeout(20):
        r= requests.get(w, verify=False, timeout=4)
        return (1, {"epoch":int(time.time()), "url": w, "final_url": r.url,"length": len(r.content), 
                "elapsed":r.elapsed.total_seconds(), "history": str([(l.status_code, l.url) for l in r.history]), 
                "headers":str(r.headers.items()), "cookies": str(r.cookies.items()), "status_code": r.status_code,
                "content": r.content[:1500] })
    except Exception as e:
        result = {"epoch": int(time.time()), "url": w, "final_url": '0', "length": 0, 
        "elapsed": 0, "history":str(e), "headers": '0', "cookies" :'0', "status_code": 0,
        "content":"0"}
        return (0, result)

def checkPing():
    w1= endpoint+"ping"
    state, data = onewebsite(w1)
    if not data['content']=='<h1>OK</h1>':
        return False
    return True

def loadData(country, email):
    print "loading data"
    print checkPing()
    settings = QtCore.QSettings('blockedonline', 'main')
    uid = settings.value(str(country), 0).toInt()[0]
    while(not checkPing()):
        logglier("no connection.. waiting.")
        time.sleep(10)
    if uid:
        print "already got it: ", uid
        try:
            f=requests.get(endpoint+"blocked/load", params={'uid':uid}, verify=False)
            return f.json()['websites'] 
        except Exception as e:
            print f.status_code, f.content
            logglier("Couldn't load webistes list! Please report this.", number=1, other=e)
            return []
    else:
        payload = {'email': email, 'country': countryNames[country], 'client':'desktop_{0}'.format(version)}
        headers = {'content-type': 'application/json'}       
        try:
            r=requests.post(endpoint+"blocked/load", data=json.dumps(payload, encoding='ISO-8859-1'), headers=headers,verify=False)
            if r.status_code==200:
                uid = json.loads(r.content)['uid']
                settings.setValue(str(country),uid)
                print uid
                return loadData(country,email)
            else:
                print r.status_code, r.content
                return []
        except Exception as e:
            logglier("Trouble connecting to our server. Retrying shortly.", number=133, other=e)
            time.sleep(15)
            try:
                r=requests.post(endpoint+"blocked/load", data=json.dumps(payload, encoding='ISO-8859-1'), headers=headers,verify=False)
                if r.status_code==200:
                    uid = json.loads(r.content)['uid']
                    settings.setValue(str(country),uid)
                    return loadData(country,email)
                else:
                    return []
            except Exception as e:
                logglier("No luck with the server. Sorry!", number=134, other=e)
                return []

countryNames=sorted(["Canada","Sao Tome and Principe","Venezuela","Guinea-Bissau","Montenegro","Lithuania","Cambodia","Saint Helena","Switzerland","Ethiopia","Aruba","Argentina","Cameroon","Burkina Faso","Turkmenistan","Ghana","Saudi Arabia","Rwanda","Togo","Japan","American Samoa","Montserrat","Cocos (Keeling) Islands","Pitcairn","Guatemala","Bosnia and Herzegovina","Kuwait","Russian Federation","Jordan","Bonaire","Virgin Islands","Dominica","Liberia","Maldives","Micronesia","Jamaica","Oman","Martinique","Albania","Gabon","Niue","Monaco","Wallis and Futuna","New Zealand","Virgin Islands","Jersey","Andorra","Yemen","Greenland","Samoa","Norfolk Island","United Arab Emirates","Guam","India","Azerbaijan","Lesotho","Saint Vincent and the Grenadines","Kenya","Macao","Turkey","Afghanistan","Bangladesh","Mauritania","Solomon Islands","Turks and Caicos Islands","Saint Lucia","San Marino","French Polynesia","France","Syrian Arab Republic","Bermuda","Slovakia","Somalia","Peru","Swaziland","Nauru","Seychelles","Norway","Malawi","Cook Islands","Benin","Western Sahara","Cuba","Iran","Falkland Islands (Malvinas)","Mayotte","Holy See (Vatican City State)","China","Armenia","Timor-Leste","Dominican Republic","Ukraine","Bahrain","Tonga","Finland","Libya","Mexico","Cayman Islands","Central African Republic","New Caledonia","Mauritius","Tajikistan","Liechtenstein","Australia","Mali","Sweden","Bulgaria","Palestine","United States","Romania","Angola","Chad","South Africa","Tokelau","Cyprus","Brunei Darussalam","Qatar","Malaysia","Austria","Mozambique","Uganda","Hungary","Niger","Isle of Man","Brazil","Faroe Islands","Guinea","Panama","South Korea","Costa Rica","Luxembourg","Cape Verde","Bahamas","Gibraltar","Ireland","Pakistan","Palau","Nigeria","Ecuador","Czech Republic","Macedonia","Viet Nam","Belarus","Vanuatu","Algeria","Slovenia","El Salvador","Tuvalu","Saint Pierre and Miquelon","Marshall Islands","Chile","Puerto Rico","Belgium","Kiribati","Haiti","Belize","Hong Kong","Sierra Leone","Georgia","Lao People's Democratic Republic","Gambia","Philippines","Morocco","Croatia","Mongolia","Guernsey","Thailand","Namibia","Grenada","Taiwan","Iraq","Tanzania","Portugal","Estonia","Uruguay","Equatorial Guinea","Lebanon","Svalbard and Jan Mayen","Uzbekistan","Tunisia","Djibouti","Antigua and Barbuda","Spain","Colombia","Burundi","Fiji","Barbados","Madagascar","Italy","Bhutan","Sudan","Bolivia","Nepal","Malta","Netherlands","Northern Mariana Islands","Suriname","Anguilla","Christmas Island","Indonesia","Iceland","Zambia","Senegal","Papua New Guinea","Saint Kitts and Nevis","Trinidad and Tobago","Zimbabwe","Germany","Denmark","Kazakhstan","Poland","Moldova","Eritrea","Kyrgyzstan","Congo","North Korea","Israel","Sri Lanka","Latvia","South Sudan","Guyana","Guadeloupe","Honduras","Myanmar","Egypt","Nicaragua","Singapore","Serbia","Botswana","United Kingdom","Antarctica","Congo","Sint Maarten (Dutch part)","Greece","Paraguay","French Guiana","Comoros"])

def postData(data, country):
    settings = QtCore.QSettings('blockedonline', 'main')
    if len(data) is 0:
        return 1
    uid = settings.value(str(country), 0).toInt()[0]
    while(not checkPing()):
        logglier("no connection.. waiting.")
        time.sleep(10)

    payload = {'report': data, 'uid': uid}
    headers = {'content-type': 'application/json'}
    try:
        r=requests.post(endpoint+"blocked/report", data=json.dumps(payload, encoding='ISO-8859-1'), headers=headers,verify=False)
        if r.status_code==200:
            return 1
        else:
            print "posting fail status", r.status_code, r.content
            return 0
    except Exception as e:
        logglier("Trouble connecting to our server. Retrying shortly.", number=133, other=e)
        time.sleep(15)

        try:
            r=requests.post(endpoint+"blocked/report", data=json.dumps(payload, encoding='ISO-8859-1'), headers=headers,verify=False)
            logglier("Server is back. Processing more...", number=135, other=e)
            if r.status_code==200:
                return 1
            else:
                return 0
        except Exception as e:
            logglier("No luck with the server. Sorry!", number=134, other=e)
            return 0

class Worker(QtCore.QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)       

class StartQT4(QtGui.QDialog):
    def __init__(self, parent=None):
        super(StartQT4, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.icon=SystemTrayIcon()
        self.icon.isSystemTrayAvailable()
        self.ui.pushButton.clicked.connect(self.scan)
        self.icon.activated.connect(self.activate)

        self.ui.comboBox.addItems(['']+countryNames)
        self.ui.comboBox.activated['int'].connect(self.handleChangedCombo)
        self.country=-1

        self.scanflag=False

        self.bee = Worker(self.beescanner, ())
        self.bee.finished.connect(self.closeOnError)
        self.bee.terminated.connect(self.closeOnError)

        self.versionbee = Worker(self._checkVersion, ())
        self.versionbee.terminated.connect(self.closeOnError)
        self.versionbee.start()

        dummyEmitter = QtCore.QObject()
        self.connect(dummyEmitter, QtCore.SIGNAL("logMsg(QString)"), self.ui.textBrowser.append)
        consoleHandler = ConsoleWindowLogHandler(dummyEmitter)
        consoleHandler.setLevel(logging.INFO)
        chformatter = logging.Formatter('%(levelname)s: %(message)s')
        consoleHandler.setFormatter(chformatter)
        logger.addHandler(consoleHandler)
        logger.info("If you enter your email address, we will send you future updates. But it is optional.")        

    def _checkVersion(self):
        try:
            r= requests.get(endpoint+"software_version", verify=False)
            if r.text!=version:
                logglier("This file is too old! Please download the latest version.", number=2)
                time.sleep(20)
                self.closeOnError()
        except Exception as e:
            logglier("Something went wrong. Please report this! Are you connected to the internet?",number=3, other=e)
            time.sleep(20)
            self.closeOnError()

    def beescanner(self):
        verbose=1

        websites=loadData(self.country, str(self.ui.lineEdit.text()))
        if websites and verbose:
            logglier("Finished loading {0} websites. Starting to process...".format(len(websites)),number=77,other=[self.country, str(self.ui.lineEdit.text())])

        leftovers=[]
        retry=[]

        if websites:
            data=[]
            count=0
            for w in websites:
                status, result = onewebsite(w)
                if status:
                    data.append(result)
                else:
                    while(not checkPing()):
                        logglier("no connection.. waiting.")
                        time.sleep(10)
                    leftovers.append(w)
                
                if len(data) > 30:
                    if not postData(data, self.country):
                        logglier("Something went wrong! Please report this.", number=4)
                        time.sleep(20)
                        self.closeOnError()
                    else:
                        count=count+len(data)
                        if verbose: logger.info(str(count*5)+" websites checked! Processing more...")
                        data = []

                if len(leftovers) > 30:
                    for l in leftovers:
                        status, result = onewebsite(l)
                        if status:
                            data.append(result)
                        else:
                            while(not checkPing()):
                                logglier("no connection.. waiting.")
                                time.sleep(10)
                            retry.append(l)
                    leftovers = []

                if len(retry) > 30:
                    for retw in retry:
                        while(not checkPing()):
                            logglier("no connection.. waiting.")
                            time.sleep(10)
                        status, result = onewebsite(retw)
                        data.append(result)
                    retry = []

            retry.extend(leftovers)
            for retw in retry:
                status, result = onewebsite(retw)
                if status:
                    data.append(result)
                else:
                    while(not checkPing()):
                        time.sleep(10)
                    data.append(result)

            if not postData(data, self.country):
                logglier("Something went wrong! Please report this.", number=5)
                time.sleep(20)
                self.closeOnError()
            else:
                if verbose: logger.info("Almost done!")
       
    def scan(self):
        if self.country==-1:
            logglier("You must select your country! Email is optional!", number=6)
        elif not self.ui.checkBox.isChecked():
            logglier("You must agree with our Terms and Conditions.")
        else:
            self.scanflag=True
            self.ui.pushButton.hide()
            self.ui.lineEdit.hide()
            self.ui.label_2.hide()
            self.ui.label.hide()
            self.ui.comboBox.hide()
            self.ui.label_3.hide()
            self.ui.checkBox.hide()
            logger.info("This program will automatically close when finished. It might take some hours though.")
            self.bee.start()

    def closeOnError(self):
        QtGui.QApplication.exit()

    def closeEvent(self, event):
        if self.scanflag==False:
            QtGui.QApplication.exit()
        else:
            self.icon.show()
            self.hide() 
            event.ignore() 
            
    def activate(self,reason):
        if reason==3:
            self.show()
            
    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()  

    def handleChangedCombo(self, ind):
        self.country=ind-1

class SingleApplication(QtGui.QApplication):
    def __init__(self, argv, key):  
        QtGui.QApplication.__init__(self, argv)
        
        self._memory = QtCore.QSharedMemory(self)
        self._memory.setKey(key)
        if self._memory.attach():
            self._running = True
        else:
            self._running = False
            if not self._memory.create(1):
                raise RuntimeError(
                    self._memory.errorString().toLocal8Bit().data())
                    
    def isRunning(self):
        return self._running
 
if __name__ == "__main__":
    
    key = 'Report Internet Latency'

    app = SingleApplication(sys.argv, key)
    if app.isRunning():
        sys.exit(1)    
    mainWindow = StartQT4()
    app.setActiveWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
