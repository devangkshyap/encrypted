# Render Deployment Instructions

## Quick Deploy to Render (Free)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: your-encryption-app
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python backend/app.py`
   - Click "Create Web Service"

3. **Done!** Render will give you a URL like: `https://your-encryption-app.onrender.com`

## Configuration

The app automatically detects its environment:
- **Local**: Uses `http://localhost:5000` for API calls
- **Production**: Uses the same domain for API calls

No manual configuration needed!

## Environment Variables (Optional)

For production security, add these in Render dashboard:
- `FLASK_ENV=production`
- `SECRET_KEY=your-random-secret-key-here`

## Free Tier Notes

- Render free tier spins down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds
- Upgrade to paid plan for always-on service

## Local Development

```bash
python backend/app.py
```
Then open: http://localhost:5000/

## Troubleshooting

If deployment fails, check Render logs for errors.
Common issues:
- Missing dependencies in requirements.txt
- Python version mismatch (using 3.13.9)
