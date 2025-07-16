from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QApplication, QMessageBox)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Finans Takip - Giriş')
        self.setFixedSize(400, 500)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #FFF5E6;
            }
        ''')
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Ana widget ve layout
        central_widget = QWidget()
        central_widget.setStyleSheet('''
            QWidget {
                background-color: #FFF5E6;
            }
        ''')
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 40)
        layout.setSpacing(20)
        
        # Başlık çubuğu
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setFixedWidth(400)
        title_bar.setStyleSheet('''
            QWidget {
                background-color: #D94E1F;
            }
        ''')
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 0, 15, 0)
        
        # Başlık etiketi
        window_title = QLabel('Finans Takip - Giriş')
        window_title.setStyleSheet('color: white; font-size: 18px; font-weight: bold;')
        
        # Kapatma butonu
        close_button = QPushButton('×')
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
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
        close_button.clicked.connect(self.close)
        
        title_bar_layout.addWidget(window_title)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)
        
        layout.addWidget(title_bar)
        
        # Logo ve başlık
        title_label = QLabel('Finans Takip')
        title_label.setStyleSheet('color: #D94E1F; font-size: 38px; font-weight: bold;')
        title_label.setAlignment(Qt.AlignCenter)
        
        # Kullanıcı adı girişi
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Kullanıcı Adı')
        self.username_input.setFixedSize(300, 40)
        self.username_input.setStyleSheet("""
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
        
        # Şifre girişi
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Şifre')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(300, 40)
        self.password_input.setStyleSheet("""
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
        self.login_button = QPushButton('Giriş Yap')
        self.login_button.setFixedSize(300, 40)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.login)
        
        # Diğer widget'ları ekle
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)  # Boşluk artırıldı
        content_layout.setContentsMargins(0, 40, 0, 40)  # Üst ve alt marjin eklendi
        content_layout.addWidget(title_label)
        content_layout.addWidget(self.username_input)
        content_layout.addWidget(self.password_input)
        content_layout.addWidget(self.login_button)
        
        layout.addStretch()
        layout.addWidget(content_widget)
        layout.addStretch()
        
        self.center()
        
        # Buton animasyonu için event filter
        self.login_button.installEventFilter(self)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
    
    def eventFilter(self, obj, event):
        if obj == self.login_button:
            if event.type() == event.Enter:
                # Hover başladığında büyütme animasyonu
                self.animation = QPropertyAnimation(self.login_button, b'pos')
                self.animation.setDuration(200)
                current_pos = self.login_button.pos()
                self.animation.setStartValue(current_pos)
                self.animation.setEndValue(current_pos - QPoint(3, 3))
                self.animation.setEasingCurve(QEasingCurve.OutCubic)
                self.animation.start()
            elif event.type() == event.Leave:
                # Hover bittiğinde küçültme animasyonu
                self.animation = QPropertyAnimation(self.login_button, b'pos')
                self.animation.setDuration(200)
                current_pos = self.login_button.pos()
                self.animation.setStartValue(current_pos)
                self.animation.setEndValue(current_pos + QPoint(3, 3))
                self.animation.setEasingCurve(QEasingCurve.OutCubic)
                self.animation.start()
        return super().eventFilter(obj, event)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "admin" and password == "1234":
            # Burada ana pencereye geçiş yapılacak
            QMessageBox.information(
                self,
                'Başarılı',
                'Giriş başarılı!',
                QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self,
                'Hata',
                'Kullanıcı adı veya şifre hatalı!',
                QMessageBox.Ok
            )
            self.password_input.clear()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())