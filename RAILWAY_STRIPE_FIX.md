# Fix Stripe API Key in Railway

## Issue
Railway isn't reading the `STRIPE_SECRET_KEY` environment variable.

## Solution

### Step 1: Verify Variable in Railway

1. Go to Railway dashboard
2. Click your service (the one deployed)
3. Go to **Variables** tab
4. Look for `STRIPE_SECRET_KEY`
5. **Verify:**
   - Name is exactly: `STRIPE_SECRET_KEY` (case-sensitive)
   - Value starts with: `sk_test_...`
   - No extra spaces before/after

### Step 2: Trigger Redeploy

After adding/changing environment variables, Railway needs to redeploy:

**Option A: Automatic (usually happens)**
- Railway should auto-redeploy when you add variables
- Wait 2-3 minutes

**Option B: Manual Redeploy**
1. In Railway, go to your service
2. Click **Deployments** tab
3. Click **"Redeploy"** or **"Deploy"** button
4. Wait for deployment to complete

### Step 3: Verify It's Working

After redeploy, check:
```
https://web-production-62146.up.railway.app/debug/stripe-config
```

Should show:
```json
{
  "stripe_installed": true,
  "stripe_key_set": true,
  "stripe_key_length": 51,
  "stripe_key_prefix": "sk_test"
}
```

### Step 4: Test Payment

Once the debug endpoint shows the key is set:
1. Go to pricing page
2. Click "Subscribe Now"
3. Should redirect to Stripe checkout

---

## Common Issues

### Variable Not Found
- **Check:** Variable name is exactly `STRIPE_SECRET_KEY` (no typos)
- **Check:** Variable is in the correct service (not project-level)
- **Fix:** Delete and re-add the variable

### Still Not Working After Redeploy
- **Check:** Railway logs for errors
- **Check:** Debug endpoint shows key is set
- **Try:** Restart the service manually

---

## Quick Checklist

- [ ] `STRIPE_SECRET_KEY` added to Railway Variables
- [ ] Value is your test key: `sk_test_...`
- [ ] Railway redeployed (check Deployments tab)
- [ ] Debug endpoint shows key is set
- [ ] Try subscribing again

---

**After fixing, wait 2-3 minutes for Railway to redeploy, then test again!**

