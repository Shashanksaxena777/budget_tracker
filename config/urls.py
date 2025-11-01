"""
Main URL Configuration
This is the entry point for all URLs in the project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Panel
    # URL: /admin/
    # Provides web interface to manage database
    path('admin/', admin.site.urls),
    
    # Authentication APIs
    # URL: /api/auth/...
    # includes all URLs from apps.users.urls
    # Example: /api/auth/login/, /api/auth/logout/, etc.
    path('api/auth/', include('apps.users.urls')),
    
    # We'll add more API endpoints later:
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/budgets/', include('apps.budgets.urls')),
]

"""
URL Structure Explanation:

include() function:
- Includes all URL patterns from another urls.py file
- Keeps URLs organized by app
- Makes URLs modular and reusable

Example with include():
Main urls.py:           App urls.py:           Final URL:
path('api/auth/',   +   path('login/')    =   /api/auth/login/
  include(...))         path('logout/')   =   /api/auth/logout/

Why this structure?
1. Organization: All auth URLs are in users app
2. Scalability: Easy to add new apps
3. Namespace: Prevents URL conflicts
4. Clean: Main urls.py stays small and readable

REST API Convention:
/api/         → API namespace
  /auth/      → Authentication resources
    /login/   → Specific action
  /transactions/  → Transaction resources
  /budgets/       → Budget resources
"""