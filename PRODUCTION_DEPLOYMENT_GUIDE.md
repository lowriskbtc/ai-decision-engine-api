# Production Deployment Guide

Complete guide for deploying AI Weed Company services to production.

## Overview

This guide covers deployment of:
1. **API Service** - FastAPI backend
2. **Landing Page** - SaaS landing page
3. **Waitlist Backend** - Email collection service

## Prerequisites

### Required Accounts
- [ ] Deployment platform account (Heroku/Railway/Render)
- [ ] Domain provider account
- [ ] DNS management access
- [ ] SSL certificate provider

### Required Tools
- [ ] Git installed
- [ ] Python 3.11+ installed
- [ ] Deployment platform CLI (optional)

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Advantages:**
- Simple deployment
- Automatic HTTPS
- Built-in database options
- Free tier available

**Steps:**
1. Go to railway.app
2. Create new project
3. Connect GitHub repository
4. Add environment variables from `.env.example`
5. Deploy!

### Option 2: Render

**Steps:**
1. Go to render.com
2. Create new Web Service
3. Connect repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy

### Option 3: Heroku

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create aiweed-api`
4. Set config vars from `.env.example`
5. Deploy: `git push heroku main`

### Option 4: Docker Deployment

**Steps:**
1. Build image: `docker build -t aiweed-api ./api`
2. Run container: `docker run -p 8000:8000 aiweed-api`
3. Or use docker-compose: `docker-compose up -d`

## Environment Variables

Copy from `api/.env.example` and set:

**Required:**
- `API_HOST` - Server host (usually 0.0.0.0)
- `API_PORT` - Server port (usually from platform)
- `SECRET_KEY` - Change from default!

**Recommended:**
- `ALLOWED_ORIGINS` - Your domain(s)
- `DATABASE_URL` - If using database
- `LOG_LEVEL` - INFO or DEBUG

## Landing Page Deployment

### Netlify (Easiest)

1. Go to netlify.com
2. Drag & drop `saas_landing/` folder
3. Or connect GitHub repo
4. Done! (HTTPS automatic)

### Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `cd saas_landing && vercel`
3. Follow prompts

### GitHub Pages

1. Push to GitHub
2. Go to repo Settings > Pages
3. Select branch and folder
4. Enable Pages

## Post-Deployment

### Verification Checklist

- [ ] API health endpoint responds: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Landing page loads
- [ ] Waitlist form works
- [ ] HTTPS enabled
- [ ] Domain configured
- [ ] SSL certificate active

### Monitoring Setup

1. Set up uptime monitoring (UptimeRobot, Pingdom)
2. Configure error tracking (Sentry, Rollbar)
3. Set up analytics (Google Analytics)
4. Enable logging (platform logs or external service)

### Health Checks

**API Health:**
```bash
curl https://your-api-domain.com/health
```

**Waitlist Health:**
```bash
curl https://your-waitlist-domain.com/health
```

## Troubleshooting

### API Not Starting
- Check environment variables
- Verify Python version (3.11+)
- Check logs for errors
- Verify port configuration

### CORS Errors
- Check `ALLOWED_ORIGINS` setting
- Verify domain matches exactly
- Check for trailing slashes

### Database Issues
- Verify `DATABASE_URL` format
- Check database connection
- Verify credentials

## Scaling Considerations

### API Scaling
- Use multiple workers: `gunicorn api.main:app -w 4`
- Set up load balancer
- Use Redis for caching
- Enable CDN for static assets

### Database Scaling
- Use connection pooling
- Set up read replicas
- Monitor query performance
- Use indexing appropriately

## Security Checklist

- [ ] SECRET_KEY changed
- [ ] API keys secured
- [ ] HTTPS enabled
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Input validation active
- [ ] Error messages don't leak info
- [ ] Logs don't contain secrets

## Rollback Plan

If deployment fails:

1. **Keep Previous Version Running**
   - Don't delete old deployment immediately
   - Keep backup ready

2. **Quick Rollback**
   ```bash
   # On platform, redeploy previous version
   # Or restore from backup
   ```

3. **Investigate**
   - Check logs
   - Review recent changes
   - Test locally first

## Support

For deployment issues:
- Check platform documentation
- Review API logs
- Test locally first
- Check environment variables

## Next Steps After Deployment

1. Test all endpoints
2. Set up monitoring
3. Configure backups
4. Set up alerts
5. Update documentation with production URLs
6. Announce launch!

