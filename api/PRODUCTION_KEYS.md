# Production API Keys - Secure Storage

**IMPORTANT: Keep these keys secure! Do not commit to version control.**

## Generated Production Keys

### Free Tier Keys
```
[Generated on: 2025-11-05]
Tier: Free
Limit: 100 requests/month
Keys: (See api_keys.json for full list)
```

### Pro Tier Keys
```
[Generated on: 2025-11-05]
Tier: Pro
Limit: 10,000 requests/month
Keys: (See api_keys.json for full list)
```

### Enterprise Tier Keys
```
[Generated on: 2025-11-05]
Tier: Enterprise
Limit: 1,000,000 requests/month
Keys: (See api_keys.json for full list)
```

## Security Best Practices

1. **Never commit keys to Git**
   - Add `api_keys.json` to `.gitignore`
   - Add `rate_limits.json` to `.gitignore`

2. **Store keys securely**
   - Use environment variables in production
   - Use secret management services (AWS Secrets Manager, etc.)
   - Encrypt keys at rest

3. **Rotate keys regularly**
   - Rotate keys every 90 days
   - Deactivate old keys immediately
   - Notify users before rotation

4. **Monitor key usage**
   - Check `rate_limits.json` regularly
   - Monitor for unusual activity
   - Set up alerts for rate limit violations

## Key Distribution

### For Users
1. User signs up for account
2. System generates API key automatically
3. Key sent via secure email
4. User stores key securely

### For Testing
- Use development keys: `dev_key_123`, `pro_key_456`
- These are safe for local testing
- Never use in production

## Key Management Commands

```bash
# Generate new key
python api/manage_api_keys.py generate pro production

# List all keys
python api/manage_api_keys.py list

# Deactivate key
python api/manage_api_keys.py deactivate <api_key>

# Get key info
python api/manage_api_keys.py info <api_key>
```

## Production Deployment

In production, store keys in:
- Environment variables
- Database (encrypted)
- Secret management service
- NOT in code files

