import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                            QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate  # Added QDate import
from PyQt5.QtGui import QPainter, QColor
from styles import COLORS, COMMON_STYLES, FORM_STYLES

class FinancialAnalysisPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mali Analizler')
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
        title_label = QLabel('Mali Analizler')
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
        
        # Analiz seçimi
        analysis_widget = QWidget()
        analysis_widget.setFixedHeight(80)
        analysis_widget.setStyleSheet("background-color: white;")
        analysis_layout = QHBoxLayout(analysis_widget)
        
        analysis_label = QLabel('Analiz Türü:')
        analysis_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems([
            'Likidite Oranları',
            'Finansal Yapı Oranları',
            'Faaliyet Oranları',
            'Karlılık Oranları'
        ])
        self.analysis_combo.setFixedWidth(300)
        self.analysis_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #D94E1F;
                border-radius: 10px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.analysis_combo.currentIndexChanged.connect(self.update_analysis)
        
        analysis_layout.addWidget(analysis_label)
        analysis_layout.addWidget(self.analysis_combo)
        analysis_layout.addStretch()
        
        # Analiz sonuçları tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Oran', 'Değer', 'Değerlendirme'])
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
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        layout.addWidget(title_bar)
        layout.addWidget(analysis_widget)
        layout.addWidget(self.table)
        
        # Veritabanını oluştur
        self.create_database()
        
        # İlk analizi göster - Move this after database creation
        self.update_analysis()

    def update_analysis(self):
        analysis_type = self.analysis_combo.currentText()
        
        # Önce oranları göster
        if analysis_type == 'Likidite Oranları':
            self.show_liquidity_ratios()
        elif analysis_type == 'Finansal Yapı Oranları':
            self.show_financial_structure_ratios()
        elif analysis_type == 'Faaliyet Oranları':
            self.show_activity_ratios()
        elif analysis_type == 'Karlılık Oranları':
            self.show_profitability_ratios()
            
        # Move save_analysis_results after showing the ratios
        self.save_analysis_results(analysis_type)
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Mali analiz sonuçları tablosunu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date DATE NOT NULL,
                analysis_type TEXT NOT NULL,
                ratio_name TEXT NOT NULL,
                ratio_value REAL NOT NULL,
                evaluation TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis_results(self, analysis_type):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        current_date = QDate.currentDate().toString(Qt.ISODate)
        
        # Tablodaki tüm oranları kaydet
        for row in range(self.table.rowCount()):
            ratio_name = self.table.item(row, 0).text()
            ratio_value = float(self.table.item(row, 1).text().replace('%', '').replace(',', '.'))
            evaluation = self.table.item(row, 2).text()
            
            cursor.execute('''
                INSERT INTO financial_analysis 
                (analysis_date, analysis_type, ratio_name, ratio_value, evaluation)
                VALUES (?, ?, ?, ?, ?)
            ''', (current_date, analysis_type, ratio_name, ratio_value, evaluation))
        
        conn.commit()
        conn.close()
        
        QMessageBox.information(
            self,
            'Başarılı',
            'Mali analiz sonuçları başarıyla kaydedildi.',
            QMessageBox.Ok
        )
    
    def show_liquidity_ratios(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Cari oran hesaplama
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions WHERE status = "Tahsil Edildi") +
                (SELECT SUM(amount) FROM income_transactions WHERE status = "Beklemede") as current_assets,
                (SELECT SUM(amount) FROM expense_transactions WHERE status = "Beklemede") as current_liabilities
        ''')
        result = cursor.fetchone()
        current_assets = result[0] or 0
        current_liabilities = result[1] or 0
        
        current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
        
        # Asit-test oranı hesaplama (stoklar hariç)
        acid_test_ratio = current_ratio  # Şimdilik stok verisi olmadığı için cari oranla aynı
        
        # Nakit oranı hesaplama
        cursor.execute('SELECT SUM(amount) FROM income_transactions WHERE status = "Tahsil Edildi"')
        cash = cursor.fetchone()[0] or 0
        cash_ratio = cash / current_liabilities if current_liabilities != 0 else 0
        
        conn.close()
        
        # Tabloyu güncelle
        self.table.setRowCount(3)
        
        # Cari oran
        self.table.setItem(0, 0, QTableWidgetItem('Cari Oran'))
        self.table.setItem(0, 1, QTableWidgetItem(f'{current_ratio:.2f}'))
        evaluation = 'İyi' if current_ratio >= 2 else 'Orta' if current_ratio >= 1 else 'Zayıf'
        self.table.setItem(0, 2, QTableWidgetItem(evaluation))
        
        # Asit-test oranı
        self.table.setItem(1, 0, QTableWidgetItem('Asit-Test Oranı'))
        self.table.setItem(1, 1, QTableWidgetItem(f'{acid_test_ratio:.2f}'))
        evaluation = 'İyi' if acid_test_ratio >= 1 else 'Orta' if acid_test_ratio >= 0.7 else 'Zayıf'
        self.table.setItem(1, 2, QTableWidgetItem(evaluation))
        
        # Nakit oranı
        self.table.setItem(2, 0, QTableWidgetItem('Nakit Oranı'))
        self.table.setItem(2, 1, QTableWidgetItem(f'{cash_ratio:.2f}'))
        evaluation = 'İyi' if cash_ratio >= 0.2 else 'Orta' if cash_ratio >= 0.1 else 'Zayıf'
        self.table.setItem(2, 2, QTableWidgetItem(evaluation))
    
    def show_financial_structure_ratios(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Toplam borçlar
        cursor.execute('SELECT SUM(amount) FROM expense_transactions WHERE status = "Beklemede"')
        total_liabilities = cursor.fetchone()[0] or 0
        
        # Toplam varlıklar - type sütunu olmadığı için sorguyu düzelttik
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) +
                (SELECT COALESCE(SUM(amount), 0) FROM expense_transactions) as total_assets
        ''')
        total_assets = cursor.fetchone()[0] or 0
        
        # Öz sermaye
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) -
                (SELECT SUM(amount) FROM expense_transactions) as equity
        ''')
        equity = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Oranları hesapla
        debt_ratio = total_liabilities / total_assets if total_assets != 0 else 0
        equity_ratio = equity / total_assets if total_assets != 0 else 0
        debt_equity_ratio = total_liabilities / equity if equity != 0 else 0
        
        # Tabloyu güncelle
        self.table.setRowCount(3)
        
        # Borç oranı
        self.table.setItem(0, 0, QTableWidgetItem('Borç Oranı'))
        self.table.setItem(0, 1, QTableWidgetItem(f'{debt_ratio:.2f}'))
        evaluation = 'İyi' if debt_ratio <= 0.5 else 'Orta' if debt_ratio <= 0.7 else 'Riskli'
        self.table.setItem(0, 2, QTableWidgetItem(evaluation))
        
        # Öz sermaye oranı
        self.table.setItem(1, 0, QTableWidgetItem('Öz Sermaye Oranı'))
        self.table.setItem(1, 1, QTableWidgetItem(f'{equity_ratio:.2f}'))
        evaluation = 'İyi' if equity_ratio >= 0.5 else 'Orta' if equity_ratio >= 0.3 else 'Zayıf'
        self.table.setItem(1, 2, QTableWidgetItem(evaluation))
        
        # Borç/Öz sermaye oranı
        self.table.setItem(2, 0, QTableWidgetItem('Borç/Öz Sermaye Oranı'))
        self.table.setItem(2, 1, QTableWidgetItem(f'{debt_equity_ratio:.2f}'))
        evaluation = 'İyi' if debt_equity_ratio <= 1 else 'Orta' if debt_equity_ratio <= 2 else 'Riskli'
        self.table.setItem(2, 2, QTableWidgetItem(evaluation))
    
    def show_activity_ratios(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Satışlar (gelirler)
        cursor.execute('SELECT SUM(amount) FROM income_transactions')
        sales = cursor.fetchone()[0] or 0
        
        # Ortalama alacaklar
        cursor.execute('SELECT SUM(amount) FROM income_transactions WHERE status = "Beklemede"')
        receivables = cursor.fetchone()[0] or 0
        
        # Ortalama stoklar (varsayılan)
        inventory = 0  # Stok verisi olmadığı için 0 alıyoruz
        
        # Toplam varlıklar - type sütunu olmadığı için sorguyu düzelttik
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) +
                (SELECT COALESCE(SUM(amount), 0) FROM expense_transactions) as total_assets
        ''')
        total_assets = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Oranları hesapla
        receivables_turnover = sales / receivables if receivables != 0 else 0
        inventory_turnover = sales / inventory if inventory != 0 else 0
        asset_turnover = sales / total_assets if total_assets != 0 else 0
        
        # Tabloyu güncelle
        self.table.setRowCount(3)
        
        # Alacak devir hızı
        self.table.setItem(0, 0, QTableWidgetItem('Alacak Devir Hızı'))
        self.table.setItem(0, 1, QTableWidgetItem(f'{receivables_turnover:.2f}'))
        evaluation = 'İyi' if receivables_turnover >= 6 else 'Orta' if receivables_turnover >= 4 else 'Düşük'
        self.table.setItem(0, 2, QTableWidgetItem(evaluation))
        
        # Stok devir hızı
        self.table.setItem(1, 0, QTableWidgetItem('Stok Devir Hızı'))
        self.table.setItem(1, 1, QTableWidgetItem('N/A'))
        self.table.setItem(1, 2, QTableWidgetItem('Stok verisi mevcut değil'))
        
        # Aktif devir hızı
        self.table.setItem(2, 0, QTableWidgetItem('Aktif Devir Hızı'))
        self.table.setItem(2, 1, QTableWidgetItem(f'{asset_turnover:.2f}'))
        evaluation = 'İyi' if asset_turnover >= 1 else 'Orta' if asset_turnover >= 0.5 else 'Düşük'
        self.table.setItem(2, 2, QTableWidgetItem(evaluation))
    
    def show_profitability_ratios(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Satışlar (gelirler)
        cursor.execute('SELECT SUM(amount) FROM income_transactions')
        sales = cursor.fetchone()[0] or 0
        
        # Net kar
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) -
                (SELECT SUM(amount) FROM expense_transactions) as net_profit
        ''')
        net_profit = cursor.fetchone()[0] or 0
        
        # Toplam varlıklar - type sütunu olmadığı için sorguyu düzelttik
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) +
                (SELECT COALESCE(SUM(amount), 0) FROM expense_transactions) as total_assets
        ''')
        total_assets = cursor.fetchone()[0] or 0
        
        # Öz sermaye
        cursor.execute('''
            SELECT 
                (SELECT SUM(amount) FROM income_transactions) -
                (SELECT SUM(amount) FROM expense_transactions) as equity
        ''')
        equity = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # Oranları hesapla
        net_profit_margin = net_profit / sales if sales != 0 else 0
        roa = net_profit / total_assets if total_assets != 0 else 0
        roe = net_profit / equity if equity != 0 else 0
        
        # Tabloyu güncelle
        self.table.setRowCount(3)
        
        # Net kar marjı
        self.table.setItem(0, 0, QTableWidgetItem('Net Kar Marjı'))
        self.table.setItem(0, 1, QTableWidgetItem(f'{net_profit_margin:.2%}'))
        evaluation = 'İyi' if net_profit_margin >= 0.1 else 'Orta' if net_profit_margin >= 0.05 else 'Düşük'
        self.table.setItem(0, 2, QTableWidgetItem(evaluation))
        
        # Aktif karlılığı (ROA)
        self.table.setItem(1, 0, QTableWidgetItem('Aktif Karlılığı (ROA)'))
        self.table.setItem(1, 1, QTableWidgetItem(f'{roa:.2%}'))
        evaluation = 'İyi' if roa >= 0.1 else 'Orta' if roa >= 0.05 else 'Düşük'
        self.table.setItem(1, 2, QTableWidgetItem(evaluation))
        
        # Öz sermaye karlılığı (ROE)
        self.table.setItem(2, 0, QTableWidgetItem('Öz Sermaye Karlılığı (ROE)'))
        self.table.setItem(2, 1, QTableWidgetItem(f'{roe:.2%}'))
        evaluation = 'İyi' if roe >= 0.15 else 'Orta' if roe >= 0.1 else 'Düşük'
        self.table.setItem(2, 2, QTableWidgetItem(evaluation))