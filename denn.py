import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt, QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # Başlık etiketi
        title_label = QLabel('Finans Takip - Ana Sayfa')
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
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_button)
        
        # Ana sayfa içeriği
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # İşlem blokları
        blocks = [
            ('Gelir ve\nİşlemler', '💰'),
            ('Gider\nİşlemleri', '💳'),
            ('Nakit\nAkışı', '📊'),
            ('Bütçe\nYönetimi', '📈'),
            ('Bilanço\nTablosu', '📑'),
            ('Gelir\nTablosu', '📋'),
            ('Mali\nAnalizler', '📊'),
            ('Finansal\nRaporlar', '📝')
        ]
        
        for i, (text, icon) in enumerate(blocks):
            block = QPushButton(f'{icon}\n{text}')
            block.setFixedSize(200, 140)
            block.setStyleSheet("""
                QPushButton {
                    background-color: #D94E1F;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: bold;
                    text-align: center;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #B33D15;
                }
            """)
            content_layout.addWidget(block, i // 4, i % 4)
        
        layout.addWidget(title_bar)
        layout.addWidget(content_widget)
        
        self.center()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())