import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QLineEdit, QDateEdit, QMessageBox, QComboBox,
                            QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QDialog)
from PyQt5.QtCore import Qt, QDate
from styles import COLORS, COMMON_STYLES, FORM_STYLES
from utils import Utils

class ExpenseTransactionsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gider İşlemleri')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF5E6;
            }
        """)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Başlık çubuğu
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet("background-color: #D94E1F;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)
        
        # Geri dönme butonu
        back_button = QPushButton('←')
        back_button.setFixedSize(50, 50)
        back_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 28px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #B33D15;
                border-radius: 25px;
            }
        """)
        back_button.clicked.connect(self.close)
        
        # Başlık etiketi
        title_label = QLabel('Gider İşlemleri')
        title_label.setStyleSheet('color: white; font-size: 28px; font-weight: bold;')
        
        # Yeni Gider butonu
        add_button = QPushButton('+ Yeni Gider')
        add_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #D94E1F;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFE0E0;
            }
        """)
        add_button.clicked.connect(self.show_new_expense_dialog)
        
        # Kapatma butonu
        close_button = QPushButton('×')
        close_button.setFixedSize(60, 60)
        close_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 24px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        close_button.clicked.connect(self.close)
        
        title_layout.addWidget(back_button)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(add_button)
        title_layout.addWidget(close_button)
        
        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Kategori', 'Açıklama', 'Tutar', 'Durum', 'İşlemler'])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #D94E1F;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #FFE0E0;
            }
        """)
        
        # Tablo sütunlarını otomatik genişlet
        header = self.table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 100)
        
        layout.addWidget(title_bar)
        layout.addWidget(self.table)
        
        # Veritabanı bağlantısı ve tablo oluşturma
        self.create_database()
        # Verileri tabloya yükle
        self.load_expense_data()
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def load_expense_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT date, category, description, amount, status FROM expense_transactions')
        data = cursor.fetchall()
        
        self.table.setRowCount(len(data))
        for row, (date, category, description, amount, status) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(category))
            self.table.setItem(row, 2, QTableWidgetItem(description))
            self.table.setItem(row, 3, QTableWidgetItem(f"{amount:,.2f} TL"))
            self.table.setItem(row, 4, QTableWidgetItem(status))
            
            # İşlem butonları için widget
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            
            edit_button = QPushButton('✏️')
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #FFE0E0;
                    border-radius: 5px;
                }
            """)
            
            delete_button = QPushButton('🗑️')
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #FFE0E0;
                    border-radius: 5px;
                }
            """)
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, 5, actions_widget)
        
        conn.close()
    
    def show_new_expense_dialog(self):
        dialog = NewExpenseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_expense_data()

class NewExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Gider Kaydı')
        self.setFixedSize(800, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Kategori:', QComboBox()),
            ('Açıklama:', QLineEdit()),
            ('Tutar:', QLineEdit()),
            ('Durum:', QComboBox())
        ]
        
        for label_text, widget in fields:
            field_container = QWidget()
            field_layout = QHBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                if label_text == 'Kategori:':
                    widget.addItems(['Personel Giderleri', 'Kira Giderleri', 'Elektrik/Su/Doğalgaz', 
                                   'Malzeme Alımları', 'Ulaşım Giderleri', 'Diğer'])
                elif label_text == 'Durum:':
                    widget.addItems(['Ödendi', 'Beklemede', 'İptal Edildi'])
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
                widget.setDisplayFormat("dd.MM.yyyy")
            elif isinstance(widget, QLineEdit):
                if label_text == 'Tutar:':
                    widget.setPlaceholderText('0,00 TL')
                else:
                    widget.setPlaceholderText(f'{label_text[:-1]} giriniz...')
            
            widget.setStyleSheet("""
                QLineEdit, QDateEdit, QComboBox {
                    padding: 8px;
                    border: 2px solid #D94E1F;
                    border-radius: 8px;
                    font-size: 14px;
                    min-width: 300px;
                }
            """)
            
            field_layout.addWidget(widget)
            layout.addWidget(field_container)
            
            if label_text == 'Tarih:':
                self.date = widget
            elif label_text == 'Kategori:':
                self.category = widget
            elif label_text == 'Açıklama:':
                self.description = widget
            elif label_text == 'Tutar:':
                self.amount = widget
            elif label_text == 'Durum:':
                self.status = widget
        
        # Butonlar
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        save_button = QPushButton('Kaydet')
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        save_button.clicked.connect(self.save_expense)
        
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
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addWidget(button_container)
    
    def save_expense(self):
        # Veri doğrulama
        if not self.amount.text():
            QMessageBox.warning(self, "Hata", "Tutar boş bırakılamaz!")
            return
        
        try:
            amount = float(self.amount.text().replace(',', '.').replace('TL', '').strip())
            if amount <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir tutar giriniz!")
            return
        
        # Veritabanına kaydet
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expense_transactions (date, category, description, amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.date.date().toString("yyyy-MM-dd"),
            self.category.currentText(),
            self.description.text(),
            amount,
            self.status.currentText()
        ))
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Başarılı", "Gider kaydı başarıyla oluşturuldu!")
        self.accept()