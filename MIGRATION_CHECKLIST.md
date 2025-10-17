# Lambda Migration Checklist

Track the conversion of your 24 AWS Lambda functions to this project structure.

## Progress Tracker

**Completed: 1 / 24**

## Lambda Functions

### ✅ 1. File Upload
- [x] Created directory structure
- [x] Implemented handler.py
- [x] Added to template.yaml
- [x] Added to serverless.yml
- [x] Created test event
- [x] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

**Location:** `lambdas/file_upload/handler.py`  
**Endpoint:** POST /upload  
**Purpose:** Upload files to S3 (forms and gifts)

---

### ⬜ 2. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

**Location:** `lambdas/[name]/handler.py`  
**Endpoint:** [METHOD] /[path]  
**Purpose:** [Description]

---

### ⬜ 3. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

**Location:** `lambdas/[name]/handler.py`  
**Endpoint:** [METHOD] /[path]  
**Purpose:** [Description]

---

### ⬜ 4. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

**Location:** `lambdas/[name]/handler.py`  
**Endpoint:** [METHOD] /[path]  
**Purpose:** [Description]

---

### ⬜ 5. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 6. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 7. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 8. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 9. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 10. [Lambda Name]
- [ ] Created directory structure
- [ ] Implemented handler.py
- [ ] Added to template.yaml
- [ ] Added to serverless.yml
- [ ] Created test event
- [ ] Tested locally
- [ ] Deployed to AWS
- [ ] Verified in production

---

### ⬜ 11-24. [Remaining Lambdas]

Copy the template above for each remaining Lambda function.

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

- Lambda functions are in `lambdas/[name]/handler.py`
- Shared code is in `helpers/`
- Test events are in `tests/events/`
- Update this file as you migrate each Lambda

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
- Migrate all 24 Lambdas
- Test locally
- Fix issues

### Phase 2: Staging (Week 2)
- Deploy to staging environment
- Integration testing
- Performance testing

### Phase 3: Production (Week 3)
- Deploy to production
- Monitor logs
- Gradual rollout

---

Last Updated: [Date]
