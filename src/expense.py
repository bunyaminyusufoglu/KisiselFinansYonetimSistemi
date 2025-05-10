from datetime import datetime
from database import Database

class ExpenseManager:
    def __init__(self, db):
        self.db = db
        self.categories = [
            "Kira",
            "Faturalar",
            "Market",
            "Ulaşım",
            "Sağlık",
            "Eğitim",
            "Eğlence",
            "Alışveriş",
            "Diğer"
        ]

    def add_expense(self, user_id, category, amount, description=""):
        """Yeni bir gider ekler"""
        if category not in self.categories:
            raise ValueError("Geçersiz kategori")
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Gider tutarı pozitif olmalıdır")
            
            self.db.add_expense(user_id, category, amount, description)
            return True
        except ValueError as e:
            raise ValueError(f"Geçersiz gider bilgisi: {str(e)}")

    def get_expense_summary(self, user_id, start_date=None, end_date=None):
        """Belirli bir tarih aralığındaki giderleri özetler"""
        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            
            expenses = self.db.get_expense_summary(user_id, start_date, end_date)
            
            # Kategori bazında toplam giderleri hesapla
            total_by_category = {category: 0 for category in self.categories}
            for category, amount in expenses:
                total_by_category[category] = amount
            
            # Toplam gideri hesapla
            total_expense = sum(total_by_category.values())
            
            return {
                "by_category": total_by_category,
                "total": total_expense
            }
        except ValueError as e:
            raise ValueError(f"Tarih formatı hatalı: {str(e)}")

    def get_categories(self):
        """Mevcut gider kategorilerini döndürür"""
        return self.categories

    def add_category(self, category):
        """Yeni bir gider kategorisi ekler"""
        if category in self.categories:
            raise ValueError("Bu kategori zaten mevcut")
        self.categories.append(category)
        return True 