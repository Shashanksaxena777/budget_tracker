import os
import google.generativeai as genai
from decouple import config
from datetime import datetime, timedelta
from django.db.models import Sum
import traceback

from apps.budgets.models import Budget
from apps.transactions.models import Transaction


# ===========================
# 🔐 Gemini Configuration
# ===========================

GEMINI_API_KEY = config('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


def get_latest_model():
    """
    Automatically select the most suitable available Gemini model.
    Falls back safely if a model isn't available.
    """
    try:
        models = genai.list_models()
        model_names = [m.name for m in models]

        # Preference order (most powerful to lighter)
        preferred = [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-pro-latest",
            "gemini-flash-latest",
        ]

        for p in preferred:
            if any(p in name for name in model_names):
                print(f"✅ Using Gemini model: {p}")
                return p

        # Fallback
        print("⚠️ Preferred Gemini models not found. Using first available model.")
        return model_names[0] if model_names else "gemini-2.5-flash"

    except Exception as e:
        print("💥 Error fetching Gemini model list:", e)
        return "gemini-2.5-flash"  # safe fallback


# Use the best available model
MODEL_NAME = get_latest_model()
model = genai.GenerativeModel(MODEL_NAME)


# ===========================
# 🤖 Financial Advisor Class
# ===========================

class FinancialAdvisor:
    """AI Financial Advisor using Gemini"""

    @staticmethod
    def get_user_financial_context(user):
        """Fetch user's recent financial context"""

        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        transactions = Transaction.objects.filter(user=user, date__gte=thirty_days_ago)

        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.type == 'expense')

        # Get category breakdown (top 5)
        expense_by_category = (
            transactions.filter(type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:5]
        )

        # Get current month's budget
        current_month = datetime.now().date().replace(day=1)
        try:
            budget = Budget.objects.get(user=user, month=current_month)
            budget_amount = float(budget.budget_amount)
        except Budget.DoesNotExist:
            budget_amount = None

        return {
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'balance': float(total_income - total_expenses),
            'budget': budget_amount,
            'top_expenses': list(expense_by_category),
            'transaction_count': transactions.count(),
        }

    @staticmethod
    def get_advice(user, question):
        """Generate personalized financial advice using Gemini"""

        context = FinancialAdvisor.get_user_financial_context(user)

        # Create prompt
        budget_text = (
            f"₹{context['budget']:,.2f}"
            if context['budget'] is not None
            else "Not set"
        )

        prompt = f"""You are a professional financial advisor. Analyze this financial data and answer the user's question.

        Financial Summary (Last 30 Days):
        - Total Income: ₹{context['total_income']:,.2f}
        - Total Expenses: ₹{context['total_expenses']:,.2f}
        - Current Balance: ₹{context['balance']:,.2f}
        - Monthly Budget: {budget_text}
        - Number of Transactions: {context['transaction_count']}

        Top Expense Categories:
        {chr(10).join([f"- {item['category__name']}: ₹{item['total']:,.2f}" for item in context['top_expenses']])}

        User Question: {question}

        Provide personalized, actionable financial advice based on this data. Be specific, supportive, and practical. Use Indian Rupees (₹) in your response. Keep your response short in 4-5 sentence."""


        try:
            response = model.generate_content(prompt)
            ai_text = (
                response.candidates[0].content.parts[0].text
                if response.candidates and response.candidates[0].content.parts
                else "No response generated."
            )
            return {'success': True, 'advice': ai_text}

        except Exception as e:
            print("Gemini API Error:", e)
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
