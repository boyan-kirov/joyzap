# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Initial Setup (One-time)

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Edit .env file with your credentials
nano .env
```

Required values:
- `jwt_secret` - Your JWT secret key
- `aws_access_key_id` - AWS access key
- `aws_secret_access_key` - AWS secret key  
- `aws_bucket` - Your S3 bucket name

### 3. Test Locally

**Option A: Simple Python test**
```bash
python test_local.py
```

**Option B: AWS SAM local API**
```bash
# Build first
sam build

# Start local API
sam local start-api --env-vars .env

# Test with curl
curl -X POST http://localhost:3000/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file":"data:image/png;base64,...","file_name":"test"}'
```

### 4. Deploy to AWS

**Using AWS SAM:**
```bash
sam build
sam deploy --guided  # First time only
sam deploy           # Subsequent deploys
```

**Using Serverless Framework:**
```bash
serverless deploy
```

## 📁 Adding Your Other 23 Lambdas

### Quick Template

1. **Create directory:**
   ```bash
   mkdir -p lambdas/my_function
   touch lambdas/my_function/__init__.py
   ```

2. **Copy template:**
   ```bash
   cp lambda_template.py lambdas/my_function/handler.py
   ```

3. **Update handler.py** with your logic

4. **Add to template.yaml:**
   ```yaml
   MyFunction:
     Type: AWS::Serverless::Function
     Properties:
       FunctionName: drishlio-my-function
       CodeUri: .
       Handler: lambdas.my_function.handler.lambda_handler
       Events:
         Api:
           Type: Api
           Properties:
             Path: /my-path
             Method: post
   ```

5. **Add to serverless.yml:**
   ```yaml
   myFunction:
     handler: lambdas/my_function/handler.lambda_handler
     name: ${self:provider.stage}-my-function
     events:
       - http:
           path: my-path
           method: post
           cors: true
   ```

## 🐛 Debugging in VSCode

1. Open any Lambda handler file
2. Set breakpoints (click left of line numbers)
3. Press **F5** to start debugging
4. Select "Debug Current Lambda"

## 📝 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run local test
python test_local.py

# SAM commands
sam build
sam local start-api
sam deploy

# Serverless commands
serverless deploy
serverless deploy function -f fileUpload
serverless logs -f fileUpload

# Check AWS credentials
aws sts get-caller-identity

# List S3 buckets
aws s3 ls
```

## ❓ Troubleshooting

**Import errors:**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**AWS credentials not found:**
- Check .env file has correct values
- Or configure AWS CLI: `aws configure`

**SAM commands not working:**
- Install SAM CLI: `pip install aws-sam-cli`

**Module not found errors:**
- Make sure you have `__init__.py` files in all directories
- Check `sys.path.append()` in handler files

## 📚 Next Steps

1. Add your remaining 23 Lambda functions
2. Create test events in `tests/events/`
3. Add unit tests
4. Set up CI/CD pipeline
5. Configure CloudWatch alarms

## 💡 Tips

- Use `lambda_template.py` as a starting point for new functions
- Keep shared code in `helpers/` directory
- Test locally before deploying
- Use environment variables for configuration
- Enable CloudWatch logs for debugging

## 🔗 Resources

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Serverless Framework](https://www.serverless.com/framework/docs)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
