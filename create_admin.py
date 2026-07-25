#!/usr/bin/env python
"""
Create superuser during deployment if it doesn't exist
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

username = 'nazi'
password = 'nazrawi19'
email = 'admin@sportexpo.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✓ Superuser "{username}" created successfully')
else:
    print(f'ℹ Superuser "{username}" already exists')
