from django.contrib.auth import get_user_model

User = get_user_model()

username = "testuser"
email = "admin@example.com"
password = "testpass123"
first_name = "Shashank"
last_name = "Saxena"

# Check if user already exists
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
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    print("⚠️ Superuser already existed — updated first and last name.")
