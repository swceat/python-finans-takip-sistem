from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QDateEdit, QMessageBox, QComboBox,
                            QApplication, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPainter, QPdfWriter, QTextDocument
import os

class IncomeStatementReport(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gelir Tablosu Raporu')
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
        title_label = QLabel('Gelir Tablosu Raporu')
        title_label.setStyleSheet('color: white; font-size: 28px; font-weight: bold;')
        
        # Rapor oluştur butonu
        self.generate_report_button = QPushButton('📄 Rapor Oluştur')
        self.generate_report_button.setStyleSheet("""
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
        self.generate_report_button.clicked.connect(self.generate_report)
        
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
        title_layout.addWidget(self.generate_report_button)
        title_layout.addWidget(close_button)
        
        # Filtre bölümü
        filter_widget = QWidget()
        filter_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QDateEdit, QComboBox {
                padding: 5px;
                border: 2px solid #D94E1F;
                border-radius: 5px;
                min-width: 150px;
            }
        """)
        filter_layout = QHBoxLayout(filter_widget)
        
        # Başlangıç tarihi
        start_date_label = QLabel('Başlangıç Tarihi:')
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        
        # Bitiş tarihi
        end_date_label = QLabel('Bitiş Tarihi:')
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        
        # Rapor türü
        report_type_label = QLabel('Rapor Türü:')
        self.report_type = QComboBox()
        self.report_type.addItems(['Aylık', 'Üç Aylık', 'Yıllık'])
        
        filter_layout.addWidget(start_date_label)
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(end_date_label)
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(report_type_label)
        filter_layout.addWidget(self.report_type)
        filter_layout.addStretch()
        
        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Kalem', 'Önceki Dönem', 'Cari Dönem', 'Değişim %'])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #FFE0E0;
            }
            QHeaderView::section {
                background-color: #D94E1F;
                color: white;
                padding: 8px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                font-size: 14px;
            }
        """)
        
        # Tablo sütunlarını otomatik genişlet
        header = self.table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Widget'ları ana layout'a ekle
        layout.addWidget(title_bar)
        layout.addWidget(filter_widget)
        layout.addWidget(self.table)
        
        self.add_sample_data()
        
    def add_sample_data(self):
        items = [
            ('Hasılat', '1,000,000.00 ₺', '1,200,000.00 ₺', '+20.00%'),
            ('Satışların Maliyeti (-)', '600,000.00 ₺', '700,000.00 ₺', '+16.67%'),
            ('BRÜT KAR/ZARAR', '400,000.00 ₺', '500,000.00 ₺', '+25.00%'),
            ('Faaliyet Giderleri (-)', '200,000.00 ₺', '250,000.00 ₺', '+25.00%'),
            ('FAALİYET KARI/ZARARI', '200,000.00 ₺', '250,000.00 ₺', '+25.00%'),
            ('Finansman Gelirleri', '50,000.00 ₺', '60,000.00 ₺', '+20.00%'),
            ('Finansman Giderleri (-)', '30,000.00 ₺', '35,000.00 ₺', '+16.67%'),
            ('DÖNEM NET KARI/ZARARI', '220,000.00 ₺', '275,000.00 ₺', '+25.00%')
        ]
        
        self.table.setRowCount(len(items))
        for row, (item, prev, curr, change) in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item))
            self.table.setItem(row, 1, QTableWidgetItem(prev))
            self.table.setItem(row, 2, QTableWidgetItem(curr))
            self.table.setItem(row, 3, QTableWidgetItem(change))
            
            # Ana başlıkları kalın yap
            if item in ['BRÜT KAR/ZARAR', 'FAALİYET KARI/ZARARI', 'DÖNEM NET KARI/ZARARI']:
                for col in range(4):
                    self.table.item(row, col).setFont(QFont('Arial', 10, QFont.Bold))
    
    def generate_report(self):
        try:
            # PDF dosya adını oluştur
            start_date = self.start_date.date().toString('dd.MM.yyyy')
            end_date = self.end_date.date().toString('dd.MM.yyyy')
            filename = f'Gelir_Tablosu_Raporu_{start_date}-{end_date}.pdf'
            
            # PDF yazıcı oluştur
            writer = QPdfWriter(filename)
            writer.setPageSize(QPdfWriter.A4)
            
            # Painter oluştur
            painter = QPainter()
            painter.begin(writer)
            
            # HTML içeriği oluştur
            html = f"""
            <html>
            <head>
                <style>
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                    th {{ background-color: #D94E1F; color: white; }}
                </style>
            </head>
            <body>
                <h1 style="text-align: center;">Gelir Tablosu Raporu</h1>
                <p>Dönem: {start_date} - {end_date}</p>
                <p>Rapor Türü: {self.report_type.currentText()}</p>
                <table>
                    <tr>
                        <th>Kalem</th>
                        <th>Önceki Dönem</th>
                        <th>Cari Dönem</th>
                        <th>Değişim %</th>
                    </tr>
            """
            
            # Tablo verilerini ekle
            for row in range(self.table.rowCount()):
                html += "<tr>"
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        html += f"<td>{item.text()}</td>"
                    else:
                        html += "<td></td>"
                html += "</tr>"
            
            html += """
                </table>
            </body>
            </html>
            """
            
            # HTML'i PDF'e dönüştür
            document = QTextDocument()
            document.setHtml(html)
            document.setPageSize(writer.pageRect().size())
            document.drawContents(painter)
            
            painter.end()
            
            QMessageBox.information(
                self,
                'Başarılı',
                f'Rapor başarıyla oluşturuldu!\nDosya: {filename}',
                QMessageBox.Ok
            )
            
            # PDF'i aç
            os.startfile(filename)
            
        except Exception as e:
            QMessageBox.warning(
                self,
                'Hata',
                f'Rapor oluşturulurken bir hata oluştu:\n{str(e)}',
                QMessageBox.Ok
            )