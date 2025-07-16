import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QLineEdit, QDateEdit, QMessageBox, QComboBox,
                            QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QDialog)
from PyQt5.QtCore import Qt, QDate
from styles import COLORS, COMMON_STYLES, FORM_STYLES

class BudgetManagementPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bütçe Yönetimi')
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
        title_label = QLabel('Bütçe Yönetimi')
        title_label.setStyleSheet('color: white; font-size: 28px; font-weight: bold;')
        
        # Yeni Bütçe butonu
        add_button = QPushButton('+ Yeni Bütçe')
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
        add_button.clicked.connect(self.show_new_budget_dialog)
        
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
        
        # Özet bilgiler
        summary_widget = QWidget()
        summary_widget.setFixedHeight(100)
        summary_widget.setStyleSheet("background-color: white;")
        summary_layout = QHBoxLayout(summary_widget)
        
        # Toplam Bütçe
        total_budget_widget = QWidget()
        total_budget_layout = QVBoxLayout(total_budget_widget)
        total_budget_label = QLabel('Toplam Bütçe')
        total_budget_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1565C0;")
        self.total_budget_amount = QLabel('0,00 TL')
        self.total_budget_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #1565C0;")
        total_budget_layout.addWidget(total_budget_label)
        total_budget_layout.addWidget(self.total_budget_amount)
        
        # Kullanılan Bütçe
        used_budget_widget = QWidget()
        used_budget_layout = QVBoxLayout(used_budget_widget)
        used_budget_label = QLabel('Kullanılan Bütçe')
        used_budget_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #C62828;")
        self.used_budget_amount = QLabel('0,00 TL')
        self.used_budget_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #C62828;")
        used_budget_layout.addWidget(used_budget_label)
        used_budget_layout.addWidget(self.used_budget_amount)
        
        # Kalan Bütçe
        remaining_budget_widget = QWidget()
        remaining_budget_layout = QVBoxLayout(remaining_budget_widget)
        remaining_budget_label = QLabel('Kalan Bütçe')
        remaining_budget_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        self.remaining_budget_amount = QLabel('0,00 TL')
        self.remaining_budget_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        remaining_budget_layout.addWidget(remaining_budget_label)
        remaining_budget_layout.addWidget(self.remaining_budget_amount)
        
        summary_layout.addWidget(total_budget_widget)
        summary_layout.addWidget(used_budget_widget)
        summary_layout.addWidget(remaining_budget_widget)
        
        # Bütçe tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Bütçe Dönemi', 'Başlangıç Tarihi', 'Bitiş Tarihi', 
                                            'Bütçe Tutarı', 'Kullanılan', 'Kalan', 'İşlemler'])
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
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 100)
        
        layout.addWidget(title_bar)
        layout.addWidget(summary_widget)
        layout.addWidget(self.table)
        
        # Veritabanı bağlantısı ve tablo oluşturma
        self.create_database()
        # Verileri tabloya yükle
        self.load_budget_data()
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_management (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                budget_amount REAL NOT NULL,
                used_amount REAL DEFAULT 0,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def load_budget_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT period, start_date, end_date, budget_amount, used_amount, category
            FROM budget_management
            ORDER BY start_date DESC
        ''')
        data = cursor.fetchall()
        
        total_budget = 0
        total_used = 0
        
        self.table.setRowCount(len(data))
        for row, (period, start_date, end_date, budget, used, category) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(period))
            self.table.setItem(row, 1, QTableWidgetItem(start_date))
            self.table.setItem(row, 2, QTableWidgetItem(end_date))
            self.table.setItem(row, 3, QTableWidgetItem(f"{budget:,.2f} TL"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{used:,.2f} TL"))
            remaining = budget - used
            self.table.setItem(row, 5, QTableWidgetItem(f"{remaining:,.2f} TL"))
            
            total_budget += budget
            total_used += used
            
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
            
            self.table.setCellWidget(row, 6, actions_widget)
        
        # Özet bilgileri güncelle
        self.total_budget_amount.setText(f"{total_budget:,.2f} TL")
        self.used_budget_amount.setText(f"{total_used:,.2f} TL")
        self.remaining_budget_amount.setText(f"{total_budget - total_used:,.2f} TL")
        
        conn.close()
    
    def show_new_budget_dialog(self):
        dialog = NewBudgetDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_budget_data()

class NewBudgetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bütçe Kaydı')
        self.setFixedSize(800, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Bütçe Dönemi:', QComboBox()),
            ('Başlangıç Tarihi:', QDateEdit()),
            ('Bitiş Tarihi:', QDateEdit()),
            ('Bütçe Tutarı:', QLineEdit()),
            ('Kategori:', QComboBox()),
            ('Açıklama:', QLineEdit())
        ]
        
        for label_text, widget in fields:
            field_container = QWidget()
            field_layout = QHBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                if label_text == 'Bütçe Dönemi:':
                    widget.addItems(['Aylık', 'Üç Aylık', 'Yıllık', 'Özel Dönem'])
                elif label_text == 'Kategori:':
                    widget.addItems(['Genel Bütçe', 'Departman Bütçesi', 'Proje Bütçesi', 'Yatırım Bütçesi'])
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
                widget.setDisplayFormat("dd.MM.yyyy")
            elif isinstance(widget, QLineEdit):
                if label_text == 'Bütçe Tutarı:':
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
            
            if label_text == 'Bütçe Dönemi:':
                self.period = widget
            elif label_text == 'Başlangıç Tarihi:':
                self.start_date = widget
            elif label_text == 'Bitiş Tarihi:':
                self.end_date = widget
            elif label_text == 'Bütçe Tutarı:':
                self.amount = widget
            elif label_text == 'Kategori:':
                self.category = widget
            elif label_text == 'Açıklama:':
                self.description = widget
        
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
        save_button.clicked.connect(self.save_budget)
        
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
    
    def save_budget(self):
        # Veri doğrulama
        if not self.amount.text():
            QMessageBox.warning(self, "Hata", "Bütçe tutarı boş bırakılamaz!")
            return
        
        try:
            amount = float(self.amount.text().replace(',', '.').replace('TL', '').strip())
            if amount <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir bütçe tutarı giriniz!")
            return
        
        # Veritabanına kaydet
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO budget_management (
                period, start_date, end_date, budget_amount, category, description
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.period.currentText(),
            self.start_date.date().toString("yyyy-MM-dd"),
            self.end_date.date().toString("yyyy-MM-dd"),
            amount,
            self.category.currentText(),
            self.description.text()
        ))
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Başarılı", "Bütçe kaydı başarıyla oluşturuldu!")
        self.accept()