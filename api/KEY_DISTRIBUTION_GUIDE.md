# API Key Distribution Guide

Guide for securely distributing API keys to users.

## Key Distribution Process

### Step 1: User Registration
1. User signs up for account
2. User selects tier (Free/Pro/Enterprise)
3. System validates payment (if applicable)

### Step 2: Key Generation
```python
from api.api_key_manager import api_key_manager

# Generate key for user
api_key = api_key_manager.generate_api_key(
    tier="pro",
    prefix="user"
)
```

### Step 3: Secure Delivery
- Send via encrypted email
- Display in secure user dashboard
- Never send via unencrypted channels

### Step 4: User Onboarding
- Provide integration guide
- Share example code
- Offer support for setup

## Email Template

```
Subject: Your AI Decision Engine API Key

Hello [User Name],

Your API key has been generated:

API Key: [key]
Tier: [tier]
Limit: [requests/month]

Documentation: https://docs.aiweedcompany.com
Support: support@aiweedcompany.com

Keep this key secure and never share it publicly.

Best regards,
AI Weed Company Team
```

## Dashboard Integration

Create a user dashboard that:
- Shows current API key
- Displays usage statistics
- Allows key regeneration
- Shows rate limit status

## Key Rotation

### Automatic Rotation
- Rotate keys every 90 days
- Notify users 7 days before
- Provide new key via secure channel

### Manual Rotation
- User requests new key
- Old key deactivated immediately
- New key generated and sent

## Security Best Practices

1. **Never log full keys**
   - Only log first 10 characters
   - Use: `key[:10] + "..."`

2. **Monitor usage**
   - Track requests per key
   - Alert on unusual patterns
   - Rate limit enforcement

3. **Key storage**
   - Encrypt at rest
   - Use secure database
   - Regular backups

4. **Access control**
   - Limit who can generate keys
   - Audit key generation
   - Track key usage

## Integration Examples

### Python
```python
import requests

headers = {
    "X-API-Key": "your_production_key_here",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.aiweedcompany.com/decisions/evaluate",
    json={"category": "FINANCIAL", "amount": 1000},
    headers=headers
)
```

### JavaScript
```javascript
fetch('https://api.aiweedcompany.com/decisions/evaluate', {
    method: 'POST',
    headers: {
        'X-API-Key': 'your_production_key_here',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        category: 'FINANCIAL',
        amount: 1000
    })
})
```

## Support

For key-related issues:
- Email: support@aiweedcompany.com
- Documentation: https://docs.aiweedcompany.com
- Status: https://status.aiweedcompany.com

