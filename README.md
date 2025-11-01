# Budget Tracker Backend

Django REST Framework backend for the Personal Budget Tracker application.

## 🚀 Features

- **User Authentication** - Token-based authentication
- **Transaction Management** - CRUD operations for income/expense tracking
- **Category Management** - Dynamic category creation and management
- **Budget Management** - Monthly budget setting and tracking
- **Financial Analytics** - Summary calculations and comparisons
- **API Documentation** - Browsable API interface
- **Filtering & Pagination** - Advanced query capabilities

## 🛠️ Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Token Authentication
- **CORS**: django-cors-headers
- **Filtering**: django-filter

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd budget-tracker-backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy example env file
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOW_ALL_ORIGINS=True
```

**Generate a secure SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: `testuser`
- Email: `test@example.com`
- Password: `testpass123` (or your preferred password)

### 7. Create Sample Data (Optional)

```bash
python manage.py shell
```

Run the following in the Python shell:

```python
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from datetime import date, datetime, timedelta

# Get user
user = User.objects.get(username='testuser')

# Create categories
salary = Category.objects.create(user=user, name='Salary', type='income')
freelance = Category.objects.create(user=user, name='Freelance', type='income')
rent = Category.objects.create(user=user, name='Rent', type='expense')
groceries = Category.objects.create(user=user, name='Groceries', type='expense')
utilities = Category.objects.create(user=user, name='Utilities', type='expense')
entertainment = Category.objects.create(user=user, name='Entertainment', type='expense')

# Create sample transactions
Transaction.objects.create(
    user=user, 
    category=salary, 
    type='income', 
    amount=50000, 
    description='Monthly Salary', 
    date=date.today()
)
Transaction.objects.create(
    user=user, 
    category=freelance, 
    type='income', 
    amount=15000, 
    description='Web Development Project', 
    date=date.today() - timedelta(days=2)
)
Transaction.objects.create(
    user=user, 
    category=rent, 
    type='expense', 
    amount=20000, 
    description='Monthly Rent', 
    date=date.today() - timedelta(days=1)
)
Transaction.objects.create(
    user=user, 
    category=groceries, 
    type='expense', 
    amount=5000, 
    description='Weekly Groceries', 
    date=date.today() - timedelta(days=3)
)
Transaction.objects.create(
    user=user, 
    category=utilities, 
    type='expense', 
    amount=3000, 
    description='Electricity Bill', 
    date=date.today() - timedelta(days=5)
)

# Create budget for current month
current_month = datetime(datetime.now().year, datetime.now().month, 1).date()
Budget.objects.create(user=user, month=current_month, budget_amount=50000)

print("Sample data created successfully!")
exit()
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/` | User login | No |
| POST | `/api/auth/logout/` | User logout | Yes |
| GET | `/api/auth/profile/` | Get user profile | Yes |

### Transactions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/transactions/` | List transactions (paginated) | Yes |
| POST | `/api/transactions/` | Create transaction | Yes |
| GET | `/api/transactions/{id}/` | Get transaction detail | Yes |
| PUT | `/api/transactions/{id}/` | Update transaction | Yes |
| DELETE | `/api/transactions/{id}/` | Delete transaction | Yes |
| GET | `/api/transactions/summary/` | Financial summary | Yes |

**Query Parameters:**
- `page` - Page number
- `page_size` - Items per page (10, 20, 50, 100)
- `type` - Filter by income/expense
- `category` - Filter by category ID
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)
- `min_amount` - Minimum amount
- `max_amount` - Maximum amount
- `search` - Search in description
- `ordering` - Sort field (date, -date, amount, -amount)

### Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List categories | Yes |
| POST | `/api/categories/` | Create category | Yes |
| GET | `/api/categories/{id}/` | Get category detail | Yes |
| PUT | `/api/categories/{id}/` | Update category | Yes |
| DELETE | `/api/categories/{id}/` | Delete category | Yes |

**Query Parameters:**
- `type` - Filter by income/expense

### Budgets

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/budgets/` | List budgets | Yes |
| POST | `/api/budgets/` | Create budget | Yes |
| GET | `/api/budgets/{id}/` | Get budget detail | Yes |
| PUT | `/api/budgets/{id}/` | Update budget | Yes |
| DELETE | `/api/budgets/{id}/` | Delete budget | Yes |
| GET | `/api/budgets/current/` | Get current month budget | Yes |
| GET | `/api/budgets/comparison/` | Budget vs actual comparison | Yes |

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test apps.transactions

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🌐 Deployment

### Option 1: Railway (Recommended)

1. Create account at [Railway.app](https://railway.app)

2. Install Railway CLI:
```bash
npm install -g @railway/cli
```

3. Login and initialize:
```bash
railway login
railway init
```

4. Add PostgreSQL database:
```bash
railway add
# Select PostgreSQL
```

5. Set environment variables:
```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app
```

6. Deploy:
```bash
railway up
```

### Option 2: Render

1. Create account at [Render.com](https://render.com)

2. Create new Web Service

3. Connect GitHub repository

4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`

5. Add environment variables in dashboard

6. Create PostgreSQL database and link

### Option 3: PythonAnywhere

1. Create account at [PythonAnywhere.com](https://www.pythonanywhere.com)

2. Upload code via Git or Files

3. Create virtual environment

4. Configure WSGI file

5. Set up static files

6. Reload web app

## 🔒 Security Considerations

**For Production:**

1. **Set DEBUG=False** in `.env`

2. **Use strong SECRET_KEY**

3. **Configure ALLOWED_HOSTS**:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

4. **Use PostgreSQL** instead of SQLite

5. **Set CORS properly**:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

6. **Use HTTPS** (SSL certificate)

7. **Environment variables** - Never commit `.env` to Git

8. **Database backups** - Regular backups

## 📁 Project Structure

```
budget-tracker-backend/
├── apps/
│   ├── users/          # Authentication
│   ├── transactions/   # Transaction management
│   ├── categories/     # Category management
│   └── budgets/        # Budget management
├── config/             # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is created for educational purposes.

## 👥 Test Credentials

**For reviewers:**
- Username: `testuser`
- Password: `testpass123`

## 🐛 Known Issues

- None currently

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using Django and Django REST Framework**