import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys
import subprocess

# Global renk tanımlamaları
BG_COLOR = '#fff5f0'        # Krem rengi arka plan
CARD_COLOR = '#e0592a'      # Ana turuncu
HOVER_COLOR = '#ff6b3d'     # Hover için açık turuncu
TEXT_COLOR = 'white'        # Metin rengi
HEADER_COLOR = '#8B2000'    # Koyu turuncu
BUTTON_COLOR = '#e0592a'    # Buton rengi

class LoginScreen:
    # Sabit değişkenler
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "1234"
    
    # Renk tanımlamaları
    BG_COLOR = '#fff5f0'        # Krem rengi arka plan
    DARK_ORANGE = '#8B2000'     # Koyu turuncu
    MAIN_ORANGE = '#e0592a'     # Ana turuncu
    LIGHT_ORANGE = '#ff6b3d'    # Açık turuncu
    ENTRY_BG = '#fff1e6'        # Giriş alanı arka plan
    FOCUS_BG = '#fff9f6'        # Odaklanma arka plan

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Giriş")
        
        # Pencere başlık çubuğunu kaldır
        self.root.overrideredirect(True)
        
        # Pencere boyutu ve konumu
        window_width = 300
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Ana container
        self.container = tk.Frame(self.root, bg=self.BG_COLOR)
        self.container.pack(fill='both', expand=True)
        
        # Özel başlık çubuğu
        self.title_bar = tk.Frame(self.container, bg=self.DARK_ORANGE, height=35)
        self.title_bar.pack(fill='x')
        self.title_bar.pack_propagate(False)
        
        # Başlık etiketi
        self.title_label = tk.Label(self.title_bar, text="Finans Takip", 
                                  bg=self.DARK_ORANGE, fg='white',
                                  font=('Segoe UI Semibold', 11))
        self.title_label.pack(side='left', padx=10)
        
        # Çarpı butonu
        self.close_button = tk.Button(self.title_bar, text='×',
                                    bg=self.DARK_ORANGE, fg='white',
                                    font=('Segoe UI', 13), bd=0,
                                    activebackground=self.MAIN_ORANGE,
                                    command=self.quit_app)
        self.close_button.pack(side='right', padx=10)
        
        # Ana içerik frame'i
        self.frame = tk.Frame(self.container, bg=self.BG_COLOR)
        self.frame.pack(pady=25, padx=35, fill='both', expand=True)

        # Kullanıcı Adı Label
        tk.Label(self.frame,
                text="Kullanıcı Adı",
                font=('Segoe UI', 10),
                fg='#666666',
                bg=self.BG_COLOR).pack(anchor='w', pady=(25,5))

        # Kullanıcı Adı Entry Frame
        self.username_frame = tk.Frame(self.frame, bg=self.MAIN_ORANGE, padx=1, pady=1)
        self.username_frame.pack(fill='x')
        
        self.username_entry = tk.Entry(self.username_frame,
                                     font=('Segoe UI', 11),
                                     bg=self.ENTRY_BG,
                                     fg='#333333',
                                     relief='flat',
                                     insertbackground='#666666')
        self.username_entry.pack(fill='x', padx=1, pady=1)

        # Şifre Label
        tk.Label(self.frame,
                text="Şifre",
                font=('Segoe UI', 10),
                fg='#666666',
                bg=self.BG_COLOR).pack(anchor='w', pady=(15,5))

        # Şifre Entry Frame
        self.password_frame = tk.Frame(self.frame, bg=self.MAIN_ORANGE, padx=1, pady=1)
        self.password_frame.pack(fill='x')
        
        # Şifre Entry ve göster/gizle butonu için container
        self.pass_container = tk.Frame(self.password_frame, bg=self.ENTRY_BG)
        self.pass_container.pack(fill='x', padx=1, pady=1)
        
        self.password_entry = tk.Entry(self.pass_container,
                                     font=('Segoe UI', 11),
                                     bg=self.ENTRY_BG,
                                     fg='#333333',
                                     relief='flat',
                                     show="•",
                                     insertbackground='#666666')
        self.password_entry.pack(side='left', fill='x', expand=True)
        
        # Şifre göster/gizle butonu
        self.show_password = False
        self.toggle_btn = tk.Button(self.pass_container,
                                  text="👁",
                                  font=('Segoe UI', 10),
                                  bg=self.ENTRY_BG,
                                  fg='#666666',
                                  bd=0,
                                  padx=5,
                                  activebackground=self.ENTRY_BG,
                                  cursor='hand2',
                                  command=self.toggle_password)
        self.toggle_btn.pack(side='right')

        # Entry'lere focus efektleri
        self.username_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.password_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Enter tuşu ile giriş
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())

        # Giriş Butonu
        self.login_button = tk.Button(self.frame,
                                    text="Giriş Yap",
                                    font=('Segoe UI Semibold', 11),
                                    bg=self.MAIN_ORANGE,
                                    fg='white',
                                    relief='flat',
                                    activebackground=self.LIGHT_ORANGE,
                                    activeforeground='white',
                                    cursor='hand2',
                                    command=self.login)
        self.login_button.pack(fill='x', pady=(30,0))

        # Hata mesajı label'ı
        self.error_label = tk.Label(self.frame,
                                  text="",
                                  font=('Segoe UI', 9),
                                  fg='red',
                                  bg=self.BG_COLOR)
        self.error_label.pack(pady=(10,0))

        # Pencere sürükleme için event'ler
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        
        # Pencereyi ortala
        self.center_window()
        
        self.root.mainloop()

    def quit_app(self):
        """Uygulamayı kapat"""
        self.root.quit()
        self.root.destroy()

    def toggle_password(self):
        """Şifreyi göster/gizle"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="🔒")
        else:
            self.password_entry.config(show="•")
            self.toggle_btn.config(text="👁")

    def on_entry_focus_in(self, event):
        event.widget.master.configure(bg=self.LIGHT_ORANGE)
        event.widget.configure(bg=self.FOCUS_BG)
        if hasattr(event.widget, 'master'):
            for widget in event.widget.master.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=self.FOCUS_BG)

    def on_entry_focus_out(self, event):
        event.widget.master.configure(bg=self.MAIN_ORANGE)
        event.widget.configure(bg=self.ENTRY_BG)
        if hasattr(event.widget, 'master'):
            for widget in event.widget.master.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=self.ENTRY_BG)

    def show_error(self, message):
        """Hata mesajını göster"""
        self.error_label.config(text=message)
        self.root.after(2000, lambda: self.error_label.config(text=""))

    def login(self):
        """Giriş kontrolü"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            self.root.destroy()
            
            # Yeni pencere
            new_window = tk.Tk()
            new_window.title("Yönetim Platformu")
            
            # Pencere boyutu
            window_width = 1200
            window_height = 800
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Ana container
            main_frame = tk.Frame(new_window, bg=BG_COLOR)
            main_frame.pack(fill='both', expand=True, padx=40, pady=40)
            
            # İlk menüyü göster
            show_main_menu(main_frame)
            
            new_window.mainloop()
        else:
            self.show_error("Kullanıcı adı veya şifre hatalı!")
            self.password_entry.delete(0, 'end')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def create_rounded_button(parent, icon, text, row, col):
    """Yuvarlak kenarlı buton oluştur"""
    frame = tk.Frame(parent, bg=BG_COLOR)
    frame.grid(row=row, column=col, padx=5, pady=5)
    
    canvas = tk.Canvas(frame, width=150, height=100, 
                      bg=CARD_COLOR, highlightthickness=0)
    canvas.pack()
    
    # Yuvarlak köşeler için
    radius = 10
    
    def draw_rounded_rect(color):
        canvas.delete('all')
        canvas.create_rectangle(radius, 0, 150-radius, 100, 
                              fill=color, outline=color)
        canvas.create_rectangle(0, radius, 150, 100-radius, 
                              fill=color, outline=color)
        canvas.create_arc(0, 0, radius*2, radius*2, 
                         start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(150-radius*2, 0, 150, radius*2, 
                         start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(0, 100-radius*2, radius*2, 100, 
                         start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(150-radius*2, 100-radius*2, 150, 100, 
                         start=270, extent=90, fill=color, outline=color)
        canvas.create_text(75, 35, text=icon, font=('Segoe UI', 24), fill=TEXT_COLOR)
        canvas.create_text(75, 70, text=text, font=('Segoe UI', 10, 'bold'), 
                          fill=TEXT_COLOR, justify='center')
    
    draw_rounded_rect(CARD_COLOR)
    
    def on_enter(e):
        draw_rounded_rect(HOVER_COLOR)
    
    def on_leave(e):
        draw_rounded_rect(CARD_COLOR)
    
    canvas.bind('<Enter>', on_enter)
    canvas.bind('<Leave>', on_leave)
    canvas.bind('<Button-1>', lambda e: open_section(text, parent.master))
    
    return canvas

def show_main_menu(main_frame):
    """Ana menüyü göster"""
    # Mevcut içeriği temizle
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Başlık
    tk.Label(main_frame,
            text="YÖNETİM PLATFORMU",
            font=('Segoe UI', 24, 'bold'),
            fg='#8B2000',
            bg=BG_COLOR).pack(pady=(0,30))
    
    # Butonlar için frame
    buttons_frame = tk.Frame(main_frame, bg=BG_COLOR)
    buttons_frame.pack(expand=True)
    
    # Buton bilgileri
    buttons = [
        ("💰", "Gelir ve\nSatışlar"),
        ("💳", "Giderler ve\nMasraflar"),
        ("📊", "Nakit\nAkışı"),
        ("📈", "Bütçe\nYönetimi"),
        ("📑", "Bilanço\nTakibi"),
        ("📋", "Gelir\nTablosu"),
        ("📊", "Mali\nAnaliz"),
        ("📉", "Finansal\nRaporlar"),
        ("🏦", "Banka\nİşlemleri"),
        ("💼", "Cari\nHesaplar"),
        ("📝", "Fatura\nYönetimi"),
        ("🔄", "Borç/Alacak\nTakibi")
    ]
    
    # Grid ağırlıkları
    for i in range(4):
        buttons_frame.grid_columnconfigure(i, weight=1)
    for i in range(3):
        buttons_frame.grid_rowconfigure(i, weight=1)
    
    # Butonları oluştur
    for i, (icon, text) in enumerate(buttons):
        create_rounded_button(buttons_frame, icon, text, i//4, i%4)

def show_add_record_dialog(tree):
    """Yeni kayıt ekleme penceresi"""
    dialog = tk.Toplevel()
    dialog.title("Yeni Kayıt Ekle")
    
    # Pencereyi ana pencereye göre boyutlandır
    window_width = dialog.master.winfo_width() - 100
    window_height = dialog.master.winfo_height() - 100
    x = dialog.master.winfo_x() + 50
    y = dialog.master.winfo_y() + 50
    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Ana frame'i grid ile yapılandır
    dialog.grid_columnconfigure(0, weight=1)
    dialog.grid_rowconfigure(0, weight=1)
    
    # Ana container
    main_frame = tk.Frame(dialog, bg=BG_COLOR)
    main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Başlık
    tk.Label(main_frame,
            text="Yeni Kayıt Ekle",
            font=('Segoe UI', 16, 'bold'),
            fg=HEADER_COLOR,
            bg=BG_COLOR).grid(row=0, column=0, sticky='w', pady=(0, 20))
    
    # Form için frame
    form_frame = tk.Frame(main_frame, bg=BG_COLOR)
    form_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 20))
    form_frame.grid_columnconfigure(0, weight=1)
    
    # Form elemanları için sözlük
    entries = {}
    current_row = 0
    
    # Tarih Frame
    date_frame = tk.Frame(form_frame, bg=BG_COLOR)
    date_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    date_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(date_frame,
            text="Tarih:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    date_select_frame = tk.Frame(date_frame, bg=BG_COLOR)
    date_select_frame.grid(row=0, column=1, sticky='ew', pady=(5,0))
    
    # Gün
    day = ttk.Combobox(date_select_frame, values=[str(i).zfill(2) for i in range(1,32)],
                     width=5, state='readonly', font=('Segoe UI', 11))
    day.grid(row=0, column=0, padx=(0,5))
    day.set("01")
    
    # Ay
    month = ttk.Combobox(date_select_frame, 
                       values=["01", "02", "03", "04", "05", "06", 
                             "07", "08", "09", "10", "11", "12"],
                       width=5, state='readonly', font=('Segoe UI', 11))
    month.grid(row=0, column=1, padx=5)
    month.set("01")
    
    # Yıl
    year = ttk.Combobox(date_select_frame, 
                      values=[str(i) for i in range(2024,2030)],
                      width=7, state='readonly', font=('Segoe UI', 11))
    year.grid(row=0, column=2, padx=5)
    year.set("2024")
    
    entries['Tarih'] = (day, month, year)
    current_row += 1
    
    # Kategori Frame
    category_frame = tk.Frame(form_frame, bg=BG_COLOR)
    category_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    category_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(category_frame,
            text="Kategori:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    category = ttk.Combobox(category_frame,
                         values=["Ürün Satışları", "Hizmet Gelirleri", "Diğer Gelirler"],
                         state='readonly',
                         font=('Segoe UI', 11))
    category.grid(row=0, column=1, sticky='ew', pady=(5,0))
    category.set("Ürün Satışları")
    entries['Kategori'] = category
    current_row += 1
    
    # Açıklama Frame
    desc_frame = tk.Frame(form_frame, bg=BG_COLOR)
    desc_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    desc_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(desc_frame,
            text="Açıklama:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    desc_entry = tk.Entry(desc_frame, font=('Segoe UI', 11))
    desc_entry.grid(row=0, column=1, sticky='ew', pady=(5,0))
    entries['Açıklama'] = desc_entry
    current_row += 1
    
    # Tutar Frame
    amount_frame = tk.Frame(form_frame, bg=BG_COLOR)
    amount_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    amount_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(amount_frame,
            text="Tutar (₺):",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    def validate_amount(P):
        if P == "": return True
        try:
            float(P.replace(',', '.'))
            return True
        except ValueError:
            return False
    
    vcmd = (dialog.register(validate_amount), '%P')
    amount_entry = tk.Entry(amount_frame, font=('Segoe UI', 11),
                          validate='key', validatecommand=vcmd)
    amount_entry.grid(row=0, column=1, sticky='ew', pady=(5,0))
    entries['Tutar'] = amount_entry
    current_row += 1
    
    # Ödeme Şekli Frame
    payment_frame = tk.Frame(form_frame, bg=BG_COLOR)
    payment_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    payment_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(payment_frame,
            text="Ödeme Şekli:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    payment = ttk.Combobox(payment_frame,
                        values=["Nakit", "Kredi Kartı", "Havale/EFT", "Çek", "Diğer"],
                        state='readonly',
                        font=('Segoe UI', 11))
    payment.grid(row=0, column=1, sticky='ew', pady=(5,0))
    payment.set("Nakit")
    entries['Ödeme'] = payment
    current_row += 1
    
    # Durum Frame
    status_frame = tk.Frame(form_frame, bg=BG_COLOR)
    status_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    status_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(status_frame,
            text="Durum:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    status = ttk.Combobox(status_frame,
                       values=["Tamamlandı", "Beklemede", "İptal Edildi"],
                       state='readonly',
                       font=('Segoe UI', 11))
    status.grid(row=0, column=1, sticky='ew', pady=(5,0))
    status.set("Tamamlandı")
    entries['Durum'] = status
    current_row += 1
    
    # Not Frame
    note_frame = tk.Frame(form_frame, bg=BG_COLOR)
    note_frame.grid(row=current_row, column=0, sticky='ew', pady=5)
    note_frame.grid_columnconfigure(1, weight=1)
    
    tk.Label(note_frame,
            text="Not:",
            font=('Segoe UI', 10),
            fg='#666666',
            bg=BG_COLOR).grid(row=0, column=0, sticky='w')
    
    note_entry = tk.Text(note_frame, height=3, font=('Segoe UI', 11))
    note_entry.grid(row=0, column=1, sticky='ew', pady=(5,0))
    entries['Not'] = note_entry
    current_row += 1
    
    # Butonlar için frame
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.grid(row=current_row, column=0, sticky='ew', pady=(20,0))
    button_frame.grid_columnconfigure(1, weight=1)
    
    # İptal Butonu
    tk.Button(button_frame,
             text="İptal",
             font=('Segoe UI', 11),
             bg='#dc3545',
             fg='white',
             padx=20,
             pady=5,
             relief='flat',
             cursor='hand2',
             command=dialog.destroy).grid(row=0, column=0, padx=5)
    
    # Kaydet Butonu
    tk.Button(button_frame,
             text="Kaydet",
             font=('Segoe UI', 11),
             bg=BUTTON_COLOR,
             fg='white',
             padx=20,
             pady=5,
             relief='flat',
             cursor='hand2',
             command=lambda: save_record(entries, tree, dialog)).grid(row=0, column=2, padx=5)
    
    dialog.transient(dialog.master)
    dialog.grab_set()

def save_record(entries, tree, dialog):
    """Kayıt ekleme fonksiyonu"""
    # Tarih değerlerini al
    day, month, year = entries['Tarih']
    date = f"{day.get()}/{month.get()}/{year.get()}"
    
    # Diğer değerleri al
    values = [
        date,
        entries['Kategori'].get(),
        entries['Açıklama'].get(),
        f"₺{entries['Tutar'].get()}",
        entries['Ödeme'].get(),
        entries['Durum'].get()
    ]
    
    # Tabloya ekle
    tree.insert('', 'end', values=values)
    dialog.destroy()

def show_category_dialog():
    """Kategori yönetimi penceresi"""
    dialog = tk.Toplevel()
    dialog.title("Kategori Yönetimi")
    dialog.geometry("300x400")
    # Dialog içeriği...

def reset_records(tree):
    """Kayıtları sıfırla"""
    if messagebox.askyesno("Kayıtları Sıfırla", 
                             "Tüm kayıtlar silinecek. Emin misiniz?"):
        for item in tree.get_children():
            tree.delete(item)
        update_summary_values()  # Özet değerlerini güncelle

def refresh_sales_data(tree):
    """Verileri yenile"""
    # Verileri yeniden yükle...
    pass

def open_section(section_name, main_frame):
    """Seçilen bölümü aç"""
    # Mevcut içeriği temizle
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    if section_name == "Gelir ve\nSatışlar":
        # Ana frame'i grid ile yapılandır
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)  # Content için
        
        # Üst menü çubuğu
        top_bar = tk.Frame(main_frame, bg=HEADER_COLOR)
        top_bar.grid(row=0, column=0, sticky='ew')
        
        # Geri dönüş butonu
        back_button = tk.Button(top_bar,
                              text="← Ana Menü",
                              font=('Segoe UI', 10),
                              bg=HEADER_COLOR,
                              fg='white',
                              bd=0,
                              padx=15,
                              pady=8,
                              activebackground=BUTTON_COLOR,
                              activeforeground='white',
                              cursor='hand2',
                              command=lambda: show_main_menu(main_frame))
        back_button.pack(side='left')
        
        # Yenile butonu
        refresh_button = tk.Button(top_bar,
                                 text="⟳ Yenile",
                                 font=('Segoe UI', 10),
                                 bg=HEADER_COLOR,
                                 fg='white',
                                 bd=0,
                                 padx=15,
                                 pady=8,
                                 activebackground=BUTTON_COLOR,
                                 activeforeground='white',
                                 cursor='hand2',
                                 command=lambda: refresh_sales_data(tree))
        refresh_button.pack(side='left')
        
        # Ana içerik container
        content_frame = tk.Frame(main_frame, bg=BG_COLOR)
        content_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(2, weight=1)  # Tablo için
        
        # Başlık ve butonlar
        header_frame = tk.Frame(content_frame, bg=BG_COLOR)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)  # Başlık ve butonlar arası boşluk
        
        tk.Label(header_frame,
                text="Gelir ve Satışlar Yönetimi",
                font=('Segoe UI', 20, 'bold'),
                fg=HEADER_COLOR,
                bg=BG_COLOR).grid(row=0, column=0, sticky='w')
        
        # Butonlar için frame
        buttons_frame = tk.Frame(header_frame, bg=BG_COLOR)
        buttons_frame.grid(row=0, column=1, sticky='e')
        
        # Yeni Kayıt Butonu
        tk.Button(buttons_frame,
                 text="+ Yeni Kayıt",
                 font=('Segoe UI', 11),
                 bg=BUTTON_COLOR,
                 fg='white',
                 padx=15,
                 pady=5,
                 relief='flat',
                 cursor='hand2',
                 command=lambda: show_add_record_dialog(tree)).grid(row=0, column=2, padx=5)
        
        # Kategori Yönetimi Butonu
        tk.Button(buttons_frame,
                 text="⚙ Kategori Yönetimi",
                 font=('Segoe UI', 11),
                 bg=BUTTON_COLOR,
                 fg='white',
                 padx=15,
                 pady=5,
                 relief='flat',
                 cursor='hand2',
                 command=show_category_dialog).grid(row=0, column=1, padx=5)
        
        # Kayıtları Sıfırla Butonu
        tk.Button(buttons_frame,
                 text="🗑 Kayıtları Sıfırla",
                 font=('Segoe UI', 11),
                 bg='#dc3545',
                 fg='white',
                 padx=15,
                 pady=5,
                 relief='flat',
                 cursor='hand2',
                 command=lambda: reset_records(tree)).grid(row=0, column=0, padx=5)
        
        # Tablo Frame
        table_frame = tk.Frame(content_frame, bg='white')
        table_frame.grid(row=2, column=0, sticky='nsew')
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Tablo oluştur
        columns = ('Tarih', 'Kategori', 'Açıklama', 'Tutar', 'Ödeme Şekli', 'Durum')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Başlıkları ayarla
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        tree.grid(row=0, column=0, sticky='nsew')
        
        # Özet Frame
        summary_frame = tk.Frame(content_frame, bg='white')
        summary_frame.grid(row=3, column=0, sticky='ew', pady=(20, 0))
        summary_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Özet bilgileri
        summaries = [
            ('Toplam Gelir', '₺0'),
            ('Aylık Ortalama', '₺0'),
            ('En Yüksek İşlem', '₺0'),
            ('Bekleyen Ödemeler', '₺0')
        ]
        
        for i, (label, value) in enumerate(summaries):
            frame = tk.Frame(summary_frame, bg='white', padx=20)
            frame.grid(row=0, column=i, sticky='ew')
            
            tk.Label(frame,
                    text=label,
                    font=('Segoe UI', 10),
                    fg='#666666',
                    bg='white').grid(row=0, column=0)
            
            tk.Label(frame,
                    text=value,
                    font=('Segoe UI', 14, 'bold'),
                    fg=HEADER_COLOR,
                    bg='white').grid(row=1, column=0)

def update_summary_values():
    """Özet değerlerini güncelle"""
    pass  # Bu fonksiyon daha sonra implement edilecek

if __name__ == "__main__":
    LoginScreen()
