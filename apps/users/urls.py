"""
User App URLs
Maps URLs to views (API endpoints).

URL patterns define how to route incoming requests to the right view.
"""

from django.urls import path
from . import views

# app_name creates a namespace for these URLs
# Useful when multiple apps have similar URL names
# Example: 'users:login' vs 'admin:login'
app_name = 'users'



urlpatterns = [
    # Login endpoint
    # URL: /api/auth/login/
    # View: login_view function
    # Name: 'login' (used for reverse URL lookup)
    path('login/', views.login_view, name='login'),
    
    # Logout endpoint
    # URL: /api/auth/logout/
    path('logout/', views.logout_view, name='logout'),
    
    # User profile endpoint
    # URL: /api/auth/profile/
    path('profile/', views.user_profile, name='profile'),
]

"""
How URL routing works:

1. User requests: POST http://localhost:8000/api/auth/login/

2. Django checks main urls.py (config/urls.py)
   - Finds: path('api/auth/', include('apps.users.urls'))
   - Strips 'api/auth/' from URL
   - Passes remaining 'login/' to apps.users.urls

3. Django checks apps/users/urls.py
   - Finds: path('login/', views.login_view)
   - Calls: views.login_view(request)

4. View processes request and returns response

Visual Flow:
/api/auth/login/
    ↓
config/urls.py → strips /api/auth/ → passes to apps.users.urls
    ↓
apps/users/urls.py → strips /login/ → calls views.login_view
    ↓
views.login_view() executes → returns Response
"""