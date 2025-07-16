import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                            QDialog, QComboBox, QMessageBox)

class NewReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Finansal Rapor')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Rapor Türü:', QComboBox()),
            ('Başlangıç Tarihi:', QDateEdit()),
            ('Bitiş Tarihi:', QDateEdit()),
            ('Rapor Başlığı:', QLineEdit()),
            ('Açıklama:', QLineEdit())
        ]
        
        for label_text, widget in fields:
            field_container = QWidget()
            field_layout = QHBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(label_text)
            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 120px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Aylık Rapor', 'Üç Aylık Rapor', 'Yıllık Rapor',
                               'Özel Dönem Raporu', 'Karşılaştırmalı Rapor'])
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            elif isinstance(widget, QLineEdit):
                widget.setPlaceholderText(f'{label_text[:-1]} giriniz...')
            
            widget.setStyleSheet("""
                QLineEdit, QDateEdit, QComboBox {
                    padding: 8px;
                    border: 2px solid #D94E1F;
                    border-radius: 8px;
                    font-size: 14px;
                    min-width: 200px;
                    background-color: white;
                }
                QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                    border-color: #B33D15;
                }
            """)
            
            field_layout.addWidget(widget)
            layout.addWidget(field_container)
            
            if label_text == 'Rapor Türü:':
                self.report_type = widget
            elif label_text == 'Başlangıç Tarihi:':
                self.start_date = widget
            elif label_text == 'Bitiş Tarihi:':
                self.end_date = widget
            elif label_text == 'Rapor Başlığı:':
                self.title = widget
            elif label_text == 'Açıklama:':
                self.description = widget
        
        # Butonlar
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        save_button = QPushButton('Rapor Oluştur')
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton('İptal')
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addWidget(button_container)

class FinancialReportsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Finansal Raporlar')
        self.setFixedSize(800, 600)
        
        # Veritabanı bağlantısı
        self.create_database()
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Başlık
        title_label = QLabel('Finansal Raporlar')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #D94E1F;')
        title_label.setAlignment(Qt.AlignCenter)
        
        # Rapor türü seçimi
        type_layout = QHBoxLayout()
        type_label = QLabel('Rapor Türü:')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['Gelir Raporu', 'Gider Raporu', 'Nakit Akışı Raporu', 'Bilanço Raporu'])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        
        # Yeni rapor butonu
        new_report_button = QPushButton('Yeni Rapor Oluştur')
        new_report_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        new_report_button.clicked.connect(self.create_new_report)
        type_layout.addWidget(new_report_button)
        
        # Rapor tablosu
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(['Rapor ID', 'Rapor Türü', 'Tarih', 'İşlemler'])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Layout'a widget'ları ekle
        layout.addWidget(title_label)
        layout.addLayout(type_layout)
        layout.addWidget(self.report_table)
        
        # Raporları yükle
        self.load_reports()
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            report_date TEXT NOT NULL,
            report_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()
    
    def load_reports(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM financial_reports ORDER BY created_at DESC')
        reports = cursor.fetchall()
        
        self.report_table.setRowCount(len(reports))
        for i, report in enumerate(reports):
            self.report_table.setItem(i, 0, QTableWidgetItem(str(report[0])))
            self.report_table.setItem(i, 1, QTableWidgetItem(report[1]))
            self.report_table.setItem(i, 2, QTableWidgetItem(report[2]))
            
            # İşlem butonları
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            
            view_button = QPushButton('Görüntüle')
            download_button = QPushButton('İndir')
            delete_button = QPushButton('Sil')
            
            for button in [view_button, download_button, delete_button]:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #D94E1F;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #B33D15;
                    }
                """)
                actions_layout.addWidget(button)
            
            self.report_table.setCellWidget(i, 3, actions_widget)
        
        conn.close()
    
    def create_new_report(self):
        # Yeni rapor oluşturma işlemi
        report_type = self.type_combo.currentText()
        # Rapor oluşturma işlemleri burada yapılacak
        QMessageBox.information(self, 'Başarılı', 'Yeni rapor oluşturuldu!')
        self.load_reports()