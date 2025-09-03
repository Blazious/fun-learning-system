# 🗄️ Database Setup Guide

## 🎯 **SQLite Setup (Recommended for Development)**

Great news! We've switched to SQLite, which is much easier to set up and doesn't require any external database installation.

## 🚀 **Quick Setup (3 Steps)**

### **Step 1: Navigate to Backend Directory**
```bash
cd backend
```

### **Step 2: Run the Setup Script**
```bash
python setup_sqlite.py
```

This script will:
- ✅ Create the SQLite database file automatically
- ✅ Run all Django migrations
- ✅ Optionally create a superuser account

### **Step 3: Start the Development Server**
```bash
python manage.py runserver
```

## 🌐 **Access Your Platform**

- **Admin Panel**: http://localhost:8000/admin/
- **API Endpoints**: http://localhost:8000/api/

## 🔧 **Manual Setup (Alternative)**

If you prefer to run commands manually:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## 📁 **What Gets Created**

- **Database file**: `backend/db.sqlite3` (created automatically)
- **Admin user**: Created during setup (if you choose to)

## ✅ **Benefits of SQLite**

- 🚀 **No installation required** - comes with Python
- 🔧 **Zero configuration** - works out of the box
- 📱 **Portable** - database file can be moved/copied
- 🧪 **Perfect for development** - fast and reliable
- 💾 **Single file** - easy to backup and version control

## 🔄 **Switching Back to PostgreSQL Later**

If you want to use PostgreSQL in production, you can easily switch back by:
1. Updating the `DATABASES` setting in `settings.py`
2. Installing `psycopg2-binary`
3. Running migrations on the new database

## 🐛 **Troubleshooting**

### Issue: "No module named 'django'"
**Solution**: Activate your virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: "Permission denied"
**Solution**: Make sure you have write permissions in the backend directory

### Issue: "Database is locked"
**Solution**: Make sure no other process is using the database file

## 🎉 **You're All Set!**

SQLite is perfect for development and will work immediately without any complex setup. Your Django project is now ready to run!
