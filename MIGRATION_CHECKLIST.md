# Lambda Migration Checklist

Track the conversion of your 24 AWS Lambda functions to this project structure.

## Progress Tracker

**Completed: 24 / 24** 🎉 🚀 ✅ **100% COMPLETE!**

## Lambda Functions

### ✅ 1. File Upload

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [x] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/file_upload/handler.py`  
**Endpoint:** POST /upload  
**Purpose:** Upload files to S3 (forms and gifts)

---

### ✅ 2. WebSocket Disconnect

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/websocket_disconnect/handler.py`  
**Endpoint:** WebSocket $disconnect  
**Purpose:** Clear socket_id from users table when WebSocket disconnects

---

### ✅ 3. My Friends

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/my_friends/handler.py`  
**Endpoint:** GET /friends  
**Purpose:** Get user's friends list with optional keyword search

---

### ✅ 4. Notifications

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/notifications/handler.py`  
**Endpoints:** GET /notifications, PUT /notifications  
**Purpose:** Retrieve and update user notifications

---

### ✅ 5. Stripe Webhook

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/stripe_webhook/handler.py`  
**Endpoint:** POST /stripe/webhook  
**Purpose:** Handle Stripe payment webhook events (checkout, transfers, payouts)

---

### ✅ 6. Gift Management

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/gift_management/handler.py`  
**Endpoints:** GET /gift/categories, POST /gift, PATCH /gift/{id}, PUT /gift  
**Purpose:** CRUD operations for gifts and gift categories

---

### ✅ 7. Dashboard Statistics

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [ ] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/dashboard_statistics/handler.py`  
**Endpoint:** GET /dashboard/statistics  
**Purpose:** Get dashboard statistics and transaction history for a user

---

### ✅ 8. WebSocket Connect

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [ ] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/websocket_connect/handler.py`  
**Endpoint:** WebSocket $connect  
**Purpose:** Store socket_id in users table when WebSocket connects

---

### ✅ 9. Google Auth

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [ ] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/google_auth/handler.py`  
**Endpoint:** POST /auth/google  
**Purpose:** Handle Google OAuth authentication and user registration

---

### ✅ 10. Relation Management

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [ ] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/relation_management/handler.py`  
**Endpoints:** POST /relation, PUT /relation, PATCH /relation, DELETE /relation  
**Purpose:** Manage friend relationships (send, accept, reject, delete requests)

---

### ✅ 11. Calendar Events

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [ ] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/calendar_events/handler.py`  
**Endpoints:** GET /calendar, POST /calendar, GET /calendar/{id}, PUT /calendar, DELETE /calendar/{id}  
**Purpose:** CRUD operations for calendar events

---

### ✅ 12. Parameters

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/parameters/handler.py`  
**Endpoint:** GET /parameters/{type}  
**Purpose:** System parameters and gift category management

---

### ✅ 13. My Followers

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/my_followers/handler.py`  
**Endpoint:** GET /my-followers  
**Purpose:** Get list of followers (pending friend requests)

---

### ✅ 14. WebSocket Message

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/websocket_message/handler.py`  
**Endpoint:** POST /websocket-message  
**Purpose:** Handle WebSocket messages and notifications

---

### ✅ 15. Login

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/login/handler.py`  
**Endpoint:** POST/GET/PUT/PATCH /login  
**Purpose:** Multi-method authentication handler

---

### ✅ 16. Registration

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/registration/handler.py`  
**Endpoint:** POST /registration  
**Purpose:** User registration with validation

---

### ✅ 17. Activity Log

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/activity_log/handler.py`  
**Endpoint:** GET /activity-log  
**Purpose:** User activity logging and retrieval

---

### ✅ 18. Stripe Checkout

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/stripe_checkout/handler.py`  
**Endpoint:** POST /stripe-checkout  
**Purpose:** Extended Stripe webhook v2 (checkout, transfer, payout)

---

### ✅ 19. My Follows

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/my_follows/handler.py`  
**Endpoint:** GET /my-follows  
**Purpose:** Get users that this user follows

---

### ✅ 20. Payment

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/payment/handler.py`  
**Endpoint:** GET/POST /payment  
**Purpose:** Payment operations and history management

---

### ✅ 21. Password Reset

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/password_reset/handler.py`  
**Endpoint:** POST/PUT /password-reset  
**Purpose:** Password reset operations

---

### ✅ 22. Joyzaps

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/joyzaps/handler.py`  
**Endpoint:** POST/GET /joyzaps  
**Purpose:** Complex joyzap operations (presents, cards, time capsules)

---

### ✅ 23. Time Capsule Collector

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/timecapsule_collector/handler.py`  
**Endpoint:** Scheduled task (no HTTP endpoint)  
**Purpose:** Collect expired time capsules

---

### ✅ 24. User Profile

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/user_profile/handler.py`  
**Endpoint:** GET/PUT /user-profile  
**Purpose:** User profile operations with event data

---

### ✅ 25. Reports

-   [x] Created directory structure
-   [x] Implemented handler.py
-   [x] Added to template.yaml
-   [x] Added to serverless.yml
-   [x] Created test event
-   [ ] Tested locally
-   [ ] Deployed to AWS
-   [ ] Verified in production

**Location:** `lambdas/reports/handler.py`  
**Endpoint:** POST/GET /reports  
**Purpose:** Report management (create/get)

---

## Quick Commands for Each Lambda

```bash
# Create new Lambda (replace name, method, path)
./create_lambda.sh lambda_name post /endpoint

# Test locally
python test_local.py

# Deploy single function (Serverless)
serverless deploy function -f lambdaName

# Deploy all
sam deploy
# or
serverless deploy
```

## Notes

-   Lambda functions are in `lambdas/[name]/handler.py`
-   Shared code is in `helpers/`
-   Test events are in `tests/events/`
-   Update this file as you migrate each Lambda

## Migration Tips

1. **One at a time:** Convert and test each Lambda individually
2. **Use the script:** `./create_lambda.sh` saves time
3. **Test locally first:** Catch issues before deploying
4. **Update docs:** Document each Lambda's purpose and endpoint
5. **Keep AWS versions:** Don't delete from AWS until new ones are verified

## Common Patterns

### Pattern 1: Simple CRUD

```python
# GET, POST, PUT, DELETE operations
# Uses JWT auth
# Returns JSON response
```

### Pattern 2: File Operations

```python
# Uploads/downloads from S3
# Processes files
# Returns file URLs
```

### Pattern 3: Data Processing

```python
# Transforms data
# Calls external APIs
# Aggregates information
```

### Pattern 4: Notifications

```python
# Sends emails/SMS
# Triggers other Lambdas
# Updates status
```

## Deployment Strategy

### Phase 1: Development (Week 1)

-   Migrate all 24 Lambdas
-   Test locally
-   Fix issues

### Phase 2: Staging (Week 2)

-   Deploy to staging environment
-   Integration testing
-   Performance testing

### Phase 3: Production (Week 3)

-   Deploy to production
-   Monitor logs
-   Gradual rollout

---

Last Updated: [Date]
