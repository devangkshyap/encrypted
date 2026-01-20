# Deployment Guide

## Current Architecture
This application consists of:
- **Frontend**: Static HTML/CSS/JS in the `frontend/` folder
- **Backend**: Flask API server in `backend/app.py`

## Deployment Options

### Option 1: Separate Frontend + Backend (Recommended)

#### Backend Deployment (Choose one):

**A. Deploy to Render:**
1. Go to https://render.com and sign up
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python backend/app.py`
   - Environment: Python 3
5. Copy the deployed backend URL (e.g., `https://your-app.onrender.com`)

**B. Deploy to Railway:**
1. Go to https://railway.app
2. Create a new project from your GitHub repo
3. Railway will auto-detect Python and deploy
4. Copy the deployed backend URL

#### Frontend Deployment (Netlify):
1. Update API URLs in `frontend/clean_encryption_app.html`:
   - Replace all `http://localhost:5000` with your backend URL
2. Deploy to Netlify:
   - Drag and drop the `frontend` folder to Netlify
   - Or connect your GitHub repo and set:
     - Publish directory: `frontend`
     - Build command: (leave empty)

### Option 2: Local Development Only
If you want to keep this as a local application:
1. Run the backend: `python backend/app.py`
2. Open `frontend/clean_encryption_app.html` in your browser
3. The app will connect to `http://localhost:5000`

## Environment Variables
Make sure to set these on your backend hosting platform:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`

## CORS Configuration
The backend is already configured to allow CORS from any origin using Flask-CORS.
For production, update the CORS settings in `backend/app.py` to only allow your frontend domain.
