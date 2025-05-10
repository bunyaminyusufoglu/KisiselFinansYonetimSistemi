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
        frame = ttk.Frame(self.root, padding=0, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        card = ttk.Frame(frame, padding=30, style="Card.TFrame")
        card.pack()
        ttk.Label(card, text="Kişisel Finans", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(card, text="Yönetim Sistemi", style="Subheader.TLabel").pack(pady=(0, 20))
        ttk.Label(card, text="Kullanıcı Adı:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.username_entry = ttk.Entry(card, width=28)
        self.username_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="Şifre:", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.password_entry = ttk.Entry(card, show="•", width=28)
        self.password_entry.pack(fill="x", pady=(0, 18))
        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="Giriş Yap", command=self.login).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Kayıt Ol", command=self.show_register).pack(side="left", expand=True, fill="x", padx=(5, 0))

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
        frame = ttk.Frame(self.root, padding=0, style="TFrame")
        frame.pack(fill="both", expand=True)
        card = ttk.Frame(frame, padding=30, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(card, text=f"Hoş Geldiniz, {user_info.get('full_name', user_info.get('username', ''))}", style="Header.TLabel").pack(pady=(0, 20))
        ttk.Button(card, text="Gelir Ekle", command=self.show_add_income).pack(fill="x", pady=5)
        ttk.Button(card, text="Gelir Raporu", command=self.show_income_report).pack(fill="x", pady=5)
        ttk.Button(card, text="Gider Ekle", command=self.show_add_expense).pack(fill="x", pady=5)
        ttk.Button(card, text="Gider Raporu", command=self.show_expense_report).pack(fill="x", pady=5)
        ttk.Button(card, text="Profil Ayarları", command=self.show_profile_settings).pack(fill="x", pady=5)
        ttk.Button(card, text="Çıkış Yap", command=self.logout).pack(fill="x", pady=(20, 0))

    def show_add_expense(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="Gider Ekle", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Kategori:").grid(row=1, column=0, pady=5)
        self.expense_category = ttk.Combobox(frame, values=self.expense_manager.get_categories())
        self.expense_category.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Tutar:").grid(row=2, column=0, pady=5)
        self.expense_amount = ttk.Entry(frame)
        self.expense_amount.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Açıklama:").grid(row=3, column=0, pady=5)
        self.expense_description = ttk.Entry(frame)
        self.expense_description.grid(row=3, column=1, pady=5)
        
        ttk.Button(frame, text="Kaydet", command=self.save_expense).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Geri Dön", command=self.show_main_menu).grid(row=5, column=0, columnspan=2)

    def show_expense_report(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="Gider Raporu", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Tarih aralığı seçimi
        ttk.Label(frame, text="Başlangıç Tarihi:").grid(row=1, column=0, pady=5)
        self.start_date = ttk.Entry(frame)
        self.start_date.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Bitiş Tarihi:").grid(row=2, column=0, pady=5)
        self.end_date = ttk.Entry(frame)
        self.end_date.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Raporu Göster", command=self.display_expense_report).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Geri Dön", command=self.show_main_menu).grid(row=4, column=0, columnspan=2)

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

    def display_expense_report(self):
        try:
            start_date = self.start_date.get() or None
            end_date = self.end_date.get() or None
            
            report = self.expense_manager.get_expense_summary(self.current_user, start_date, end_date)
            
            # Rapor penceresi
            report_window = tk.Toplevel(self.root)
            report_window.title("Gider Raporu")
            report_window.geometry("400x500")
            
            frame = ttk.Frame(report_window, padding="20")
            frame.pack(fill="both", expand=True)
            
            ttk.Label(frame, text="Gider Raporu", font=("Helvetica", 16)).pack(pady=10)
            
            # Kategori bazında giderler
            for category, amount in report["by_category"].items():
                if amount > 0:
                    ttk.Label(frame, text=f"{category}: {amount:.2f} TL").pack(pady=5)
            
            ttk.Label(frame, text=f"Toplam Gider: {report['total']:.2f} TL", 
                     font=("Helvetica", 12, "bold")).pack(pady=10)
            
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
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="Gelir Ekle", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Kategori:").grid(row=1, column=0, pady=5)
        self.income_category = ttk.Combobox(frame, values=self.income_manager.get_categories())
        self.income_category.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Tutar:").grid(row=2, column=0, pady=5)
        self.income_amount = ttk.Entry(frame)
        self.income_amount.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Açıklama:").grid(row=3, column=0, pady=5)
        self.income_description = ttk.Entry(frame)
        self.income_description.grid(row=3, column=1, pady=5)
        
        ttk.Button(frame, text="Kaydet", command=self.save_income).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Geri Dön", command=self.show_main_menu).grid(row=5, column=0, columnspan=2)

    def show_income_report(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="Gelir Raporu", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Tarih aralığı seçimi
        ttk.Label(frame, text="Başlangıç Tarihi:").grid(row=1, column=0, pady=5)
        self.income_start_date = ttk.Entry(frame)
        self.income_start_date.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Bitiş Tarihi:").grid(row=2, column=0, pady=5)
        self.income_end_date = ttk.Entry(frame)
        self.income_end_date.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Raporu Göster", command=self.display_income_report).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Geri Dön", command=self.show_main_menu).grid(row=4, column=0, columnspan=2)

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

    def display_income_report(self):
        try:
            start_date = self.income_start_date.get() or None
            end_date = self.income_end_date.get() or None
            
            report = self.income_manager.get_income_summary(self.current_user, start_date, end_date)
            
            # Rapor penceresi
            report_window = tk.Toplevel(self.root)
            report_window.title("Gelir Raporu")
            report_window.geometry("400x500")
            
            frame = ttk.Frame(report_window, padding="20")
            frame.pack(fill="both", expand=True)
            
            ttk.Label(frame, text="Gelir Raporu", font=("Helvetica", 16)).pack(pady=10)
            
            # Kategori bazında gelirler
            for category, amount in report["by_category"].items():
                if amount > 0:
                    ttk.Label(frame, text=f"{category}: {amount:.2f} TL").pack(pady=5)
            
            ttk.Label(frame, text=f"Toplam Gelir: {report['total']:.2f} TL", 
                     font=("Helvetica", 12, "bold")).pack(pady=10)
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop() 