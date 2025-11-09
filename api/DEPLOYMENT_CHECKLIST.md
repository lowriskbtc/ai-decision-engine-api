# Production Deployment Checklist

## Pre-Deployment

### Code Quality
- [x] All tests passing
- [x] Code reviewed
- [x] Error handling implemented
- [x] Input validation added
- [x] Logging configured
- [x] Documentation updated

### Security
- [ ] Environment variables set
- [ ] SECRET_KEY changed from default
- [ ] CORS origins configured
- [ ] API keys secured
- [ ] SSL/TLS configured
- [ ] Rate limiting enabled

### Infrastructure
- [ ] Server provisioned
- [ ] Domain configured
- [ ] DNS records set
- [ ] SSL certificate installed
- [ ] Database configured (if needed)
- [ ] Monitoring set up

### Testing
- [ ] Load testing completed
- [ ] Security testing done
- [ ] Integration tests passing
- [ ] Smoke tests passing

## Deployment Steps

1. **Backup Current State**
   ```bash
   # Create backup
   cp -r api api_backup_$(date +%Y%m%d)
   ```

2. **Set Environment Variables**
   ```bash
   # Copy template
   cp api/.env.example api/.env
   # Edit .env with production values
   ```

3. **Install Dependencies**
   ```bash
   pip install -r api/requirements.txt
   ```

4. **Run Tests**
   ```bash
   python api/test_api.py
   ```

5. **Start Server**
   ```bash
   # Using uvicorn directly
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   
   # Or using systemd/gunicorn
   gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

6. **Verify Deployment**
   ```bash
   curl http://localhost:8000/health
   ```

## Post-Deployment

- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] Logs being collected
- [ ] Performance metrics tracked
- [ ] Documentation updated with production URL
- [ ] Team notified of deployment

## Rollback Plan

If issues occur:
1. Stop new server
2. Restore from backup
3. Investigate logs
4. Fix issues
5. Redeploy

