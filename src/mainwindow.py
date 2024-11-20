# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject, Signal, QThread

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

# City names
import Sehirler
import error_codes as Durum
# Driver
import DriverSetting
import DriverGet
import Rota
import Control


class Worker(QObject):
    finished = Signal()
    ongoing = Signal()

    def __init__(self):
        super().__init__()
        self.working = True
    
    def run(self):
        while self.working:
            # Get the current date and time
            current_date_time = self.ui.dateTimeEdit.dateTime().currentDateTime()
            # Get the selected city names
            nereden = self.ui.comboBox_nereden.currentText()
            nereye = self.ui.comboBox_nereye.currentText()
            # Get the selected period
            period = self.ui.horizontalSlider_period.value()
            # Get the selected sound
            sound = self.ui.checkBox_sound.isChecked()
            # Get the selected date and time
            date_time = self.ui.dateTimeEdit.dateTime().toPyDateTime()

            # Get the selected driver
            driver = self.ui.comboBox_driver.currentText()
            # Get the selected driver settings
            driver_settings = DriverSetting.DriverSetting(driver)

            # Get the selected route
            route = Rota.Rota(nereden, nereye)

            # Get the selected control
            control = Control.Control(driver_settings, route, date_time, period, sound)

            # Get the selected driver
            driver_get = DriverGet.DriverGet(driver_settings, route, date_time, period, sound)

            # Get the selected driver
            driver_get.get()

            # Get the selected control
            control.control()

            # Emit the ongoing signal
            self.ongoing.emit()

            # Sleep for the selected period
            self.sleep(period * 60)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Update combobox with city names
        self.ui.comboBox_nereden.addItems(Sehirler.sehir_listesi)
        self.ui.comboBox_nereye.addItems(Sehirler.sehir_listesi)

        # Set default values
        self.ui.comboBox_nereden.setCurrentIndex(0)
        self.ui.comboBox_nereye.setCurrentIndex(23)

        # Set current date and time
        self.ui.dateTimeEdit.setDateTime(self.ui.dateTimeEdit.dateTime().currentDateTime())

        # Connect signals
        self.ui.horizontalSlider_period.valueChanged.connect(lambda: self.ui.label.setText(str(self.ui.horizontalSlider_period.value()) + " dakika"))
        self.ui.checkBox_sound.toggled.connect(lambda: self.ui.textEdit.setText("Ses açık" if self.ui.checkBox_sound.isChecked() else "Ses kapalı"))

        # Connect buttons
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)

    def start(self):
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton_start.setEnabled(False)
        #Create Qthread to run the loop
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        # Connect signals
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.ongoing.connect(self.updateLog)
        
        #start
        self.thread.start()
    
    def updateLog(self, text):
        self.ui.textEdit.append(text)
    
    def stop(self):
        self.worker.working = False
        self.thread.quit()

        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_start.setEnabled(True)
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
