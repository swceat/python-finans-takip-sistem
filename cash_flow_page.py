import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from styles import COLORS, COMMON_STYLES, FORM_STYLES

class CashFlowPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nakit Akışı')
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
        title_label = QLabel('Nakit Akışı')
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
        
        # Toplam Gelir
        total_income_widget = QWidget()
        total_income_layout = QVBoxLayout(total_income_widget)
        total_income_label = QLabel('Toplam Gelir')
        total_income_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        self.total_income_amount = QLabel('0,00 TL')
        self.total_income_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        total_income_layout.addWidget(total_income_label)
        total_income_layout.addWidget(self.total_income_amount)
        
        # Toplam Gider
        total_expense_widget = QWidget()
        total_expense_layout = QVBoxLayout(total_expense_widget)
        total_expense_label = QLabel('Toplam Gider')
        total_expense_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #C62828;")
        self.total_expense_amount = QLabel('0,00 TL')
        self.total_expense_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #C62828;")
        total_expense_layout.addWidget(total_expense_label)
        total_expense_layout.addWidget(self.total_expense_amount)
        
        # Net Nakit Akışı
        net_cash_widget = QWidget()
        net_cash_layout = QVBoxLayout(net_cash_widget)
        net_cash_label = QLabel('Net Nakit Akışı')
        net_cash_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1565C0;")
        self.net_cash_amount = QLabel('0,00 TL')
        self.net_cash_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #1565C0;")
        net_cash_layout.addWidget(net_cash_label)
        net_cash_layout.addWidget(self.net_cash_amount)
        
        summary_layout.addWidget(total_income_widget)
        summary_layout.addWidget(total_expense_widget)
        summary_layout.addWidget(net_cash_widget)
        
        # Nakit akışı tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Tür', 'Açıklama', 'Tutar', 'Durum'])
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
        
        layout.addWidget(title_bar)
        layout.addWidget(summary_widget)
        layout.addWidget(self.table)
        
        # Verileri yükle
        self.load_cash_flow_data()
    
    def load_cash_flow_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Gelir ve gider verilerini birleştir
        cursor.execute('''
            SELECT 
                date,
                'Gelir' as type,
                description,
                amount,
                status
            FROM income_transactions
            UNION ALL
            SELECT 
                date,
                'Gider' as type,
                description,
                -amount as amount,
                status
            FROM expense_transactions
            ORDER BY date DESC
        ''')
        data = cursor.fetchall()
        
        # Toplam değerleri hesapla
        total_income = 0
        total_expense = 0
        
        self.table.setRowCount(len(data))
        for row, (date, type_, description, amount, status) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(type_))
            self.table.setItem(row, 2, QTableWidgetItem(description))
            
            # Tutarı formatlı göster ve renklendirme yap
            amount_item = QTableWidgetItem(f"{abs(amount):,.2f} TL")
            if amount > 0:
                amount_item.setForeground(Qt.darkGreen)
                total_income += amount
            else:
                amount_item.setForeground(Qt.darkRed)
                total_expense += abs(amount)
            self.table.setItem(row, 3, amount_item)
            
            self.table.setItem(row, 4, QTableWidgetItem(status))
        
        # Özet bilgileri güncelle
        self.total_income_amount.setText(f"{total_income:,.2f} TL")
        self.total_expense_amount.setText(f"{total_expense:,.2f} TL")
        net_cash = total_income - total_expense
        self.net_cash_amount.setText(f"{net_cash:,.2f} TL")
        
        conn.close()