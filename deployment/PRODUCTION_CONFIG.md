# Production Configuration Guide

## Environment Variables

Create a `.env` file with the following:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=production

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
LOG_LEVEL=INFO

# Features
ENABLE_ANALYTICS=true
ENABLE_WEBHOOKS=true
ENABLE_CACHING=true
```

## Security Checklist

- [ ] Change all default secrets
- [ ] Use strong API keys
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Configure backups

## Production Settings

1. **Disable Debug Mode**
   - Set `DEBUG=false` in environment

2. **Enable CORS**
   - Configure allowed origins
   - Restrict to your domains

3. **Set Up Monitoring**
   - Configure Sentry or similar
   - Set up uptime monitoring
   - Configure alerting

4. **Database Setup** (if needed)
   - Configure production database
   - Set up backups
   - Configure connection pooling

## Deployment Platforms

### Railway
```bash
railway up
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t ai-decision-engine .
docker run -p 8000:8000 ai-decision-engine
```

### Render
- Connect GitHub repository
- Configure build settings
- Set environment variables
- Deploy

## Post-Deployment

1. Verify health endpoint
2. Test all endpoints
3. Check monitoring
4. Review logs
5. Test from external network
