"""
Main URL Configuration
This is the entry point for all URLs in the project.
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

def api_root(request):
    """Root API endpoint"""
    return JsonResponse({
        'message': 'Budget Tracker API',
        'status': 'active',
        'endpoints': {
            'auth': '/api/auth/',
            'transactions': '/api/transactions/',
            'categories': '/api/categories/',
            'budgets': '/api/budgets/',
            'admin': '/admin/',
        }
    })



urlpatterns = [
    path('', api_root, name='api-root'),  # Add this
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/budgets/', include('apps.budgets.urls')),
    path('api/ai/', include('apps.ai.urls')),
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