from datetime import datetime
from database import Database
from typing import Dict

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

    def get_expense_summary(self, user_id: int) -> Dict:
        """Get summary of expenses by category."""
        # Get all expense entries from database
        expense_entries = self.db.get_expense_summary(user_id)
        
        # Calculate totals by category
        category_totals = {}
        for category, amount in expense_entries:
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
        """Mevcut gider kategorilerini döndürür"""
        return self.categories

    def add_category(self, category):
        """Yeni bir gider kategorisi ekler"""
        if category in self.categories:
            raise ValueError("Bu kategori zaten mevcut")
        self.categories.append(category)
        return True 