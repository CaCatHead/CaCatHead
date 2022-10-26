from django.contrib.auth.models import User


def init_superuser(username='root', password='12345678', email='root@example.com'):
    User.objects.create_superuser(username=username, email=email, password=password)
