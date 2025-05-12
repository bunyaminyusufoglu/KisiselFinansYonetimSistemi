import tkinter as tk
from tkinter import messagebox, ttk
from user import UserManager
from income import IncomeManager
from expense import ExpenseManager
from database import Database
from datetime import datetime

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kişisel Finans Yönetim Sistemi")
        self.root.state('zoomed')
        self.root.configure(bg="#f7f9fa")
        
        self.db = Database()
        self.user_manager = UserManager()
        self.income_manager = IncomeManager(self.user_manager.db)
        self.expense_manager = ExpenseManager(self.db)
        
        self.current_user = None
        self.setup_styles()
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f7f9fa")
        style.configure("Card.TFrame", background="#fff", relief="flat", borderwidth=0)
        style.configure("TLabel", background="#fff", foreground="#222", font=("Segoe UI", 11))
        style.configure("Header.TLabel", background="#fff", foreground="#222", font=("Segoe UI", 20, "bold"))
        style.configure("Subheader.TLabel", background="#fff", foreground="#555", font=("Segoe UI", 13, "bold"))
        style.configure("TButton", background="#1976d2", foreground="#fff", font=("Segoe UI", 11, "bold"), borderwidth=0, focusthickness=3, focuscolor="#1976d2", padding=8)
        style.map("TButton", background=[('active', '#1565c0')])
        style.configure("TEntry", fieldbackground="#f7f9fa", foreground="#222", font=("Segoe UI", 11), borderwidth=1)
        style.configure("TCombobox", fieldbackground="#f7f9fa", background="#f7f9fa", foreground="#222", font=("Segoe UI", 11))

    def show_login(self):
        self.clear_window()
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Kart çerçevesi
        card = ttk.Frame(main_frame, padding=40, style="Card.TFrame")
        card.pack()
        
        # Başlıklar
        ttk.Label(card, text="Kişisel Finans", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(card, text="Yönetim Sistemi", style="Subheader.TLabel").pack(pady=(0, 20))
        
        # Kullanıcı adı girişi
        ttk.Label(card, text="Kullanıcı Adı:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.username_entry = ttk.Entry(card, width=28)
        self.username_entry.pack(fill="x", pady=(0, 10))
        
        # Şifre girişi
        ttk.Label(card, text="Şifre:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.password_entry = ttk.Entry(card, show="•", width=28)
        self.password_entry.pack(fill="x", pady=(0, 18))
        
        # Butonlar
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Giriş Yap", command=self.login, style="TButton").pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Kayıt Ol", command=self.show_register, style="TButton").pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Stil ayarları
        style = ttk.Style()
        style.configure("Card.TFrame", background="#e0f7fa", relief="raised", borderwidth=2)
        style.configure("TLabel", background="#e0f7fa", foreground="#00796b", font=("Segoe UI", 11, "bold"))
        style.configure("Header.TLabel", background="#e0f7fa", foreground="#004d40", font=("Segoe UI", 20, "bold"))
        style.configure("Subheader.TLabel", background="#e0f7fa", foreground="#004d40", font=("Segoe UI", 13, "bold"))
        style.configure("TButton", background="#00796b", foreground="#fff", font=("Segoe UI", 11, "bold"), borderwidth=0, focusthickness=3, focuscolor="#00796b", padding=8)
        style.map("TButton", background=[('active', '#004d40')])

    def show_register(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=0, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        card = ttk.Frame(frame, padding=30, style="Card.TFrame")
        card.pack()
        ttk.Label(card, text="Yeni Hesap", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Kullanıcı Adı:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.reg_username_entry = ttk.Entry(card, width=28)
        self.reg_username_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="Şifre:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.reg_password_entry = ttk.Entry(card, show="•", width=28)
        self.reg_password_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="E-posta:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.reg_email_entry = ttk.Entry(card, width=28)
        self.reg_email_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="Ad Soyad:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.reg_fullname_entry = ttk.Entry(card, width=28)
        self.reg_fullname_entry.pack(fill="x", pady=(0, 18))
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Kayıt Ol", command=self.register).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Geri Dön", command=self.show_login).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def show_main_menu(self):
        self.clear_window()
        user_info = self.db.get_user_info(self.current_user)
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # Sol kısım: Butonlar
        left_frame = ttk.Frame(main_frame, style="TFrame")
        left_frame.pack(side="left", fill="y", expand=True)
        left_frame.pack_propagate(False)
        left_frame.config(width=int(self.root.winfo_screenwidth() * 0.6))
        
        # Üst başlık kartı
        header_card = ttk.Frame(left_frame, padding=15, style="Card.TFrame")
        header_card.pack(fill="x", pady=(0, 20))
        ttk.Label(header_card, 
                 text=f"Hoş Geldiniz, {user_info.get('full_name', user_info.get('username', ''))}",
                 style="Header.TLabel").pack(side="left")
        ttk.Button(header_card, text="Çıkış Yap", command=self.logout).pack(side="right")
        
        # Gelir İşlemleri Kartı
        income_card = ttk.Frame(left_frame, padding=20, style="Card.TFrame")
        income_card.pack(fill="x", pady=10)
        ttk.Label(income_card, text="Gelir İşlemleri", style="Subheader.TLabel").pack(pady=(0, 10))
        ttk.Button(income_card, text="Gelir Ekle", command=self.show_add_income).pack(fill="x", pady=5)
        ttk.Button(income_card, text="Gelir Raporu", command=self.show_income_report).pack(fill="x", pady=5)
        
        # Gider İşlemleri Kartı
        expense_card = ttk.Frame(left_frame, padding=20, style="Card.TFrame")
        expense_card.pack(fill="x", pady=10)
        ttk.Label(expense_card, text="Gider İşlemleri", style="Subheader.TLabel").pack(pady=(0, 10))
        ttk.Button(expense_card, text="Gider Ekle", command=self.show_add_expense).pack(fill="x", pady=5)
        ttk.Button(expense_card, text="Gider Raporu", command=self.show_expense_report).pack(fill="x", pady=5)
        
        # Hesap Ayarları Kartı
        settings_card = ttk.Frame(left_frame, padding=20, style="Card.TFrame")
        settings_card.pack(fill="x", pady=10)
        ttk.Label(settings_card, text="Hesap Ayarları", style="Subheader.TLabel").pack(pady=(0, 10))
        ttk.Button(settings_card, text="Profil Ayarları", command=self.show_profile_settings).pack(fill="x", pady=5)
        
        # Sağ kısım: İstatistikler
        right_frame = ttk.Frame(main_frame, style="TFrame")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Toplam Gelir Kartı
        total_income_card = ttk.Frame(right_frame, padding=20, style="Card.TFrame")
        total_income_card.pack(fill="x", pady=10)
        ttk.Label(total_income_card, text="Toplam Gelir", style="Subheader.TLabel").pack(pady=(0, 10))
        total_income = self.income_manager.get_income_summary(self.current_user)['total']
        ttk.Label(total_income_card, text=f"{total_income:.2f} TL", style="TLabel").pack()
        
        # Toplam Gider Kartı
        total_expense_card = ttk.Frame(right_frame, padding=20, style="Card.TFrame")
        total_expense_card.pack(fill="x", pady=10)
        ttk.Label(total_expense_card, text="Toplam Gider", style="Subheader.TLabel").pack(pady=(0, 10))
        total_expense = self.expense_manager.get_expense_summary(self.current_user)['total']
        ttk.Label(total_expense_card, text=f"{total_expense:.2f} TL", style="TLabel").pack()
        
        # Net Kalan Kartı
        net_balance_card = ttk.Frame(right_frame, padding=20, style="Card.TFrame")
        net_balance_card.pack(fill="x", pady=10)
        ttk.Label(net_balance_card, text="Net Kalan", style="Subheader.TLabel").pack(pady=(0, 10))
        net_balance = total_income - total_expense
        ttk.Label(net_balance_card, text=f"{net_balance:.2f} TL", style="TLabel").pack()

    def show_add_expense(self):
        self.clear_window()
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Kart çerçevesi
        card = ttk.Frame(main_frame, padding=40, style="Card.TFrame")
        card.pack()
        
        # Başlık
        ttk.Label(card, text="Gider Ekle", style="Header.TLabel").pack(pady=(0, 20))
        
        # Kategori girişi
        ttk.Label(card, text="Kategori:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.expense_category = ttk.Combobox(card, values=self.expense_manager.get_categories())
        self.expense_category.pack(fill="x", pady=(0, 10))
        
        # Tutar girişi
        ttk.Label(card, text="Tutar:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.expense_amount = ttk.Entry(card)
        self.expense_amount.pack(fill="x", pady=(0, 10))
        
        # Açıklama girişi
        ttk.Label(card, text="Açıklama:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.expense_description = ttk.Entry(card)
        self.expense_description.pack(fill="x", pady=(0, 18))
        
        # Butonlar
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Kaydet", command=self.save_expense, style="TButton").pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Geri Dön", command=self.show_main_menu, style="TButton").pack(side="left", expand=True, fill="x", padx=(5, 0))

    def show_expense_report(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Gider Raporu", font=("Helvetica", 16)).pack(pady=10)
        
        try:
            report = self.expense_manager.get_expense_summary(self.current_user)
            
            # Kategori bazında giderler
            for category, amount in report["by_category"].items():
                if amount > 0:
                    ttk.Label(frame, text=f"{category}: {amount:.2f} TL").pack(pady=5)
            
            ttk.Label(frame, text=f"Toplam Gider: {report['total']:.2f} TL", 
                     font=("Helvetica", 12, "bold")).pack(pady=10)
            
            # Gider düzenleme ve silme
            expense_entries = self.db.get_expense_entries(self.current_user)
            for entry in expense_entries:
                entry_frame = ttk.Frame(frame, style="Card.TFrame")
                entry_frame.pack(fill="x", pady=5)
                ttk.Label(entry_frame, text=f"{entry['category']}: {entry['amount']:.2f} TL - {entry['description']}", style="TLabel").pack(side="left")
                ttk.Button(entry_frame, text="Düzenle", command=lambda e=entry: self.edit_expense(e), style="TButton").pack(side="right", padx=5)
                ttk.Button(entry_frame, text="Sil", command=lambda e=entry: self.delete_expense(e), style="TButton").pack(side="right")
            
            ttk.Button(frame, text="Ana Menüye Dön", command=self.show_main_menu).pack(pady=10)
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.show_main_menu()

    def save_expense(self):
        try:
            category = self.expense_category.get()
            amount = float(self.expense_amount.get())
            description = self.expense_description.get()
            
            self.expense_manager.add_expense(self.current_user, category, amount, description)
            messagebox.showinfo("Başarılı", "Gider başarıyla eklendi!")
            self.show_main_menu()
        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def show_profile_settings(self):
        self.clear_window()
        user_info = self.db.get_user_info(self.current_user)
        frame = ttk.Frame(self.root, padding=0, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        card = ttk.Frame(frame, padding=30, style="Card.TFrame")
        card.pack()
        ttk.Label(card, text="Profil Ayarları", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Kullanıcı Adı:", style="TLabel").pack(anchor="w", pady=(0, 2))
        ttk.Label(card, text=user_info.get('username', ''), style="TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(card, text="E-posta:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.profile_email = ttk.Entry(card, width=28)
        self.profile_email.insert(0, user_info.get('email', ''))
        self.profile_email.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="Ad Soyad:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.profile_fullname = ttk.Entry(card, width=28)
        self.profile_fullname.insert(0, user_info.get('full_name', ''))
        self.profile_fullname.pack(fill="x", pady=(0, 18))
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Kaydet", command=self.save_profile).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Geri Dön", command=self.show_main_menu).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def save_profile(self):
        email = self.profile_email.get()
        full_name = self.profile_fullname.get()
        if self.db.update_user_info(self.current_user, email, full_name):
            messagebox.showinfo("Başarılı", "Profil bilgileri güncellendi!")
            self.show_main_menu()
        else:
            messagebox.showerror("Hata", "Profil güncellenirken bir hata oluştu!")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.db.verify_user(username, password):
            self.current_user = self.db.get_user_id(username)
            self.show_main_menu()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()
        full_name = self.reg_fullname_entry.get()
        
        if self.db.register_user(username, password, email, full_name):
            messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı!")
            self.show_login()
        else:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanılıyor!")

    def logout(self):
        self.current_user = None
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_add_income(self):
        self.clear_window()
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Kart çerçevesi
        card = ttk.Frame(main_frame, padding=40, style="Card.TFrame")
        card.pack()
        
        # Başlık
        ttk.Label(card, text="Gelir Ekle", style="Header.TLabel").pack(pady=(0, 20))
        
        # Kategori girişi
        ttk.Label(card, text="Kategori:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.income_category = ttk.Combobox(card, values=self.income_manager.get_categories())
        self.income_category.pack(fill="x", pady=(0, 10))
        
        # Tutar girişi
        ttk.Label(card, text="Tutar:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.income_amount = ttk.Entry(card)
        self.income_amount.pack(fill="x", pady=(0, 10))
        
        # Açıklama girişi
        ttk.Label(card, text="Açıklama:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.income_description = ttk.Entry(card)
        self.income_description.pack(fill="x", pady=(0, 18))
        
        # Butonlar
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Kaydet", command=self.save_income, style="TButton").pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Geri Dön", command=self.show_main_menu, style="TButton").pack(side="left", expand=True, fill="x", padx=(5, 0))

    def show_income_report(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Gelir Raporu", font=("Helvetica", 16)).pack(pady=10)
        
        try:
            report = self.income_manager.get_income_summary(self.current_user)
            
            # Kategori bazında gelirler
            for category, amount in report["by_category"].items():
                if amount > 0:
                    ttk.Label(frame, text=f"{category}: {amount:.2f} TL").pack(pady=5)
            
            ttk.Label(frame, text=f"Toplam Gelir: {report['total']:.2f} TL", 
                     font=("Helvetica", 12, "bold")).pack(pady=10)
            
            # Gelir düzenleme ve silme
            income_entries = self.db.get_income_entries(self.current_user)
            for entry in income_entries:
                entry_frame = ttk.Frame(frame, style="Card.TFrame")
                entry_frame.pack(fill="x", pady=5)
                ttk.Label(entry_frame, text=f"{entry['category']}: {entry['amount']:.2f} TL - {entry['description']}", style="TLabel").pack(side="left")
                ttk.Button(entry_frame, text="Düzenle", command=lambda e=entry: self.edit_income(e), style="TButton").pack(side="right", padx=5)
                ttk.Button(entry_frame, text="Sil", command=lambda e=entry: self.delete_income(e), style="TButton").pack(side="right")
            
            ttk.Button(frame, text="Ana Menüye Dön", command=self.show_main_menu).pack(pady=10)
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            self.show_main_menu()

    def edit_income(self, entry):
        # Gelir düzenleme işlemleri
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Gelir Düzenle")
        edit_window.geometry("400x300")  # Pencere boyutunu artırdım
        
        ttk.Label(edit_window, text="Kategori:").pack(pady=5)
        category_entry = ttk.Entry(edit_window)
        category_entry.insert(0, entry['category'])
        category_entry.pack(fill="x", pady=5)
        
        ttk.Label(edit_window, text="Tutar:").pack(pady=5)
        amount_entry = ttk.Entry(edit_window)
        amount_entry.insert(0, entry['amount'])
        amount_entry.pack(fill="x", pady=5)
        
        ttk.Label(edit_window, text="Açıklama:").pack(pady=5)
        description_entry = ttk.Entry(edit_window)
        description_entry.insert(0, entry['description'])
        description_entry.pack(fill="x", pady=5)
        
        def save_changes():
            new_category = category_entry.get()
            new_amount = float(amount_entry.get())
            new_description = description_entry.get()
            self.db.update_income(entry['id'], new_category, new_amount, new_description)
            edit_window.destroy()
            self.show_income_report()
        
        # Kaydet butonu
        ttk.Button(edit_window, text="Kaydet", command=save_changes, style="TButton").pack(pady=10)

    def delete_income(self, entry):
        # Gelir silme işlemleri
        if messagebox.askyesno("Sil", "Bu geliri silmek istediğinizden emin misiniz?"):
            self.db.delete_income(entry['id'])
            self.show_income_report()

    def save_income(self):
        try:
            category = self.income_category.get()
            amount = float(self.income_amount.get())
            description = self.income_description.get()
            
            self.income_manager.add_income(self.current_user, category, amount, description)
            messagebox.showinfo("Başarılı", "Gelir başarıyla eklendi!")
            self.show_main_menu()
        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def edit_expense(self, entry):
        # Gider düzenleme işlemleri
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Gider Düzenle")
        edit_window.geometry("400x300")  # Pencere boyutunu artırdım
        
        ttk.Label(edit_window, text="Kategori:").pack(pady=5)
        category_entry = ttk.Entry(edit_window)
        category_entry.insert(0, entry['category'])
        category_entry.pack(fill="x", pady=5)
        
        ttk.Label(edit_window, text="Tutar:").pack(pady=5)
        amount_entry = ttk.Entry(edit_window)
        amount_entry.insert(0, entry['amount'])
        amount_entry.pack(fill="x", pady=5)
        
        ttk.Label(edit_window, text="Açıklama:").pack(pady=5)
        description_entry = ttk.Entry(edit_window)
        description_entry.insert(0, entry['description'])
        description_entry.pack(fill="x", pady=5)
        
        def save_changes():
            new_category = category_entry.get()
            new_amount = float(amount_entry.get())
            new_description = description_entry.get()
            self.db.update_expense(entry['id'], new_category, new_amount, new_description)
            edit_window.destroy()
            self.show_expense_report()
        
        # Kaydet butonu
        ttk.Button(edit_window, text="Kaydet", command=save_changes, style="TButton").pack(pady=10)

    def delete_expense(self, entry):
        # Gider silme işlemleri
        if messagebox.askyesno("Sil", "Bu gideri silmek istediğinizden emin misiniz?"):
            self.db.delete_expense(entry['id'])
            self.show_expense_report()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop() 