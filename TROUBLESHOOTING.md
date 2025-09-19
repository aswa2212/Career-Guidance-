# Troubleshooting Guide

## Step-by-Step Manual Setup

### 1. Start PostgreSQL Database

**Option A: Using Services**
1. Press `Win + R`, type `services.msc`, press Enter
2. Find "postgresql-x64-16" (or similar version)
3. Right-click → Start

**Option B: Using Command Line**
```powershell
# Try these commands one by one until one works:
net start postgresql-x64-16
net start postgresql-x64-15
net start postgresql-x64-14
net start postgresql-x64-13
```

**Option C: Check if PostgreSQL is installed**
```powershell
Get-Service -Name "*postgresql*"
```

### 2. Add Interests Column to Database

```powershell
cd "c:\Users\aswaj\OneDrive\Desktop\Project\SIH 2025\career-tracking-backend"
python add_interests_column.py
```

**If this fails:**
- Check if PostgreSQL is running
- Verify database credentials in `.env` file
- Make sure `career_db` database exists

### 3. Start Backend Server

```powershell
cd "c:\Users\aswaj\OneDrive\Desktop\Project\SIH 2025"
.\start-backend.bat
```

**Alternative method:**
```powershell
cd career-tracking-backend
python -m uvicorn app.main:app --reload
```

### 4. Start Frontend (in new terminal)

```powershell
cd "c:\Users\aswaj\OneDrive\Desktop\Project\SIH 2025"
.\start-frontend.bat
```

**Alternative method:**
```powershell
cd Frontend
npm run dev
```

## Common Issues and Solutions

### Database Connection Error
```
Error: could not connect to server: Connection refused
```

**Solutions:**
1. Start PostgreSQL service (see step 1 above)
2. Check if port 5432 is available: `netstat -an | findstr 5432`
3. Verify database exists: Connect to PostgreSQL and check if `career_db` exists

### Backend Server Error
```
Error: [WinError 10061] No connection could be made
```

**Solutions:**
1. Make sure backend is running on port 8000
2. Check if port 8000 is available: `netstat -an | findstr 8000`
3. Try starting backend manually: `python -m uvicorn app.main:app --reload`

### Frontend Build Error
```
Module not found or npm errors
```

**Solutions:**
1. Install dependencies: `cd Frontend && npm install`
2. Clear cache: `npm cache clean --force`
3. Delete node_modules and reinstall: `rm -rf node_modules && npm install`

## Quick Commands Summary

```powershell
# 1. Start PostgreSQL (try one of these)
net start postgresql-x64-16

# 2. Navigate to project
cd "c:\Users\aswaj\OneDrive\Desktop\Project\SIH 2025"

# 3. Run quick setup
.\quick_setup.bat

# 4. Start frontend (in new terminal)
.\start-frontend.bat
```

## Verification Steps

After setup, verify everything is working:

1. **Database**: `python test_new_features.py` should show Database Schema: ✅ PASS
2. **Backend**: Visit http://localhost:8000 - should show API welcome message
3. **Frontend**: Visit http://localhost:3000 - should show the application
4. **New Features**: 
   - Go to Settings → See "My Interests" section
   - Go to Dashboard → See "Recommended for You" section with AI suggestions

## Still Having Issues?

1. Check Windows Event Viewer for PostgreSQL errors
2. Look at backend console for detailed error messages
3. Check browser console for frontend errors
4. Ensure all required ports (3000, 8000, 5432) are not blocked by firewall
