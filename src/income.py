from database import Database
from datetime import datetime

class IncomeManager:
    def __init__(self, db):
        self.db = db
        self.categories = [
            "Maaş",
            "Yatırım",
            "Serbest Meslek",
            "Kira Geliri",
            "Diğer"
        ]

    def add_income(self, user_id, category, amount, description=""):
        if category not in self.categories:
            return False, "Geçersiz kategori"
        
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Miktar pozitif olmalıdır"
            
            self.db.add_income(user_id, category, amount, description)
            return True, "Gelir başarıyla eklendi"
        except ValueError:
            return False, "Geçersiz miktar"

    def get_income_categories(self):
        return self.categories

    def get_income_summary(self, user_id, start_date=None, end_date=None):
        return self.db.get_income_summary(user_id, start_date, end_date)

    def get_total_income(self, user_id, start_date=None, end_date=None):
        summary = self.get_income_summary(user_id, start_date, end_date)
        return sum(amount for _, amount in summary) 