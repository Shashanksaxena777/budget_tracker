from django.contrib.auth import get_user_model

User = get_user_model()

# Define admin user details
username = "testuser"
email = "admin@example.com"
password = "testpass123"
first_name = "Shashank"
last_name = "Saxena"

# Create superuser if not already exists
if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    print("✅ Superuser created successfully with full name.")
else:
    print("⚠️ Superuser already exists.")
