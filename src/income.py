from datetime import datetime
from database import Database
from typing import Dict

class IncomeManager:
    def __init__(self, db):
        self.db = db
        self.categories = [
            "Maaş",
            "Freelance",
            "Yatırım",
            "Kira Geliri",
            "Diğer"
        ]

    def add_income(self, user_id, category, amount, description=""):
        """Yeni bir gelir ekler"""
        if category not in self.categories:
            raise ValueError("Geçersiz kategori")
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Gelir tutarı pozitif olmalıdır")
            
            self.db.add_income(user_id, category, amount, description)
            return True
        except ValueError as e:
            raise ValueError(f"Geçersiz gelir bilgisi: {str(e)}")

    def get_income_summary(self, user_id: int) -> Dict:
        """Get summary of income by category."""
        # Get all income entries from database
        income_entries = self.db.get_income_summary(user_id)
        
        # Calculate totals by category
        category_totals = {}
        for category, amount in income_entries:
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        # Calculate total
        total = sum(category_totals.values())
        
        return {
            'by_category': category_totals,
            'total': total
        }

    def get_categories(self):
        """Mevcut gelir kategorilerini döndürür"""
        return self.categories

    def add_category(self, category):
        """Yeni bir gelir kategorisi ekler"""
        if category in self.categories:
            raise ValueError("Bu kategori zaten mevcut")
        self.categories.append(category)
        return True 