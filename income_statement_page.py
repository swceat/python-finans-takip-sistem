import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                            QDialog, QDateEdit, QLineEdit, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from styles import COLORS, COMMON_STYLES, FORM_STYLES

class IncomeStatementPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gelir Tablosu')
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
        title_label = QLabel('Gelir Tablosu')
        title_label.setStyleSheet('color: white; font-size: 28px; font-weight: bold;')
        
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
        title_layout.addWidget(close_button)
        
        # Özet bilgiler
        summary_widget = QWidget()
        summary_widget.setFixedHeight(100)
        summary_widget.setStyleSheet("background-color: white;")
        summary_layout = QHBoxLayout(summary_widget)
        
        # Toplam Gelirler
        total_income_widget = QWidget()
        total_income_layout = QVBoxLayout(total_income_widget)
        total_income_label = QLabel('Toplam Gelirler')
        total_income_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        self.total_income_amount = QLabel('0,00 TL')
        self.total_income_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        total_income_layout.addWidget(total_income_label)
        total_income_layout.addWidget(self.total_income_amount)
        
        # Toplam Giderler
        total_expenses_widget = QWidget()
        total_expenses_layout = QVBoxLayout(total_expenses_widget)
        total_expenses_label = QLabel('Toplam Giderler')
        total_expenses_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #C62828;")
        self.total_expenses_amount = QLabel('0,00 TL')
        self.total_expenses_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #C62828;")
        total_expenses_layout.addWidget(total_expenses_label)
        total_expenses_layout.addWidget(self.total_expenses_amount)
        
        # Net Kar/Zarar
        net_profit_widget = QWidget()
        net_profit_layout = QVBoxLayout(net_profit_widget)
        net_profit_label = QLabel('Net Kar/Zarar')
        net_profit_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1565C0;")
        self.net_profit_amount = QLabel('0,00 TL')
        self.net_profit_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #1565C0;")
        net_profit_layout.addWidget(net_profit_label)
        net_profit_layout.addWidget(self.net_profit_amount)
        
        summary_layout.addWidget(total_income_widget)
        summary_layout.addWidget(total_expenses_widget)
        summary_layout.addWidget(net_profit_widget)
        
        # Gelir tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Hesap', 'Tutar'])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #D94E1F;
                color: white;
                padding: 12px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #E0E0E0;
            }
            QTableWidget::item:selected {
                background-color: #FFE0E0;
            }
        """)
        
        # Tablo sütunlarını otomatik genişlet
        header = self.table.horizontalHeader()
        for i in range(2):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        layout.addWidget(title_bar)
        layout.addWidget(summary_widget)
        layout.addWidget(self.table)
        
        # Veritabanı tablosunu oluştur
        self.create_database()
        
        # Verileri yükle
        self.load_income_statement_data()
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Gelir tablosu kategorileri tablosunu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income_statement_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES income_statement_categories (id)
            )
        ''')
        
        # Varsayılan kategorileri ekle
        default_categories = [
            ('GELİRLER', 'income', None),
            ('Satış Gelirleri', 'income', 1),
            ('Diğer Gelirler', 'income', 1),
            ('GİDERLER', 'expense', None),
            ('Satışların Maliyeti', 'expense', 4),
            ('Faaliyet Giderleri', 'expense', 4),
            ('Pazarlama Giderleri', 'expense', 4),
            ('Genel Yönetim Giderleri', 'expense', 4),
            ('Finansman Giderleri', 'expense', 4)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO income_statement_categories (name, type, parent_id)
            VALUES (?, ?, ?)
        ''', default_categories)
        
        conn.commit()
        conn.close()
    
    def load_income_statement_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Gelirleri hesapla
        cursor.execute('SELECT SUM(amount) FROM income_transactions')
        total_income = cursor.fetchone()[0] or 0
        self.total_income_amount.setText(f"{total_income:,.2f} TL")
        
        # Giderleri hesapla
        cursor.execute('SELECT SUM(amount) FROM expense_transactions')
        total_expenses = cursor.fetchone()[0] or 0
        self.total_expenses_amount.setText(f"{total_expenses:,.2f} TL")
        
        # Net kar/zararı hesapla
        net_profit = total_income - total_expenses
        self.net_profit_amount.setText(f"{net_profit:,.2f} TL")
        
        # Gelir tablosu verilerini yükle
        cursor.execute('SELECT name FROM income_statement_categories ORDER BY id')
        categories = cursor.fetchall()
        
        self.table.setRowCount(len(categories))
        
        for row, (category,) in enumerate(categories):
            # Kategori adı
            self.table.setItem(row, 0, QTableWidgetItem(category))
            
            # Kategori tutarı
            if category == 'GELİRLER':
                amount = total_income
            elif category == 'GİDERLER':
                amount = total_expenses
            else:
                # Alt kategoriler için detaylı hesaplama yapılabilir
                amount = 0
            
            amount_item = QTableWidgetItem(f"{amount:,.2f} TL")
            self.table.setItem(row, 1, amount_item)
            
            # Ana başlıkları kalın yap
            if not category.startswith('   '):
                font = self.table.item(row, 0).font()
                font.setBold(True)
                self.table.item(row, 0).setFont(font)
                self.table.item(row, 1).setFont(font)
                self.table.item(row, 0).setBackground(Qt.lightGray)
                self.table.item(row, 1).setBackground(Qt.lightGray)
        
        conn.close()