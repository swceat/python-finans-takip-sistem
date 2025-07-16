from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
import locale
from constants import MESSAGES
import json
import os

class Utils:
    @staticmethod
    def show_error(parent, message):
        QMessageBox.critical(parent, 'Hata', message)
    
    @staticmethod
    def show_success(parent, message):
        QMessageBox.information(parent, 'Başarılı', message)
    
    @staticmethod
    def show_confirm(parent, message):
        reply = QMessageBox.question(parent, 'Onay', message,
                                   QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes
    
    @staticmethod
    def format_currency(amount):
        return f"{amount:,.2f} TL"
    
    @staticmethod
    def validate_amount(text):
        try:
            amount = float(text.replace(',', ''))
            return amount >= 0
        except ValueError:
            return False
    
    @staticmethod
    def format_currency(amount):
        """Para birimini formatlar"""
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        return locale.currency(amount, grouping=True)
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """Tarih aralığını kontrol eder"""
        if start_date > end_date:
            return False, "Başlangıç tarihi bitiş tarihinden sonra olamaz!"
        return True, ""
    
    @staticmethod
    def show_message(parent, title, message, icon=QMessageBox.Information):
        """Mesaj kutusu gösterir"""
        QMessageBox.information(parent, title, message, QMessageBox.Ok)
    
    @staticmethod
    def show_error(parent, title, message):
        """Hata mesajı gösterir"""
        QMessageBox.warning(parent, title, message, QMessageBox.Ok)
    
    @staticmethod
    def format_date(date):
        """Tarihi formatlar"""
        return date.toString('dd.MM.yyyy')
    
    @staticmethod
    def validate_numeric_input(text):
        """Sayısal girişi kontrol eder"""
        try:
            float(text.replace(',', '.'))
            return True, ""
        except ValueError:
            return False, "Lütfen geçerli bir sayı giriniz!"

THEME_FILE = "settings.json"

def save_theme(theme_name):
    data = {"theme": theme_name}
    with open(THEME_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_theme():
    if not os.path.exists(THEME_FILE):
        return "Açık"  # Varsayılan tema
    with open(THEME_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("theme", "Açık")


def apply_theme(window, theme_name):
    from styles import THEMES
    theme = THEMES.get(theme_name, THEMES["Açık"])
    window.setStyleSheet(f"background-color: {theme['background']}; color: {theme['foreground']};")