# 🚀 Quick Deployment Guide

## API Deployment

### Option 1: Quick Test (Local)
```bash
# Start API server
scripts\start_and_test_api.bat

# In another terminal, test endpoints
python api\test_api.py
```

### Option 2: Docker (Recommended)
```bash
cd api
docker-compose up -d
```

### Option 3: Cloud Platforms

#### Heroku
```bash
heroku create ai-decision-engine-api
git push heroku main
```

#### Railway
```bash
railway login
railway init
railway up
```

## Landing Page Deployment

### Netlify (Easiest)
1. Go to netlify.com
2. Drag & drop `saas_landing` folder
3. Done! ✅

### Vercel
```bash
npm i -g vercel
cd saas_landing
vercel
```

## Full Checklist

See `DEPLOYMENT_CHECKLIST.md` for complete deployment guide.

---

**Quick Start**: Run `scripts\start_and_test_api.bat` to test locally first!

