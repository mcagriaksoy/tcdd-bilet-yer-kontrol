# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSlider,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(592, 484)
        MainWindow.setLocale(QLocale(QLocale.Turkish, QLocale.Turkey))
        self.actionHakk_nda = QAction(MainWindow)
        self.actionHakk_nda.setObjectName(u"actionHakk_nda")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 210, 571, 31))
        font = QFont()
        font.setFamilies([u"Microsoft New Tai Lue"])
        self.horizontalLayoutWidget.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_start = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        font1 = QFont()
        font1.setFamilies([u"Microsoft New Tai Lue"])
        font1.setPointSize(12)
        self.pushButton_start.setFont(font1)
        self.pushButton_start.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.horizontalLayout_2.addWidget(self.pushButton_start)

        self.pushButton_stop = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setFont(font1)
        self.pushButton_stop.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.horizontalLayout_2.addWidget(self.pushButton_stop)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 250, 571, 181))
        self.groupBox_4.setFont(font)
        self.textEdit = QTextEdit(self.groupBox_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 20, 551, 151))
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit.setReadOnly(True)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(330, 100, 251, 101))
        self.groupBox_3.setFont(font)
        self.checkBox_sound = QCheckBox(self.groupBox_3)
        self.checkBox_sound.setObjectName(u"checkBox_sound")
        self.checkBox_sound.setGeometry(QRect(10, 30, 221, 21))
        self.checkBox_sound.setFont(font)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(330, 10, 251, 81))
        self.groupBox.setFont(font)
        self.gridLayoutWidget_3 = QWidget(self.groupBox)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 231, 52))
        self.gridLayoutWidget_3.setFont(font)
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)

        self.botToken_text = QLineEdit(self.gridLayoutWidget_3)
        self.botToken_text.setObjectName(u"botToken_text")
        self.botToken_text.setFont(font)
        self.botToken_text.setFrame(False)

        self.gridLayout_3.addWidget(self.botToken_text, 0, 1, 1, 1)

        self.chatId_text = QLineEdit(self.gridLayoutWidget_3)
        self.chatId_text.setObjectName(u"chatId_text")
        self.chatId_text.setFont(font)
        self.chatId_text.setFrame(False)

        self.gridLayout_3.addWidget(self.chatId_text, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 311, 191))
        self.groupBox_2.setFont(font)
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 130, 291, 51))
        self.verticalLayoutWidget_2.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(self.verticalLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout.addWidget(self.label_9)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSlider_period = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider_period.setObjectName(u"horizontalSlider_period")
        self.horizontalSlider_period.setFont(font)
        self.horizontalSlider_period.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_2.addWidget(self.horizontalSlider_period)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 30, 291, 102))
        self.gridLayoutWidget.setFont(font)
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.dateTimeEdit = QDateTimeEdit(self.gridLayoutWidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setCalendarPopup(True)

        self.gridLayout_4.addWidget(self.dateTimeEdit, 2, 1, 1, 1)

        self.comboBox_nereye = QComboBox(self.gridLayoutWidget)
        self.comboBox_nereye.setObjectName(u"comboBox_nereye")
        self.comboBox_nereye.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_nereye, 1, 1, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)

        self.comboBox_nereden = QComboBox(self.gridLayoutWidget)
        self.comboBox_nereden.setObjectName(u"comboBox_nereden")
        self.comboBox_nereden.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_nereden, 0, 1, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 592, 22))
        self.menuYard_m = QMenu(self.menubar)
        self.menuYard_m.setObjectName(u"menuYard_m")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuYard_m.menuAction())
        self.menuYard_m.addAction(self.actionHakk_nda)
        self.menuYard_m.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionHakk_nda.setText(QCoreApplication.translate("MainWindow", u"Hakk\u0131nda", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Aramaya Basla!", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Durdur!", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Bilgi Ekrani", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Iletisim Ayarlari", None))
        self.checkBox_sound.setText(QCoreApplication.translate("MainWindow", u"Bilet bulunursa ses cal", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Telegram Ayarlar\u0131", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Bot Token:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Chat ID:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Aranilan Tren Bilgileri", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Arama S\u0131kl\u0131\u011f\u0131n\u0131 se\u00e7iniz: ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"1 dakika", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Nereye:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Tarih / Saat:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Nereden:", None))
        self.menuYard_m.setTitle(QCoreApplication.translate("MainWindow", u"Yard\u0131m", None))
    # retranslateUi

