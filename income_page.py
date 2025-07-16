from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QDialog, QLineEdit, QComboBox,
                            QDateEdit, QScrollArea)
from PyQt5.QtCore import Qt, QDate
import sqlite3

class IncomeTransactionsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gelir İşlemleri')
        self.setWindowFlags(Qt.FramelessWindowHint)  # Çerçevesiz pencere
        self.setWindowState(Qt.WindowMaximized)  # Tam ekran
        self.setStyleSheet('background-color: #FFF5E6;')
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Kenar boşluklarını kaldır
        layout.setSpacing(0)
        
        # Başlık çubuğu
        title_bar = QWidget()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet('background-color: #D94E1F;')
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 0, 0)
        
        # Geri dönme butonu
        back_button = QPushButton('←')
        back_button.setFixedSize(50, 50)
        back_button.setStyleSheet("""
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
        back_button.clicked.connect(self.close)
        
        # Başlık etiketi
        title_label = QLabel('Gelir İşlemleri')
        title_label.setStyleSheet('color: white; font-size: 24px; font-weight: bold;')
        
        # Kapatma butonu
        close_button = QPushButton('×')
        close_button.setFixedSize(50, 50)
        close_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 20px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        close_button.clicked.connect(self.close)
        
        title_layout.addWidget(back_button)  # Geri dönme butonu eklendi
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_button)
        
        # İçerik alanı
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Butonlar için widget
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # Yeni Gelir Ekle butonu
        add_button = QPushButton('+ Yeni Gelir Ekle')
        add_button.setFixedSize(150, 40)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        add_button.clicked.connect(self.add_income)
        
        button_layout.addWidget(add_button)
        button_layout.addStretch()
        
        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Tarih', 'Kategori', 'Açıklama', 'Tutar', 'Durum'])
        
        # Tablo stilini ayarla
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #D94E1F;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #FFE0E0;
            }
            QTableWidget::item:selected {
                background-color: #FFE0E0;
                color: #D94E1F;
            }
        """)
        
        # Sütun genişliklerini ayarla
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tarih
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Kategori
        header.setSectionResizeMode(3, QHeaderView.Stretch)          # Açıklama
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Tutar
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Durum
        
        # Dikey başlıkları gizle
        self.table.verticalHeader().setVisible(False)
        
        # Layout'a widget'ları ekle
        content_layout.addWidget(button_widget)
        content_layout.addWidget(self.table)
        
        # Ana layout'a widget'ları ekle
        layout.addWidget(title_bar)
        layout.addWidget(content_widget)
        
        # Veritabanını oluştur ve verileri yükle
        self.create_database()
        self.load_data()
        
        # Pencere sürükleme için değişken
        self.dragPos = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS income_transactions (
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
    
    def load_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM income_transactions ORDER BY date DESC')
        data = cursor.fetchall()
        
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if j == 4:  # Tutar sütunu için para birimi ekle
                    item = QTableWidgetItem(f"{value:.2f} TL")
                self.table.setItem(i, j, item)
        
        conn.close()
    
    def add_income(self):
        dialog = AddIncomeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

class AddIncomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Gelir Ekle')
        self.setFixedSize(600, 700)  # Pencere boyutunu büyüttüm
        self.setStyleSheet('background-color: #FFF5E6;')
        
        # Ana scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #FFF5E6;
            }
            QScrollBar:vertical {
                border: none;
                background: #FFF5E6;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #D94E1F;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Ana widget ve layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Başlık
        title_label = QLabel('Yeni Gelir Ekle')
        title_label.setStyleSheet('color: #D94E1F; font-size: 28px; font-weight: bold;')
        title_label.setAlignment(Qt.AlignCenter)
        
        # Form alanları
        # Tarih alanı
        date_label = QLabel('Tarih:')
        date_label.setStyleSheet('color: #D94E1F; font-size: 18px; font-weight: bold;')
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                min-height: 50px;
            }
        """)
        
        # Kategori alanı
        category_label = QLabel('Kategori:')
        category_label.setStyleSheet('color: #D94E1F; font-size: 18px; font-weight: bold;')
        self.category_combo = QComboBox()
        self.category_combo.addItems(['Satış Geliri', 'Kira Geliri', 'Faiz Geliri', 'Diğer'])
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                min-height: 50px;
            }
        """)
        
        # Açıklama alanı
        description_label = QLabel('Açıklama:')
        description_label.setStyleSheet('color: #D94E1F; font-size: 18px; font-weight: bold;')
        self.description_edit = QLineEdit()
        self.description_edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                min-height: 50px;
            }
        """)
        
        # Tutar alanı
        amount_label = QLabel('Tutar (TL):')
        amount_label.setStyleSheet('color: #D94E1F; font-size: 18px; font-weight: bold;')
        self.amount_edit = QLineEdit()
        self.amount_edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                min-height: 50px;
            }
        """)
        
        # Durum alanı
        status_label = QLabel('Durum:')
        status_label.setStyleSheet('color: #D94E1F; font-size: 18px; font-weight: bold;')
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Beklemede', 'Tahsil Edildi'])
        self.status_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                min-height: 50px;
            }
        """)
        
        # Kaydet butonu
        save_button = QPushButton('Kaydet')
        save_button.setFixedHeight(60)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        save_button.clicked.connect(self.save_income)
        
        # Layout'a widget'ları ekle
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(date_label)
        layout.addWidget(self.date_edit)
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)
        layout.addWidget(description_label)
        layout.addWidget(self.description_edit)
        layout.addWidget(amount_label)
        layout.addWidget(self.amount_edit)
        layout.addWidget(status_label)
        layout.addWidget(self.status_combo)
        layout.addSpacing(20)
        layout.addWidget(save_button)
        
        # Scroll area'ya ana widget'ı ekle
        scroll.setWidget(main_widget)
        
        # Dialog layout
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(scroll)
    
    def save_income(self):
        try:
            date = self.date_edit.date().toString('yyyy-MM-dd')
            category = self.category_combo.currentText()
            description = self.description_edit.text()
            amount = float(self.amount_edit.text())
            status = self.status_combo.currentText()
            
            conn = sqlite3.connect('finance.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO income_transactions (date, category, description, amount, status)
            VALUES (?, ?, ?, ?, ?)
            ''', (date, category, description, amount, status))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, 'Başarılı', 'Gelir kaydı başarıyla eklendi.')
            self.accept()
            
        except ValueError:
            QMessageBox.warning(self, 'Hata', 'Lütfen geçerli bir tutar giriniz.')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')