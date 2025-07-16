from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QLineEdit, QDateEdit, QMessageBox,
                            QApplication)
from PyQt5.QtCore import Qt, QDate

class NewIncomeTransactionPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yeni Gelir Kaydı')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(800, 600)
        self.setStyleSheet('background-color: #FFF5E6;')
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Başlık çubuğu
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet('background-color: #D94E1F;')
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
        title_label = QLabel('Yeni Gelir Kaydı')
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
        
        # Form içeriği
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background-color: #FFF5E6;
                border-radius: 20px;
                margin: 20px;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: black;
                min-width: 120px;
            }
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 2px solid #D94E1F;
                border-radius: 8px;
                font-size: 16px;
                min-width: 300px;
                min-height: 35px;
                background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                border-color: #B33D15;
            }
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(25)
        
        # Form elemanları
        # Tarih
        date_layout = QHBoxLayout()
        date_label = QLabel('Tarih:')
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        
        # Kategori
        category_layout = QHBoxLayout()
        category_label = QLabel('Kategori:')
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Kategori giriniz...')
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_input)
        category_layout.addStretch()
        
        # Tutar
        amount_layout = QHBoxLayout()
        amount_label = QLabel('Tutar (₺):')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('0.00')
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addStretch()
        
        # Açıklama
        description_layout = QHBoxLayout()
        description_label = QLabel('Açıklama:')
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText('Gelir açıklaması...')
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_input)
        description_layout.addStretch()
        
        # Kaydet butonu
        save_button = QPushButton('Kaydet')
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #D94E1F;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #B33D15;
            }
        """)
        save_button.clicked.connect(self.save_transaction)

        # Form öğelerini ekle
        form_layout.addLayout(date_layout)
        form_layout.addLayout(category_layout)
        form_layout.addLayout(amount_layout)
        form_layout.addLayout(description_layout)
        form_layout.addStretch()
        form_layout.addWidget(save_button, alignment=Qt.AlignCenter)
        
        # Widget'ları ana layout'a ekle
        layout.addWidget(title_bar)
        layout.addWidget(form_widget)
        
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
    
    def save_transaction(self):
        try:
            amount = float(self.amount_input.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, 'Hata', 'Lütfen geçerli bir tutar giriniz!', QMessageBox.Ok)
            return
        
        if amount <= 0:
            QMessageBox.warning(self, 'Hata', 'Tutar sıfırdan büyük olmalıdır!', QMessageBox.Ok)
            return
        
        if not self.category_input.text().strip():
            QMessageBox.warning(self, 'Hata', 'Lütfen bir kategori giriniz!', QMessageBox.Ok)
            return
        
        if not self.description_input.text().strip():
            QMessageBox.warning(self, 'Hata', 'Lütfen bir açıklama giriniz!', QMessageBox.Ok)
            return
        
        QMessageBox.information(
            self,
            'Başarılı',
            'Gelir kaydı başarıyla oluşturuldu!',
            QMessageBox.Ok
        )
        
        self.amount_input.clear()
        self.description_input.clear()
        self.category_input.clear()
        self.date_edit.setDate(QDate.currentDate())