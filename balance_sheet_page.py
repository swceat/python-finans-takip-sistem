import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                            QDialog, QDateEdit, QLineEdit, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QIcon
from styles import COLORS, COMMON_STYLES, FORM_STYLES

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class BalanceSheetPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bilanço Tablosu')
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
        title_label = QLabel('Bilanço Tablosu')
        title_label.setStyleSheet('color: white; font-size: 28px; font-weight: bold;')
        
        # Yeni Kayıt Ekle butonu
        self.add_entry_button = QPushButton('+ Yeni Kayıt Ekle')
        self.add_entry_button.setStyleSheet("""
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
        self.add_entry_button.clicked.connect(self.show_add_entry_dialog)
        
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
        title_layout.addWidget(self.add_entry_button)
        title_layout.addWidget(close_button)
        
        # Özet bilgiler
        summary_widget = QWidget()
        summary_widget.setFixedHeight(100)
        summary_widget.setStyleSheet("background-color: white;")
        summary_layout = QHBoxLayout(summary_widget)
        
        # Toplam Varlıklar
        total_assets_widget = QWidget()
        total_assets_layout = QVBoxLayout(total_assets_widget)
        total_assets_label = QLabel('Toplam Varlıklar')
        total_assets_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        self.total_assets_amount = QLabel('0,00 TL')
        self.total_assets_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        total_assets_layout.addWidget(total_assets_label)
        total_assets_layout.addWidget(self.total_assets_amount)
        
        # Toplam Borçlar
        total_liabilities_widget = QWidget()
        total_liabilities_layout = QVBoxLayout(total_liabilities_widget)
        total_liabilities_label = QLabel('Toplam Borçlar')
        total_liabilities_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #C62828;")
        self.total_liabilities_amount = QLabel('0,00 TL')
        self.total_liabilities_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #C62828;")
        total_liabilities_layout.addWidget(total_liabilities_label)
        total_liabilities_layout.addWidget(self.total_liabilities_amount)
        
        # Öz Sermaye
        equity_widget = QWidget()
        equity_layout = QVBoxLayout(equity_widget)
        equity_label = QLabel('Öz Sermaye')
        equity_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1565C0;")
        self.equity_amount = QLabel('0,00 TL')
        self.equity_amount.setStyleSheet("font-size: 24px; font-weight: bold; color: #1565C0;")
        equity_layout.addWidget(equity_label)
        equity_layout.addWidget(self.equity_amount)
        
        summary_layout.addWidget(total_assets_widget)
        summary_layout.addWidget(total_liabilities_widget)
        summary_layout.addWidget(equity_widget)
        
        # Bilanço tablosu
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
        
        # Ana başlıkları kalın yap
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and not item.text().startswith('   '):
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                item.setBackground(Qt.lightGray)
        
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
        self.load_balance_sheet_data()
    
    def create_database(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Bilanço girdileri tablosunu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balance_sheet_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                account_type TEXT NOT NULL,
                account_name TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bilanço kategorileri tablosunu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balance_sheet_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES balance_sheet_categories (id)
            )
        ''')
        
        # Varsayılan kategorileri ekle
        default_categories = [
            ('DÖNEN VARLIKLAR', 'asset', None),
            ('Hazır Değerler', 'asset', 1),
            ('Ticari Alacaklar', 'asset', 1),
            ('Stoklar', 'asset', 1),
            ('DURAN VARLIKLAR', 'asset', None),
            ('Maddi Duran Varlıklar', 'asset', 5),
            ('Maddi Olmayan Duran Varlıklar', 'asset', 5),
            ('KISA VADELİ YÜKÜMLÜLÜKLER', 'liability', None),
            ('Ticari Borçlar', 'liability', 8),
            ('Banka Kredileri', 'liability', 8),
            ('UZUN VADELİ YÜKÜMLÜLÜKLER', 'liability', None),
            ('Uzun Vadeli Krediler', 'liability', 11),
            ('ÖZ SERMAYE', 'equity', None),
            ('Ödenmiş Sermaye', 'equity', 13),
            ('Yedekler', 'equity', 13),
            ('Geçmiş Yıl Karları', 'equity', 13),
            ('Dönem Net Karı', 'equity', 13)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO balance_sheet_categories (name, type, parent_id)
            VALUES (?, ?, ?)
        ''', default_categories)
        
        conn.commit()
        conn.close()
    
    def load_balance_sheet_data(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Varlıklar
        assets = [
            ('DÖNEN VARLIKLAR', ''),
            ('   Kasa', self.get_cash_balance(cursor)),
            ('   Bankalar', self.get_bank_balance(cursor)),
            ('   Ticari Alacaklar', self.get_receivables(cursor)),
            ('   Stoklar', self.get_inventory(cursor)),
            ('DURAN VARLIKLAR', ''),
            ('   Maddi Duran Varlıklar', self.get_fixed_assets(cursor)),
            ('   Maddi Olmayan Duran Varlıklar', self.get_intangible_assets(cursor))
        ]
        
        # Yükümlülükler ve Öz Sermaye
        liabilities = [
            ('KISA VADELİ YÜKÜMLÜLÜKLER', ''),
            ('   Ticari Borçlar', self.get_trade_payables(cursor)),
            ('   Banka Kredileri', self.get_bank_loans(cursor)),
            ('UZUN VADELİ YÜKÜMLÜLÜKLER', ''),
            ('   Uzun Vadeli Krediler', self.get_long_term_loans(cursor)),
            ('ÖZ SERMAYE', ''),
            ('   Sermaye', self.get_capital(cursor)),
            ('   Geçmiş Yıl Karları', self.get_retained_earnings(cursor)),
            ('   Dönem Net Karı', self.get_net_income(cursor))
        ]
        
        # Tabloyu doldur
        self.table.setRowCount(len(assets) + len(liabilities) + 1)  # +1 for spacing
        
        # Varlıkları ekle
        asset_subtotal = 0
        total_assets = 0
        asset_row_offset = 0
        for row, (account, amount) in enumerate(assets):
            item = QTableWidgetItem(account)
            if not account.startswith('   '):  # Ana başlık
                item.setBackground(QColor('#FFE0B2'))
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                # İkon eklemek için örnek:
                # item.setIcon(QIcon('icons/asset.png'))
            self.table.setItem(row + asset_row_offset, 0, item)
            if amount:
                amount_item = QTableWidgetItem(f"{amount:,.2f} TL")
                if account.startswith('   '):
                    asset_subtotal += amount
                    total_assets += amount
            else:
                amount_item = QTableWidgetItem('')
            self.table.setItem(row + asset_row_offset, 1, amount_item)
            # Alt toplamı ana başlık sonrası ekle
            if account == 'DURAN VARLIKLAR':
                subtotal_item = QTableWidgetItem('Alt Toplam')
                subtotal_item.setBackground(QColor('#FFD54F'))
                subtotal_font = subtotal_item.font()
                subtotal_font.setBold(True)
                subtotal_item.setFont(subtotal_font)
                self.table.setItem(row + asset_row_offset + 1, 0, subtotal_item)
                subtotal_amount_item = QTableWidgetItem(f"{asset_subtotal:,.2f} TL")
                subtotal_amount_item.setBackground(QColor('#FFD54F'))
                self.table.setItem(row + asset_row_offset + 1, 1, subtotal_amount_item)
                asset_row_offset += 1
                asset_subtotal = 0
        
        # Boş satır ekle
        self.table.setItem(len(assets) + asset_row_offset, 0, QTableWidgetItem(''))
        self.table.setItem(len(assets) + asset_row_offset, 1, QTableWidgetItem(''))
        
        # Yükümlülükleri ve öz sermayeyi ekle
        liability_subtotal = 0
        equity_subtotal = 0
        total_liabilities = 0
        total_equity = 0
        liability_row_offset = 0
        for row, (account, amount) in enumerate(liabilities, len(assets) + asset_row_offset + 1):
            item = QTableWidgetItem(account)
            if not account.startswith('   '):  # Ana başlık
                # Renk ve ikonlar kategoriye göre değiştirilebilir
                if 'YÜKÜMLÜLÜKLER' in account:
                    item.setBackground(QColor('#FFCDD2'))
                elif 'ÖZ SERMAYE' in account:
                    item.setBackground(QColor('#BBDEFB'))
                else:
                    item.setBackground(QColor('#E0E0E0'))
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                # İkon eklemek için örnek:
                # item.setIcon(QIcon('icons/liability.png'))
            self.table.setItem(row + liability_row_offset, 0, item)
            if amount:
                amount_item = QTableWidgetItem(f"{amount:,.2f} TL")
                if account.startswith('   '):
                    if row < len(assets) + asset_row_offset + 5:  # İlk 4 satır yükümlülükler
                        liability_subtotal += amount
                        total_liabilities += amount
                    else:
                        equity_subtotal += amount
                        total_equity += amount
            else:
                amount_item = QTableWidgetItem('')
            self.table.setItem(row + liability_row_offset, 1, amount_item)
            # Alt toplamı ana başlık sonrası ekle
            if account == 'UZUN VADELİ YÜKÜMLÜLÜKLER':
                subtotal_item = QTableWidgetItem('Alt Toplam')
                subtotal_item.setBackground(QColor('#EF9A9A'))
                subtotal_font = subtotal_item.font()
                subtotal_font.setBold(True)
                subtotal_item.setFont(subtotal_font)
                self.table.setItem(row + liability_row_offset + 1, 0, subtotal_item)
                subtotal_amount_item = QTableWidgetItem(f"{liability_subtotal:,.2f} TL")
                subtotal_amount_item.setBackground(QColor('#EF9A9A'))
                self.table.setItem(row + liability_row_offset + 1, 1, subtotal_amount_item)
                liability_row_offset += 1
                liability_subtotal = 0
            if account == 'ÖZ SERMAYE':
                subtotal_item = QTableWidgetItem('Alt Toplam')
                subtotal_item.setBackground(QColor('#90CAF9'))
                subtotal_font = subtotal_item.font()
                subtotal_font.setBold(True)
                subtotal_item.setFont(subtotal_font)
                self.table.setItem(row + liability_row_offset + 1, 0, subtotal_item)
                subtotal_amount_item = QTableWidgetItem(f"{equity_subtotal:,.2f} TL")
                subtotal_amount_item.setBackground(QColor('#90CAF9'))
                self.table.setItem(row + liability_row_offset + 1, 1, subtotal_amount_item)
                liability_row_offset += 1
                equity_subtotal = 0
        
        # Özet bilgileri güncelle
        self.total_assets_amount.setText(f"{total_assets:,.2f} TL")
        self.total_liabilities_amount.setText(f"{total_liabilities:,.2f} TL")
        self.equity_amount.setText(f"{total_equity:,.2f} TL")
        
        conn.close()
    
    def get_cash_balance(self, cursor):
        cursor.execute('SELECT SUM(amount) FROM income_transactions WHERE status = "Tahsil Edildi"')
        income = cursor.fetchone()[0] or 0
        cursor.execute('SELECT SUM(amount) FROM expense_transactions WHERE status = "Ödendi"')
        expense = cursor.fetchone()[0] or 0
        return income - expense
    
    def get_bank_balance(self, cursor):
        # Banka bakiyesi hesaplama mantığı
        return 0
    
    def get_receivables(self, cursor):
        cursor.execute('SELECT SUM(amount) FROM income_transactions WHERE status = "Beklemede"')
        return cursor.fetchone()[0] or 0
    
    def get_inventory(self, cursor):
        # Stok değeri hesaplama mantığı
        return 0
    
    def get_fixed_assets(self, cursor):
        # Maddi duran varlıklar hesaplama mantığı
        return 0
    
    def get_intangible_assets(self, cursor):
        # Maddi olmayan duran varlıklar hesaplama mantığı
        return 0
    
    def get_trade_payables(self, cursor):
        cursor.execute('SELECT SUM(amount) FROM expense_transactions WHERE status = "Beklemede"')
        return cursor.fetchone()[0] or 0
    
    def get_bank_loans(self, cursor):
        # Banka kredileri hesaplama mantığı
        return 0
    
    def get_long_term_loans(self, cursor):
        # Uzun vadeli krediler hesaplama mantığı
        return 0
    
    def get_capital(self, cursor):
        # Sermaye hesaplama mantığı
        return 0
    
    def get_retained_earnings(self, cursor):
        # Geçmiş yıl karları hesaplama mantığı
        return 0
    
    def get_net_income(self, cursor):
        cursor.execute('SELECT SUM(amount) FROM income_transactions')
        total_income = cursor.fetchone()[0] or 0
        cursor.execute('SELECT SUM(amount) FROM expense_transactions')
        total_expense = cursor.fetchone()[0] or 0
        return total_income - total_expense

    def show_add_entry_dialog(self):
        dialog = NewEntryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get values from dialog
            date = dialog.date_edit.date().toString('yyyy-MM-dd')
            account_type = dialog.account_type_input.currentText()
            account_name = dialog.account_name_input.text()
            amount = float(dialog.amount_input.text().replace(',', '.'))
            description = dialog.description_input.text()
            
            # Save to database
            conn = sqlite3.connect('finance.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO balance_sheet_entries 
                (date, account_type, account_name, amount, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, account_type, account_name, amount, description))
            conn.commit()
            conn.close()
            
            # Refresh the data
            self.load_balance_sheet_data()
            
            QMessageBox.information(
                self,
                'Başarılı',
                'Bilanço kaydı başarıyla eklendi!',
                QMessageBox.Ok
            )

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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

class NewEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Yeni Bilanço Kaydı')
        self.setFixedSize(600, 400)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Form elemanları
        fields = [
            ('Tarih:', QDateEdit()),
            ('Hesap Türü:', QComboBox()),
            ('Hesap Adı:', QLineEdit()),
            ('Tutar (₺):', QLineEdit()),
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
                    min-width: 100px;
                }
            """)
            field_layout.addWidget(label)
            
            if isinstance(widget, QComboBox):
                widget.addItems(['Varlıklar', 'Yükümlülükler', 'Öz Kaynaklar'])
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
            
            if label_text == 'Tarih:':
                self.date_edit = widget
            elif label_text == 'Hesap Türü:':
                self.account_type_input = widget
            elif label_text == 'Hesap Adı:':
                self.account_name_input = widget
            elif label_text == 'Tutar (₺):':
                self.amount_input = widget
            elif label_text == 'Açıklama:':
                self.description_input = widget
        
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