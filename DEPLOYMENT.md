# Render Deployment Guide (Free Tier)

## Prerequisites
- Render.com account
- Git repository pushed to GitHub

## Quick Setup (Free Tier - Dashboard Only)

### Step 1: Connect Repository
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account and select the repository
5. Choose branch: `main` (or your deployment branch)

### Step 2: Configure Web Service
On the deployment form, set:

| Field | Value |
|-------|-------|
| **Name** | `sportexpo` (or your preferred name) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn config.wsgi` |
| **Plan** | Free |

### Step 3: Set Environment Variables
Click "Advanced" and add:

```
SECRET_KEY = your-secret-django-key
DEBUG = False
ALLOWED_HOSTS = sportexpo.onrender.com
```

Get a secure SECRET_KEY from Django:
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### Step 4: Deploy
- Click "Create Web Service"
- Render will automatically build and deploy
- Monitor logs for any errors
- Your app will be available at `https://sportexpo.onrender.com`

## Environment Variables Needed

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | **Required** - Django secret key | Generate with Django shell |
| `DEBUG` | Set to `False` for production | `False` |
| `ALLOWED_HOSTS` | Your Render domain | `sportexpo.onrender.com` |

## Database
- Uses SQLite (included, no setup needed)
- No PostgreSQL required for free tier
- Data persists in the container but resets on redeployment

## Static Files
- WhiteNoise automatically serves static files
- Collected during build process

## Troubleshooting

| Error | Solution |
|-------|----------|
| "500 Internal Server Error" | Check Render logs for SECRET_KEY or DEBUG settings |
| Static files not loading | Run `python manage.py collectstatic --noinput` |
| Migration errors | Check if database exists and is writable |
| Deployment fails | Ensure build.sh is executable and all dependencies install |

## Local Testing with Gunicorn
```bash
gunicorn config.wsgi --bind 0.0.0.0:8000
```

## Redeployment
- Push changes to GitHub
- Render automatically redeploys on push
- Or manually trigger from Render dashboard

