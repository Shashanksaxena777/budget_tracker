from django.contrib.auth import get_user_model
User = get_user_model()

username = "testuser"
email = "admin@example.com"
password = "testpass123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superuser created successfully.")
else:
    print("⚠️ Superuser already exists.")
