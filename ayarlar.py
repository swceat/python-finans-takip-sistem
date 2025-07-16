from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFrame, QLineEdit
from PyQt5.QtCore import Qt
import os
from utils import save_theme, load_theme
from styles import THEMES

class SettingsWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Ayarlar")
        self.setFixedSize(400, 520)
        self.setStyleSheet("background-color: #FFF5E6;")

        central = QWidget()
        self.setCentralWidget(central)
        ana_layout = QVBoxLayout(central)
        ana_layout.setContentsMargins(30, 30, 30, 30)
        ana_layout.setSpacing(25)

        # Başlık
        title = QLabel("Ayarlar")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #D94E1F;")
        ana_layout.addWidget(title)

        # Tema seçimi bloğu
        tema_block = QFrame()
        tema_block.setFixedHeight(90)
        tema_block.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 16px;
            }
        """)
        tema_layout = QVBoxLayout(tema_block)
        tema_layout.setContentsMargins(16, 10, 16, 10)
        tema_label = QLabel("Tema Seçimi")
        tema_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #D94E1F;")
        tema_layout.addWidget(tema_label)
        tema_btns = QHBoxLayout()
        self.themes = [
            {"name": "Açık", "bg": "#FFF5E6", "fg": "#D94E1F"},
            {"name": "Koyu", "bg": "#232323", "fg": "#FFF5E6"},
            {"name": "Mavi", "bg": "#E3F2FD", "fg": "#1976D2"},
            {"name": "Yeşil", "bg": "#E8F5E9", "fg": "#388E3C"},
        ]
        for theme in self.themes:
            btn = QPushButton(theme["name"])
            btn.setFixedSize(70, 32)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme['bg']};
                    color: {theme['fg']};
                    border: 1.5px solid {theme['fg']};
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {theme['fg']};
                    color: {theme['bg']};
                }}
            """)
            btn.clicked.connect(lambda checked, t=theme: self.apply_theme(t))
            tema_btns.addWidget(btn)
        tema_layout.addLayout(tema_btns)
        ana_layout.addWidget(tema_block)

        # Parola değiştirme bloğu
        self.password_block = QFrame()
        self.password_block.setFixedHeight(90)
        self.password_block.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 16px;
            }
        """)
        pw_layout = QVBoxLayout(self.password_block)
        pw_layout.setContentsMargins(16, 10, 16, 10)
        pw_label = QLabel("Parola Değiştir")
        pw_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #D94E1F;")
        pw_layout.addWidget(pw_label)
        self.pw_btn = QPushButton("Parola Değiştir")
        self.pw_btn.setFixedSize(120, 32)
        self.pw_btn.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        self.pw_btn.clicked.connect(self.toggle_pw_fields)
        pw_layout.addWidget(self.pw_btn, alignment=Qt.AlignLeft)
        ana_layout.addWidget(self.password_block)

        # Parola değiştirme alanı (başta gizli)
        self.pw_fields = QWidget()
        pw_fields_layout = QVBoxLayout(self.pw_fields)
        pw_fields_layout.setContentsMargins(0, 0, 0, 0)
        self.old_pw = QLineEdit()
        self.old_pw.setPlaceholderText("Eski Parola")
        self.old_pw.setEchoMode(QLineEdit.Password)
        self.new_pw = QLineEdit()
        self.new_pw.setPlaceholderText("Yeni Parola")
        self.new_pw.setEchoMode(QLineEdit.Password)
        self.save_pw_btn = QPushButton("Kaydet")
        self.save_pw_btn.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 4px 12px;
            }
            QPushButton:hover {
                background-color: #2E7031;
            }
        """)
        self.save_pw_btn.clicked.connect(self.save_password)
        pw_fields_layout.addWidget(self.old_pw)
        pw_fields_layout.addWidget(self.new_pw)
        pw_fields_layout.addWidget(self.save_pw_btn, alignment=Qt.AlignRight)
        self.pw_fields.setVisible(False)
        ana_layout.addWidget(self.pw_fields)

        # Her şeyi sıfırla bloğu
        reset_block = QFrame()
        reset_block.setFixedHeight(90)
        reset_block.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #D94E1F;
                border-radius: 16px;
            }
        """)
        reset_layout = QVBoxLayout(reset_block)
        reset_layout.setContentsMargins(16, 10, 16, 10)
        reset_label = QLabel("Tüm Verileri Sıfırla")
        reset_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #D94E1F;")
        reset_layout.addWidget(reset_label)
        reset_btn = QPushButton("Her Şeyi Sıfırla")
        reset_btn.setFixedSize(120, 32)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #B33D15;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D94E1F;
            }
        """)
        reset_btn.clicked.connect(self.reset_all)
        reset_layout.addWidget(reset_btn, alignment=Qt.AlignLeft)
        ana_layout.addWidget(reset_block)

        # Kapat butonu
        close_btn = QPushButton("Kapat")
        close_btn.setFixedSize(120, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFF5E6;
                color: #D94E1F;
                border: 2px solid #D94E1F;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D94E1F;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        ana_layout.addWidget(close_btn, alignment=Qt.AlignRight)

    def apply_theme(self, theme):
        from styles import THEMES
        from utils import save_theme
        save_theme(theme)
        theme_colors = THEMES[theme]
        # Ana pencere ve login penceresi dahil tüm pencerelere uygula
        self.setStyleSheet(f"background-color: {theme_colors['background']}; color: {theme_colors['foreground']};")
        if self.main_window:
            self.main_window.setStyleSheet(f"background-color: {theme_colors['background']}; color: {theme_colors['foreground']};")
        QMessageBox.information(self, "Başarılı", f"Tema başarıyla değiştirildi!\nTema rengi: {theme}")
        # Burada ana pencereye de tema uygulanacaksa, sinyal ile ana pencereye bilgi gönderebilirsin

    def toggle_pw_fields(self):
        self.pw_fields.setVisible(not self.pw_fields.isVisible())

    def save_password(self):
        eski = self.old_pw.text()
        yeni = self.new_pw.text()
        user_file = "user_info.txt"
        if not eski or not yeni:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return
        if not os.path.exists(user_file):
            QMessageBox.warning(self, "Hata", "Kullanıcı bilgisi bulunamadı!")
            return
        with open(user_file, "r") as f:
            lines = f.readlines()
        current_pw = lines[1].strip() if len(lines) > 1 else ""
        if eski != current_pw:
            QMessageBox.warning(self, "Hata", "Eski parola yanlış!")
            return
        lines[1] = yeni + "\n"
        with open(user_file, "w") as f:
            f.writelines(lines)
        QMessageBox.information(self, "Başarılı", "Parola başarıyla değiştirildi! Giriş ekranına yönlendiriliyorsunuz.")
        self.old_pw.clear()
        self.new_pw.clear()
        self.pw_fields.setVisible(False)
        # Ana pencereyi kapat
        if self.main_window is not None:
            self.main_window.close()
        self.close()
        from proj import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

    def reset_all(self):
        # finance.db dosyasını sil
        db_path = "finance.db"
        onay = QMessageBox.question(self, "Onay", "Tüm finansal veriler (gelir, gider, raporlar) silinecek. Emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if onay == QMessageBox.Yes:
            if os.path.exists(db_path):
                try:
                    os.remove(db_path)
                    QMessageBox.information(self, "Başarılı", "Tüm finansal veriler silindi!")
                except Exception as e:
                    QMessageBox.warning(self, "Hata", f"Veriler silinemedi: {e}")
            else:
                QMessageBox.information(self, "Bilgi", "Zaten silinecek veri bulunamadı.")

    def apply_theme(self):
        tema = self.theme_combo.currentText()
        if tema == "Açık":
            self.setStyleSheet("background-color: #FFF5E6;")
        else:
            self.setStyleSheet("background-color: #232323; color: white;")
        # Diğer widget'lar için de gerekirse stil güncellenebilir

    def save_settings(self):
        tema = self.theme_combo.currentText()
        kullanici_adi = self.username_input.text().strip()
        # Burada ayarları kaydetme işlemleri yapılabilir
        QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi!")

    def change_theme(self, theme_name):
        save_theme(theme_name)
        theme = THEMES[theme_name]
        # Tüm açık pencerelere uygula
        self.setStyleSheet(f"background-color: {theme['background']}; color: {theme['foreground']};")
        if self.main_window:
            self.main_window.setStyleSheet(f"background-color: {theme['background']}; color: {theme['foreground']};")
        QMessageBox.information(self, "Başarılı", f"Tema başarıyla değiştirildi!\nTema rengi: {theme_name}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())