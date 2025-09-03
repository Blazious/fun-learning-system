# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

## ⚡ Quick Start (5 minutes)

### 1. Clone & Setup
```bash
git clone <repository-url>
cd learning-systen/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create PostgreSQL database
createdb funlearning_db

# Copy environment file
cp env.example .env
# Edit .env with your database credentials
```

### 3. Initialize Database
```bash
# Run the setup script (creates sample data)
python setup_db.py
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Platform
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **Login**: admin@funlearning.com / admin123

## 🔧 Manual Setup (if needed)

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Load Sample Data
```bash
python setup_db.py
```

## 📱 Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@funlearning.com | admin123 | Superuser |
| demo@funlearning.com | demo123 | Sample User |

## 🐛 Troubleshooting

### Database Connection Issues
- Check PostgreSQL is running
- Verify database credentials in `.env`
- Ensure database `funlearning_db` exists

### Import Errors
- Make sure you're in the `backend/` directory
- Activate virtual environment
- Check all dependencies are installed

### Migration Issues
- Delete `migrations/` folders (except `__init__.py`)
- Run `python manage.py makemigrations` again
- Check for model import errors

## 📚 Next Steps

1. **Explore the Admin Panel** - See all models and data
2. **Check API Endpoints** - Test the REST API
3. **Review Models** - Understand the data structure
4. **Start Building** - Add your features!

## 🆘 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review the models in each app's `models.py`
- Check Django logs in the console output
- Create an issue in the repository

---

**Happy Coding! 🎉**
