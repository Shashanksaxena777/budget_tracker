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

### 7. Run Development Server

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

## 📁 Project Structure

```
budget-tracker-backend/
├── apps/
│   ├── users/          # Authentication
│   ├── transactions/   # Transaction management
│   ├── categories/     # Category management
│   ├── budgets/        # Budget management
    └── ai/             # AI Advice
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

## 👥 Test Credentials

**For reviewers:**
- Username: `testuser`
- Password: `testpass123`

---

**Built with ❤️ using Django and Django REST Framework**