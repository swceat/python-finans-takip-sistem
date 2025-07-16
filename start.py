import sys
import os
from styles import COLORS, COMMON_STYLES, THEMES
from utils import Utils, load_theme  # <-- BURAYA EKLEYİN
from constants import APP_NAME, MESSAGES
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QMessageBox, QApplication, QGridLayout)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from income_page import IncomeTransactionsPage
from expense_page import ExpenseTransactionsPage
from cash_flow_page import CashFlowPage
from budget_management_page import BudgetManagementPage
from balance_sheet_page import BalanceSheetPage
from income_statement_page import IncomeStatementPage  # Yeni import
from financial_reports_page import FinancialReportsPage  # Yeni import
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QTimer
import requests
from PyQt5.QtWidgets import QDialog, QComboBox, QFormLayout, QLineEdit, QDialogButtonBox
from ayarlar import SettingsWindow
from PyQt5.QtCore import QPropertyAnimation, QRect

# Açıklamalar:
# widget: Arayüzdeki her bir görsel bileşene (örneğin buton, metin kutusu, etiket) verilen genel isimdir.
# layout: Widget'ların ekranda nasıl yerleşeceğini belirleyen düzenleyicilerdir (örneğin QVBoxLayout: dikey, QHBoxLayout: yatay yerleşim).
# alignment: Bir widget'ın veya içeriğin, bulunduğu alan içinde hizalanma biçimini belirtir (örneğin Qt.AlignCenter: ortalama).
# Create QApplication instance at the start
app = QApplication(sys.argv)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        theme_name = load_theme()
        theme = THEMES.get(theme_name, THEMES["Açık"])
        self.setStyleSheet(f"QMainWindow {{background-color: {theme['background']};}}")
        # Giriş penceresinin temel ayarları ve arayüz oluşturma
        self.setWindowTitle('Finans Takip - Giriş')
        self.setFixedSize(400, 500)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #FFF5E6;
            }
        ''')
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Ana widget ve layout oluşturuluyor
        ana_widget = QWidget()
        ana_widget.setStyleSheet('''
            QWidget {
                background-color: #FFF5E6;
            }
        ''')
        self.setCentralWidget(ana_widget)
        dikey_dizilim = QVBoxLayout(ana_widget)
        dikey_dizilim.setContentsMargins(0, 0, 0, 40)
        dikey_dizilim.setSpacing(20)
        
        # Başlık çubuğu ve kapatma butonu
        baslik_cubugu = QWidget()
        baslik_cubugu.setFixedHeight(40)
        baslik_cubugu.setFixedWidth(400)
        baslik_cubugu.setStyleSheet('''
            QWidget {
                background-color: #D94E1F;
            }
        ''')
        baslik_cubugu_dizilim = QHBoxLayout(baslik_cubugu)
        baslik_cubugu_dizilim.setContentsMargins(15, 0, 15, 0)
        
        pencere_basligi = QLabel('Finans Takip - Giriş')
        pencere_basligi.setStyleSheet('color: white; font-size: 18px; font-weight: bold;')
        
        kapatma_butonu = QPushButton('×')
        kapatma_butonu.setFixedSize(30, 30)
        kapatma_butonu.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 20px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                color: #FFE0E0;
            }
        """)
        kapatma_butonu.clicked.connect(self.close)
        
        baslik_cubugu_dizilim.addWidget(pencere_basligi)
        baslik_cubugu_dizilim.addStretch()
        baslik_cubugu_dizilim.addWidget(kapatma_butonu)
        
        dikey_dizilim.addWidget(baslik_cubugu)
        
        # Logo ve başlık etiketi
        baslik_etiketi = QLabel('Finans Takip')
        baslik_etiketi.setStyleSheet('color: #D94E1F; font-size: 38px; font-weight: bold;')
        baslik_etiketi.setAlignment(Qt.AlignCenter)
        
        # Kullanıcı adı giriş kutusu
        self.kullanici_adi_giris = QLineEdit()
        self.kullanici_adi_giris.setPlaceholderText('Kullanıcı Adı')
        self.kullanici_adi_giris.setFixedSize(300, 40)
        self.kullanici_adi_giris.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #D94E1F;
                border-radius: 15px;
                font-size: 16px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #B33D15;
            }
        """)
        
        # Şifre giriş kutusu
        self.sifre_giris = QLineEdit()
        self.sifre_giris.setPlaceholderText('Şifre')
        self.sifre_giris.setEchoMode(QLineEdit.Password)
        self.sifre_giris.setFixedSize(300, 40)
        self.sifre_giris.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #D94E1F;
                border-radius: 15px;
                font-size: 16px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #B33D15;
            }
        """)
        
        # Giriş butonu
        self.giris_butonu = QPushButton('Giriş Yap')
        self.giris_butonu.setFixedSize(300, 40)
        self.giris_butonu.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        self.giris_butonu.clicked.connect(self.login)
        
        # İçerik widget'ı ve düzeni
        icerik_widget = QWidget()
        icerik_dizilim = QVBoxLayout(icerik_widget)
        icerik_dizilim.setAlignment(Qt.AlignCenter)
        icerik_dizilim.setSpacing(30)
        icerik_dizilim.setContentsMargins(0, 40, 0, 40)
        icerik_dizilim.addWidget(baslik_etiketi)
        icerik_dizilim.addWidget(self.kullanici_adi_giris)
        icerik_dizilim.addWidget(self.sifre_giris)
        icerik_dizilim.addWidget(self.giris_butonu)
        
        dikey_dizilim.addStretch()
        dikey_dizilim.addWidget(icerik_widget)
        dikey_dizilim.addStretch()
        
        self.center()
        
        # Giriş butonuna animasyon eklemek için event filter kurulumu
        self.giris_butonu.installEventFilter(self)
    
    # Pencereyi ekranın ortasına yerleştirir
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    # Pencerenin sürüklenebilmesi için mouse basma olayı
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    # Pencerenin sürüklenebilmesi için mouse hareket olayı
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    # Giriş butonuna hover animasyonu ekler
    def eventFilter(self, obj, event):
        if obj == self.giris_butonu:
            if event.type() == event.Enter:
                # Hover başladığında büyütme animasyonu
                self.animasyon = QPropertyAnimation(self.giris_butonu, b'pos')
                self.animasyon.setDuration(200)
                mevcut_pozisyon = self.giris_butonu.pos()
                self.animasyon.setStartValue(mevcut_pozisyon)
                self.animasyon.setEndValue(mevcut_pozisyon - QPoint(3, 3))
                self.animasyon.setEasingCurve(QEasingCurve.OutCubic)
                self.animasyon.start()
            elif event.type() == event.Leave:
                # Hover bittiğinde küçültme animasyonu
                self.animasyon = QPropertyAnimation(self.giris_butonu, b'pos')
                self.animasyon.setDuration(200)
                mevcut_pozisyon = self.giris_butonu.pos()
                self.animasyon.setStartValue(mevcut_pozisyon)
                self.animasyon.setEndValue(mevcut_pozisyon + QPoint(3, 3))
                self.animasyon.setEasingCurve(QEasingCurve.OutCubic)
                self.animasyon.start()
        return super().eventFilter(obj, event)
    
    # Giriş işlemini kontrol eder
    def login(self):
        kullanici_adi = self.kullanici_adi_giris.text()
        sifre = self.sifre_giris.text()
        user_file = "user_info.txt"
        if not os.path.exists(user_file):
            # Eğer dosya yoksa ilk giriş için oluştur
            with open(user_file, "w") as f:
                f.write("admin\n1234\n")
        with open(user_file, "r") as f:
            lines = f.readlines()
        kayitli_kullanici = lines[0].strip() if len(lines) > 0 else ""
        kayitli_sifre = lines[1].strip() if len(lines) > 1 else ""
        if kullanici_adi == kayitli_kullanici and sifre == kayitli_sifre:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            Utils.show_error(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
            self.sifre_giris.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        theme_name = load_theme()
        theme = THEMES.get(theme_name, THEMES["Açık"])
        self.setStyleSheet(f"background-color: {theme['background']};")
        self.setWindowTitle('Finans Takip - Ana Sayfa')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Başlık çubuğu
        title_bar = QWidget()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet('background-color: #D94E1F;')
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 0, 0)
        
        # Logo
        logo_label = QLabel('💼')
        logo_label.setStyleSheet('color: white; font-size: 24px; margin-right: 10px;')
        
        # Başlık etiketi
        title_label = QLabel('Finans Takip - Ana Sayfa')
        title_label.setStyleSheet('color: white; font-size: 24px; font-weight: bold;')
        
        # Minimize butonu
        minimize_button = QPushButton('−')
        minimize_button.setFixedSize(50, 50)
        minimize_button.setStyleSheet("""
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
        minimize_button.clicked.connect(self.showMinimized)
        
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
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(close_button)
        
        # Ana sayfa içeriği
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setHorizontalSpacing(120)  # Yatayda bloklar arası mesafe daha da artırıldı
        content_layout.setVerticalSpacing(80)    # Dikeyde bloklar arası mesafe daha da artırıldı
        
        # İşlem blokları
        blocks = [
            ('Gelir ve\nİşlemler', '💰'),
            ('Gider\nİşlemleri', '💳'),
            ('Nakit\nAkışı', '📊'),
            ('Bütçe\nYönetimi', '📈'),
            ('Bilanço\nTablosu', '📑'),
            ('Gelir\nTablosu', '📋')
        ]
        
        for i, (text, icon) in enumerate(blocks):
            block = QPushButton(f'{icon}\n{text}')
            block.setFixedSize(260, 160)  # Blok genişliği ve yüksekliği artırıldı
            block.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #D94E1F, stop:1 #B33D15);
                    color: white;
                    border: none;
                    border-radius: 18px;
                    font-size: 22px;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
                QPushButton:hover {
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #B33D15, stop:1 #8C2E10);
                }
                QPushButton:pressed {
                    background-color: #8C2E10;
                }
            """)
            if text == 'Gelir ve\nİşlemler':
                block.clicked.connect(self.open_income_page)
            elif text == 'Gider\nİşlemleri':
                block.clicked.connect(self.open_expense_page)
            elif text == 'Nakit\nAkışı':
                block.clicked.connect(self.open_cash_flow_page)
            elif text == 'Bütçe\nYönetimi':
                block.clicked.connect(self.open_budget_page)
            elif text == 'Bilanço\nTablosu':
                block.clicked.connect(self.open_balance_sheet_page)
            elif text == 'Gelir\nTablosu':
                block.clicked.connect(self.open_income_statement_page)
            row = i // 3
            col = i % 3
            content_layout.addWidget(block, row, col, alignment=Qt.AlignCenter)
        
        # Ortalamak için layout'a stretch ekle
        content_layout.setRowStretch(0, 1)
        content_layout.setRowStretch(3, 1)
        content_layout.setColumnStretch(0, 1)
        content_layout.setColumnStretch(4, 1)
        
        # Ana layout düzeni
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        main_layout.addStretch(1)
        main_layout.addWidget(content_widget, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        
        layout.addWidget(title_bar)
        layout.addWidget(main_content)
        
        # Sağ alt köşeye sabit Ayarlar butonu ekle
        self.settings_button = QPushButton('⚙️ Ayarlar')
        self.settings_button.setFixedSize(140, 50)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #D94E1F;
                border: 2px solid #D94E1F;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #D94E1F;
                color: white;
            }
            QPushButton:pressed {
                background-color: #B33D15;
                color: white;
            }
        """)
        self.settings_button.clicked.connect(self.open_settings_window)
        self.settings_button.installEventFilter(self)
        # Overlay yerine doğrudan ana layout'a ekle
        layout.addWidget(self.settings_button, alignment=Qt.AlignRight | Qt.AlignBottom)

    def eventFilter(self, obj, event):
        if obj == self.settings_button:
            if event.type() == event.MouseButtonPress:
                self.apply_button_press_effect(self.settings_button)
            elif event.type() == event.MouseButtonRelease:
                self.apply_button_release_effect(self.settings_button)
        return super().eventFilter(obj, event)

    def apply_button_press_effect(self, button):
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(80)
        rect = button.geometry()
        shrinked = QRect(rect.x()+5, rect.y()+5, rect.width()-10, rect.height()-10)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(shrinked)
        self.anim.start()

    def apply_button_release_effect(self, button):
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(80)
        rect = button.geometry()
        original = QRect(rect.x()-5, rect.y()-5, rect.width()+10, rect.height()+10)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(original)
        self.anim.start()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(main_window=self)
        self.settings_window.show()

    def update_exchange_rates(self):
        try:
            # API'den kurları çek
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
            data = response.json()
            
            # Mevcut widget'ları temizle
            for i in reversed(range(self.exchange_rates_layout.count())): 
                self.exchange_rates_layout.itemAt(i).widget().setParent(None)
            
            # Kurları hesapla
            usd_try = data['rates']['TRY']
            eur_try = data['rates']['TRY'] / data['rates']['EUR']
            gbp_try = data['rates']['TRY'] / data['rates']['GBP']
            
            rates = [
                ('USD/TRY', f'{usd_try:.2f} ₺'),
                ('EUR/TRY', f'{eur_try:.2f} ₺'),
                ('GBP/TRY', f'{gbp_try:.2f} ₺')
            ]
            
            for currency, rate in rates:
                rate_widget = QWidget()
                rate_layout = QHBoxLayout(rate_widget)
                
                currency_label = QLabel(currency)
                currency_label.setStyleSheet('font-size: 16px; font-weight: bold;')
                
                rate_label = QLabel(rate)
                rate_label.setStyleSheet('font-size: 16px;')
                
                rate_layout.addWidget(currency_label)
                rate_layout.addStretch()
                rate_layout.addWidget(rate_label)
                
                self.exchange_rates_layout.addWidget(rate_widget)
                
        except Exception as e:
            print(f"Kur güncelleme hatası: {e}")

    def open_income_page(self):
        self.income_page = IncomeTransactionsPage()
        self.income_page.show()
    
    def open_expense_page(self):
        self.expense_page = ExpenseTransactionsPage()
        self.expense_page.show()
    
    def open_cash_flow_page(self):
        self.cash_flow_page = CashFlowPage()
        self.cash_flow_page.show()
    
    def open_budget_page(self):
        self.budget_page = BudgetManagementPage()
        self.budget_page.show()
    
    def open_balance_sheet_page(self):
        self.balance_sheet_page = BalanceSheetPage()
        self.balance_sheet_page.show()
    
    def open_income_statement_page(self):
        self.income_statement_page = IncomeStatementPage()
        self.income_statement_page.show()

if __name__ == '__main__':
    # Remove the QApplication creation from here since we moved it to the top
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)

        # Tema seçimi
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Açık", "Koyu"])
        layout.addWidget(QLabel("Tema Seçimi:"))
        layout.addWidget(self.theme_combo)

        # Kullanıcı adı
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Yeni kullanıcı adı")
        layout.addWidget(QLabel("Kullanıcı Adı:"))
        layout.addWidget(self.username_edit)

        # Şifre
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Yeni şifre")
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Şifre:"))
        layout.addWidget(self.password_edit)

        # Butonlar
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel | QDialogButtonBox.Close)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Close).clicked.connect(lambda: self.done(2))  # Çıkış için özel kod
        layout.addWidget(buttons)

    def logout(self):
        self.done(2)  # 2 kodu ile çıkış isteği


    def eventFilter(self, obj, event):
        if obj == self.settings_button:
            if event.type() == event.MouseButtonPress:
                self.animate_button_press(self.settings_button)
            elif event.type() == event.MouseButtonRelease:
                self.animate_button_release(self.settings_button)
        return super().eventFilter(obj, event)

    def animate_button_press(self, button):
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(80)
        rect = button.geometry()
        shrinked = QRect(rect.x()+5, rect.y()+5, rect.width()-10, rect.height()-10)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(shrinked)
        self.anim.start()

    def animate_button_release(self, button):
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(80)
        rect = button.geometry()
        original = QRect(rect.x()-5, rect.y()-5, rect.width()+10, rect.height()+10)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(original)
        self.anim.start()
