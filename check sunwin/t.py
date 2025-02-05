
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker
from PyQt5.QtGui import QIntValidator, QColor, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Main

class WorkerThread(QThread):
    finished = pyqtSignal(int)

    def __init__(self, account, main_window_object):
        super().__init__()
        self.account = account
        self.main_window_object = main_window_object
        self.worker_threads = []
        self.file_lock = QMutex()

    def run(self):
        # print(self.account)
        # data = Main.run(self.account)
        # self.main_window_object.populate_table(data)
        for account in self.accounts:
            print(account)
            if self.mutex:
                self.mutex.lock()
                if not self.is_processed(account):
                    data = Main.run(account)
                    self.main_window_object.populate_table(data)
                    self.mark_processed(account)
                self.mutex.unlock()
            else:
                if not self.is_processed(account):
                    data = Main.run(account)
                    self.main_window_object.populate_table(data)
                    self.mark_processed(account)
        self.finished.emit(0)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_threads = []
        self.ui = Ui_MainWindow(self.worker_threads)
        self.ui.setupUi(self)

    def closeEvent(self, event):
        if event:
            reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # reset
            
            if reply == QMessageBox.Yes:
                event.accept()  
            else:
                event.ignore() 

class Ui_MainWindow(object):
    def __init__(self, worker_threads):
        self.worker_threads = worker_threads
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.setGeometry(100, 100, 1108, 703) 
        # MainWindow.res(1108, 703) 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 471, 151))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(310, 90, 61, 21))
        self.lineEdit_1.setObjectName("lineEdit_1")

        int_validator = QIntValidator()
        int_validator.setRange(0, 999) 
        self.lineEdit_1.setValidator(int_validator)
        self.lineEdit_1.setReadOnly(True)
        self.lineEdit_1.setText("0")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 80, 51, 41))
        self.label_2.setObjectName("label_2")
        self.label_12 = QtWidgets.QLabel(self.centralwidget) 
        self.label_12.setGeometry(QtCore.QRect(20, 92, 81, 16))
        self.label_12.setObjectName("label_12")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 120, 91, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""
            QPushButton {
                font-family: 'Helvetica', 'Arial', sans-serif;
                background-color: #ff0081;
                color: #fff;
                border-radius: 4px;
                border: none;
                position: relative;
                font-size: 15px;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 130, 0.5);
            }
        """)

        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 180, 1091, 481))
        self.tableWidget_2.setObjectName("tableWidget_2")

        self.tableWidget_2.setColumnCount(7)  

        total_columns = 7
        total_width = 1091 
        column_width = total_width // total_columns

        for column in range(total_columns):
            self.tableWidget_2.setColumnWidth(column, column_width)

        header_labels = ["Username", "Password", "Gold", "Két", "VIP","ACCESS TOKEN", "Status"]
        self.tableWidget_2.setHorizontalHeaderLabels(header_labels)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 110, 161, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(140, 110, 41, 41))
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 451, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(950, 655, 81, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1020, 655, 81, 31))
        self.label_7.setObjectName("label_7")
        self.label_live = QtWidgets.QLabel(self.centralwidget)
        self.label_live.setGeometry(QtCore.QRect(975, 655, 41, 31))
        self.label_live.setObjectName("label_live")
        self.label_die = QtWidgets.QLabel(self.centralwidget)
        self.label_die.setGeometry(QtCore.QRect(1045, 655, 41, 31))
        self.label_die.setObjectName("label_die")
        self.tableWidget_4 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_4.setGeometry(QtCore.QRect(490, 10, 301, 151))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(0)

        self.tableWidget_5 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_5.setGeometry(QtCore.QRect(800, 10, 301, 151))
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(0)
        self.tableWidget_5.setRowCount(0)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 120, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                font-family: 'Helvetica', 'Arial', sans-serif;
                background-color: #ff0081;
                color: #fff;
                border-radius: 4px;
                border: none;
                position: relative;
                font-size: 15px;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 130, 0.5);
            }
        """)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1000, 120, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                font-family: 'Helvetica', 'Arial', sans-serif;
                background-color: #ff0081;
                color: #fff;
                border-radius: 4px;
                border: none;
                position: relative;
                font-size: 15px;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 130, 0.5);
            }
        """)

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(500, 10, 61, 41))
        self.label_10.setObjectName("label_10")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(890, 60, 201, 22))
        self.comboBox_2.setObjectName("comboBox_2")

        self.comboBox_2.addItem("All")
        self.comboBox_2.addItem("Account Live")
        self.comboBox_2.addItem("Account Die")

        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(110, 90, 131, 22))
        self.comboBox_3.setObjectName("comboBox_3")

        self.comboBox_3.addItem("Capsolver")
        self.comboBox_3.addItem("2Captcha")

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(520, 50, 211, 31))
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(520, 80, 211, 31))
        self.checkBox_2.setObjectName("checkBox_2")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(810, 50, 71, 41))
        self.label_11.setObjectName("label_11")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(310, 20, 160, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
            QPushButton {
                background-color: #005af0;
                color: #ffffff;
                border: none;
                outline: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #005af0;
                border: 1px solid #005af0;
            }
        """)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_4.clicked.connect(self.upload_file)
        self.pushButton_3.clicked.connect(self.export_file)
        self.pushButton.clicked.connect(self.start_threads)
        self.pushButton_2.clicked.connect(self.handle_checkbox)

        
        # self.populate_table(data)
        self.threads = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tool Check Account Sum6"))
        MainWindow.setWindowIcon(QIcon("logo.png"))
        self.label_2.setText(_translate("MainWindow", "Thread"))
        self.label_12.setText(_translate("MainWindow", "solve captchas"))
        self.label_3.setText(_translate("MainWindow", "Open file"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label_4.setText(_translate("MainWindow", "Number of accounts:"))
        self.label_5.setText(_translate("MainWindow", "0"))
        self.label_6.setText(_translate("MainWindow", "🟢:"))
        self.label_7.setText(_translate("MainWindow", "🔴:"))
        self.label_live.setText(_translate("MainWindow", "0"))
        self.label_die.setText(_translate("MainWindow", "0"))
        self.pushButton_2.setText(_translate("MainWindow", "filter"))
        self.checkBox.setText(_translate("MainWindow", "Filter gold from high to low"))
        self.checkBox_2.setText(_translate("MainWindow", "Filter Két from high to low"))
        self.pushButton_3.setText(_translate("MainWindow", "Export file"))
        self.label_10.setText(_translate("MainWindow", "Filter data"))
        self.label_11.setText(_translate("MainWindow", "Export data"))
        self.pushButton_4.setText(_translate("MainWindow", "Choose File"))

    def run(self,account):
        with self.file_lock:
            print("Worker thread started")
            data = Main.run(account)
            self.populate_table(data)
            print("Worker thread finished")
        self.finished.emit()

    def start_threads(self):
        if self.lineEdit.text() == "": 
            return QMessageBox.warning(self.centralwidget, "Upload File", "Vui lòng upload file trước khi chạy!") 
        selected_value = self.comboBox_3.currentText() #solve captcha value
        file_name = 'account.txt'
        accounts = self.read_accounts(file_name)
        if len(self.worker_threads) == 0:
            return QMessageBox.warning(self.centralwidget, "Error", "No worker threads available to process.")
        
        chunk_size = len(accounts) // len(self.worker_threads)
        chunks = [accounts[i:i + chunk_size] for i in range(0, len(accounts), chunk_size)]

        for chunk, worker_thread in zip(chunks, self.worker_threads):
            thread = WorkerThread(chunk, self, worker_thread.mutex)
            thread.finished.connect(self.handle_thread_finished)
            thread.start()

    def closeEvent(self, event):
        for thread in self.threads:
            thread.quit()
            thread.wait()
        event.accept()

    def handle_thread_finished(self, thread_id):
        print(f"Worker thread {thread_id} completed")

        all_threads_completed = all(thread.isFinished() for thread in self.threads)
        if all_threads_completed:
            print("All threads have completed")

    def remove_invalid_characters(self,text):
   
        invalid_characters = ['Ä', 'Ă', 'Đ', 'Vá»', 'á»']
        for char in invalid_characters:
            text = text.replace(char, '')
        return text

    def read_accounts(self,file_name):
        with open(file_name, "r", encoding='utf-8') as file:
            accounts = []
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 2:
                    username = parts[0]
                    password = parts[1]
                    username = self.remove_invalid_characters(username)
                    password = self.remove_invalid_characters(password)
                    accounts.append((username, password))
            return list(set(tuple(account) for account in accounts))

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(None, "Choose File", "", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;Word Files (*.doc *.docx)", options=options)
        if file_name:
            self.read_data(file_name)

    def read_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read().strip()  
                if not data:  
                    raise ValueError("Dữ liệu file đầu vào trống.")
                
                pairs = [line.split('|') for line in data.splitlines()]
                
                for pair in pairs:
                    if len(pair) != 2:
                        raise ValueError("Dữ liệu file đầu vào không hợp lệ. Vui lòng kiểm tra lại.")
                
                self.lineEdit_1.setText(str(len(pairs)))
                self.lineEdit.setText(file_path)
                self.label_5.setText(str(len(pairs)))
        except Exception as e:
            self.label_5.setText("0")
            self.lineEdit_1.setText("0")
            self.lineEdit.setText("")
            QMessageBox.warning(self.centralwidget, "File format error", str(e))

    def populate_table(self, data):
        # self.tableWidget_2.setRowCount(0)

        for row_number, row_data in enumerate(data):
            self.tableWidget_2.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                if row_number % 2 == 0:
                    item.setBackground(QColor(240, 240, 240))
                self.tableWidget_2.setItem(row_number, column_number, item)

        true_count, false_count = self.count_status_data()

        self.label_live.setText(str(true_count))
        self.label_die.setText(str(false_count))

    def get_status_data(self):
        status_data = []  
        total_rows = self.tableWidget_2.rowCount()
        status_column = 5  

        for row in range(total_rows):
            item = self.tableWidget_2.item(row, status_column)
            if item is not None:  
                status_data.append(item.text())

        return status_data
    
    def count_status_data(self):
        status_data = self.get_status_data()  
        true_count = status_data.count("true")
        false_count = status_data.count("false")
        return true_count, false_count
    
    def handle_checkbox(self):
        if self.checkBox.isChecked():  
            self.sort_rows_by_gold()  
        if self.checkBox_2.isChecked():  
            self.sort_rows_by_chip()
    
    def sort_rows_by_gold(self):
        gold_data = []  
        temp_items = [] 
        for row in range(self.tableWidget_2.rowCount()):
            gold_item = self.tableWidget_2.item(row, 2)  
            if gold_item:
                gold_value = int(gold_item.text())  
                gold_data.append((gold_value, row)) 
                temp_items.append([self.tableWidget_2.takeItem(row, col) for col in range(self.tableWidget_2.columnCount())])

        sorted_gold_data = sorted(gold_data, key=lambda x: x[0], reverse=True)  
        for index, (_, row) in enumerate(sorted_gold_data):
            for column, item in enumerate(temp_items[row]):
                self.tableWidget_2.setItem(index, column, item)  

        for items in temp_items:
            for item in items:
                if item:
                    item = None

    def sort_rows_by_chip(self):
        chip_data = []  
        temp_items = []  
        for row in range(self.tableWidget_2.rowCount()):
            chip_item = self.tableWidget_2.item(row, 3) 
            if chip_item:
                chip_value = int(chip_item.text())  
                chip_data.append((chip_value, row))  
                temp_items.append([self.tableWidget_2.takeItem(row, col) for col in range(self.tableWidget_2.columnCount())])

        sorted_chip_data = sorted(chip_data, key=lambda x: x[0], reverse=True) 
        for index, (_, row) in enumerate(sorted_chip_data):
            for column, item in enumerate(temp_items[row]):
                self.tableWidget_2.setItem(index, column, item)  

        for items in temp_items:
            for item in items:
                if item:
                    item = None

    def export_file(self):
        selected_value = self.comboBox_2.currentText()
        actions = {
            "All": lambda: self.export_table_data(self.tableWidget_2, "table_data.txt"),
            "Account Live": lambda: self.export_table_data_live(self.tableWidget_2, "table_data.txt"),
            "Account Die": lambda: self.export_table_data_die(self.tableWidget_2, "table_data.txt")
        }

        action = actions.get(selected_value, lambda: print("Unknown selection"))
        action()

    def get_table_data(self, table_widget):
        data = []

        for row in range(table_widget.rowCount()):
            row_data = []
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    def export_table_data(self, table_widget, file_path):
        data = self.get_table_data(table_widget)
        
        if not data:
            self.Notification("ERROR", "Empty data. File not exported.")
            return

        with open(file_path, "w") as file:
            for row in data:
                tt = "\t".join(row)
                formatted_row = "|".join(tt.split())
                file.write(formatted_row + "\n")

        
        self.Notification("SUCCESS","export file successfully")

    def export_table_data_live(self, table_widget, file_path):
        data = self.get_table_data(table_widget)
        
        if not data:
            self.Notification("ERROR", "Empty data. File not exported.")
            return

        with open(file_path, "w") as file:
            for row in data:
                if row[5].lower() == "true":
                    tt = "\t".join(row)
                    formatted_row = "|".join(tt.split())
                    file.write(formatted_row + "\n")

        self.Notification("SUCCESS","export file successfully")

    def export_table_data_die(self, table_widget, file_path):
        data = self.get_table_data(table_widget)
        
        if not data:
            self.Notification("ERROR", "Empty data. File not exported.")
            return

        with open(file_path, "w") as file:
            for row in data:
                if row[5].lower() == "false":
                    tt = "\t".join(row)
                    formatted_row = "|".join(tt.split())
                    file.write(formatted_row + "\n")
                    
        self.Notification("SUCCESS","export file successfully")

    def Notification(self,type,text):
        QMessageBox.information(self.centralwidget, type, text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1108, 703) 
    window.show()
    sys.exit(app.exec_())