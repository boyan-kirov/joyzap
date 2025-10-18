# Drishlio Lambda Functions

A collection of AWS Lambda functions for the Drishlio project, organized for local development and deployment from VSCode.

## 📁 Project Structure

```
drishlio/
├── lambdas/                    # All Lambda functions
│   ├── file_upload/           # File upload Lambda
│   │   ├── __init__.py
│   │   └── handler.py
│   └── [23 more lambdas...]   # Add your other lambdas here
├── helpers/                    # Shared helper modules
│   ├── __init__.py
│   ├── jwt.py                 # JWT authentication helper
│   └── response.py            # Response formatting helper
├── tests/                      # Unit and integration tests
├── .vscode/                    # VSCode configuration
│   └── launch.json            # Debug configurations
├── .env                        # Local environment variables (DO NOT COMMIT)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── template.yaml              # AWS SAM template
├── serverless.yml             # Serverless Framework config
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

-   Python 3.9 or higher
-   AWS CLI configured with your credentials
-   AWS SAM CLI (for local testing) or Serverless Framework
-   VSCode (recommended)

### Installation

1. **Clone the repository**

    ```bash
    cd /home/parchon/projects/drishlio
    ```

2. **Create a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/Mac
    # or
    venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**

    ```bash
    cp .env.example .env
    # Edit .env with your actual AWS credentials and configuration
    ```

5. **Fill in your .env file**
    - `jwt_secret`: Your JWT secret key
    - `aws_access_key_id`: AWS access key
    - `aws_secret_access_key`: AWS secret key
    - `aws_bucket`: Your S3 bucket name
    - `aws_form_upload_folder`: Folder for form uploads (default: forms)
    - `aws_gift_upload_folder`: Folder for gift uploads (default: gifts)

## 🧪 Local Development

### Testing Locally with AWS SAM

1. **Install AWS SAM CLI** (if not already installed)

    ```bash
    # On Linux
    pip install aws-sam-cli

    # Or using Homebrew on Mac
    brew install aws-sam-cli
    ```

2. **Start local API**

    ```bash
    sam local start-api --env-vars .env
    ```

3. **Test a specific function**
    ```bash
    sam local invoke FileUploadFunction --event tests/events/file_upload_event.json
    ```

### Testing with Python Directly

You can also test Lambda functions directly in Python:

```python
# test_local.py
import os
from dotenv import load_dotenv
from lambdas.file_upload.handler import lambda_handler

load_dotenv()

event = {
    "headers": {
        "Authorization": "Bearer your-test-token"
    },
    "body": {
        "file": "data:image/png;base64,iVBORw0...",
        "file_name": "test_file",
        "is_gift": False
    }
}

result = lambda_handler(event, None)
print(result)
```

## 🐛 Debugging in VSCode

Use the provided debug configurations in `.vscode/launch.json`:

1. Open a Lambda handler file
2. Set breakpoints
3. Press F5 or go to Run → Start Debugging
4. Select "Debug Lambda Function"

## 📦 Deployment

### Option 1: Deploy with AWS SAM

```bash
# Build the application
sam build

# Deploy (first time)
sam deploy --guided

# Deploy (subsequent times)
sam deploy
```

### Option 2: Deploy with Serverless Framework

1. **Install Serverless Framework**

    ```bash
    npm install -g serverless
    npm install --save-dev serverless-python-requirements
    ```

2. **Deploy**

    ```bash
    # Deploy to dev stage
    serverless deploy

    # Deploy to production
    serverless deploy --stage prod
    ```

3. **Deploy a single function**
    ```bash
    serverless deploy function -f fileUpload
    ```

## 📝 Adding New Lambda Functions

To add a new Lambda function:

1. **Create a new directory** under `lambdas/`:

    ```bash
    mkdir -p lambdas/your_function_name
    touch lambdas/your_function_name/__init__.py
    touch lambdas/your_function_name/handler.py
    ```

2. **Implement your handler** in `handler.py`:

    ```python
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

    from helpers.jwt import JWT, AuthorizationError
    from helpers.response import Response

    def lambda_handler(event, context):
        try:
            jwt_helper = JWT(os.environ["jwt_secret"])
            jwt_helper.auth(event)

            # Your logic here

            return Response.ok({"message": "Success"})
        except AuthorizationError as e:
            return Response.error(e.status_code, "", "Unauthorized")
        except Exception as e:
            return Response.error(500, str(e), "Internal Server Error")
    ```

3. **Add to deployment config**:

    In `template.yaml` (AWS SAM):

    ```yaml
    YourFunctionName:
        Type: AWS::Serverless::Function
        Properties:
            FunctionName: drishlio-your-function
            CodeUri: .
            Handler: lambdas.your_function_name.handler.lambda_handler
            Events:
                Api:
                    Type: Api
                    Properties:
                        Path: /your-path
                        Method: post
    ```

    In `serverless.yml`:

    ```yaml
    yourFunction:
        handler: lambdas/your_function_name/handler.lambda_handler
        name: ${self:provider.stage}-your-function
        events:
            - http:
                  path: your-path
                  method: post
                  cors: true
    ```

## 🧰 Helper Modules

### JWT Authentication (`helpers/jwt.py`)

```python
from helpers.jwt import JWT, AuthorizationError

jwt_helper = JWT(os.environ["jwt_secret"])
decoded_token = jwt_helper.auth(event)  # Validates and decodes JWT
```

### Response Helper (`helpers/response.py`)

```python
from helpers.response import Response

# Success response
return Response.ok({"key": "value"})

# Error response
return Response.error(400, "Error details", "Bad Request")

# Created response
return Response.created({"id": 123})

# No content response
return Response.no_content()
```

## 🧪 Testing

Create test events in the `tests/events/` directory:

```json
{
    "headers": {
        "Authorization": "Bearer test-token"
    },
    "body": {
        "key": "value"
    }
}
```

Run tests:

```bash
pytest tests/
```

## 📋 Next Steps

-   [ ] Add your remaining 23 Lambda functions
-   [ ] Set up CI/CD pipeline (GitHub Actions, AWS CodePipeline, etc.)
-   [ ] Add comprehensive unit tests
-   [ ] Configure CloudWatch monitoring and alerts
-   [ ] Set up API Gateway custom domain
-   [ ] Implement request validation
-   [ ] Add API documentation (OpenAPI/Swagger)

## 🔒 Security Notes

-   Never commit `.env` file or AWS credentials
-   Use AWS Secrets Manager or Parameter Store for production secrets
-   Rotate JWT secrets regularly
-   Use IAM roles instead of access keys when possible
-   Enable CloudTrail logging for audit purposes

## 📚 Additional Resources

-   [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
-   [Serverless Framework Documentation](https://www.serverless.com/framework/docs)
-   [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team Here]
