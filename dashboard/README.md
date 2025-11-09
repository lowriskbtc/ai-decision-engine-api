# User Dashboard - API Key Management

Complete user dashboard for managing API keys, viewing usage statistics, and monitoring API activity.

## Features

✅ **Key Management**
- View all API keys
- Generate new keys
- Deactivate keys
- View key information

✅ **Usage Statistics**
- Total requests
- Success rate
- Response times
- Top endpoints
- Daily breakdown

✅ **Visual Dashboard**
- Modern, responsive design
- Real-time statistics
- Usage bars
- Tier badges

## Files

- `dashboard/index.html` - Main dashboard interface
- `api/key_management_routes.py` - Backend API endpoints

## API Endpoints

### List Keys
```
GET /api/keys/list
Headers: X-API-Key: <admin_key>
```

### Generate Key
```
POST /api/keys/generate
Headers: X-API-Key: <admin_key>
Body: { "tier": "pro", "prefix": "key" }
```

### Deactivate Key
```
POST /api/keys/deactivate
Headers: X-API-Key: <admin_key>
Body: { "key": "<api_key>" }
```

### Get Key Info
```
GET /api/keys/info/<key>
Headers: X-API-Key: <admin_key>
```

### Get Key Usage
```
GET /api/keys/usage/<key>
Headers: X-API-Key: <admin_key>
```

## Access

The dashboard requires an admin API key (Dev, Pro, or Enterprise tier).

## Usage

1. Open `dashboard/index.html` in a browser
2. Dashboard will attempt to connect to API
3. If API is not available, shows demo data
4. All operations require valid admin API key

## Deployment

For production:
1. Serve dashboard from web server
2. Configure API_BASE URL
3. Set up authentication
4. Connect to production API

