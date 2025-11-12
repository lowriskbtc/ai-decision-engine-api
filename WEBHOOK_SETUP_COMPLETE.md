# ✅ Stripe Webhook Setup - Quick Guide

## Why Webhooks Are Important

Webhooks let Stripe notify your API when:
- ✅ Payment succeeds → Generate API key automatically
- ✅ Subscription updates → Update API key tier
- ✅ Subscription cancels → Downgrade to free tier

**Without webhooks:** You'd have to manually check Stripe for subscription changes.

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Go to Stripe Webhooks

1. In Stripe Dashboard, go to **Developers** → **Webhooks**
2. Click **"+ Add endpoint"**

### Step 2: Configure Webhook

1. **Endpoint URL:** 
   ```
   https://web-production-62146.up.railway.app/webhooks/stripe
   ```

2. **Description:** (optional)
   ```
   AI Decision Engine API - Subscription events
   ```

3. **Events to send:** Click "Select events" and choose:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`

4. Click **"Add endpoint"**

### Step 3: Copy Signing Secret

1. After creating the endpoint, you'll see the **Signing secret**
2. It starts with `whsec_...`
3. **Copy it** - you'll need it next

### Step 4: Add to Railway

1. Go to Railway → Your service → **Variables** tab
2. Click **"+ New Variable"**
3. Add:
   - **Name:** `STRIPE_WEBHOOK_SECRET`
   - **Value:** Your signing secret (`whsec_...`)
4. Click **"Add"**
5. Railway will automatically redeploy

---

## ✅ Verify It's Working

After Railway redeploys (2-3 minutes):

1. **Test webhook in Stripe:**
   - Go to your webhook endpoint in Stripe
   - Click **"Send test webhook"**
   - Select `checkout.session.completed`
   - Click **"Send test webhook"**

2. **Check Railway logs:**
   - Go to Railway → Your service → **Logs** tab
   - You should see: `Subscription activated: sub_...`

3. **Test with real payment:**
   - Go to your pricing page
   - Subscribe with Stripe test card: `4242 4242 4242 4242`
   - Check if API key is generated automatically

---

## 🎯 What Happens With Webhooks

### When Payment Succeeds:
1. Stripe sends `checkout.session.completed` event
2. Your API receives webhook
3. API key is automatically generated
4. Subscription is linked to API key
5. User gets API key on success page

### When Subscription Updates:
1. Stripe sends `customer.subscription.updated` event
2. Your API updates subscription status
3. API key tier stays in sync

### When Subscription Cancels:
1. Stripe sends `customer.subscription.deleted` event
2. Your API downgrades API key to free tier
3. User keeps access but with free limits

---

## 🔒 Security

- ✅ Webhook signature verification is enabled
- ✅ Only Stripe can send valid webhooks
- ✅ Invalid signatures are rejected

---

## 📝 Quick Checklist

- [ ] Webhook endpoint created in Stripe
- [ ] Endpoint URL: `https://web-production-62146.up.railway.app/webhooks/stripe`
- [ ] Events selected: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
- [ ] Signing secret copied
- [ ] `STRIPE_WEBHOOK_SECRET` added to Railway Variables
- [ ] Railway redeployed
- [ ] Test webhook sent successfully

---

**Once webhooks are set up, your payment flow will be fully automated! 🎉**

