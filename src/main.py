from user import UserManager
from income import IncomeManager

def main_menu():
    print("\n=== Kişisel Finans Yönetim Sistemi ===")
    print("1. Kayıt Ol")
    print("2. Giriş Yap")
    print("3. Çıkış")
    return input("Seçiminiz: ")

def user_menu(user_id):
    print("\n=== Kullanıcı Menüsü ===")
    print("1. Gelir Ekle")
    print("2. Gelir Raporu")
    print("3. Çıkış Yap")
    return input("Seçiminiz: ")

def main():
    user_manager = UserManager()
    income_manager = IncomeManager(user_manager.db)
    current_user_id = None

    while True:
        if current_user_id is None:
            choice = main_menu()
            
            if choice == "1":
                username = input("Kullanıcı adı: ")
                password = input("Şifre: ")
                success, message = user_manager.register_user(username, password)
                print(message)
            
            elif choice == "2":
                username = input("Kullanıcı adı: ")
                password = input("Şifre: ")
                success, result = user_manager.login_user(username, password)
                if success:
                    current_user_id = result
                    print("Giriş başarılı!")
                else:
                    print(result)
            
            elif choice == "3":
                print("Program sonlandırılıyor...")
                break
            
            else:
                print("Geçersiz seçim!")
        
        else:
            choice = user_menu(current_user_id)
            
            if choice == "1":
                print("\nGelir Kategorileri:")
                for i, category in enumerate(income_manager.get_income_categories(), 1):
                    print(f"{i}. {category}")
                
                category = input("\nKategori seçin (1-5): ")
                try:
                    category = income_manager.get_income_categories()[int(category)-1]
                except (ValueError, IndexError):
                    print("Geçersiz kategori seçimi!")
                    continue
                
                amount = input("Miktar: ")
                description = input("Açıklama (opsiyonel): ")
                
                success, message = income_manager.add_income(current_user_id, category, amount, description)
                print(message)
            
            elif choice == "2":
                summary = income_manager.get_income_summary(current_user_id)
                if summary:
                    print("\nGelir Raporu:")
                    print("-" * 30)
                    for category, amount in summary:
                        print(f"{category}: {amount:.2f} TL")
                    print("-" * 30)
                    print(f"Toplam: {income_manager.get_total_income(current_user_id):.2f} TL")
                else:
                    print("Henüz gelir kaydı bulunmuyor.")
            
            elif choice == "3":
                current_user_id = None
                print("Çıkış yapıldı.")
            
            else:
                print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
