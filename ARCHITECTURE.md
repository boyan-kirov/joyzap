# Drishlio Lambda Architecture

## 📊 Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│                   /drishlio-lambdas                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ git clone/pull
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Local Development (VSCode)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VSCode Editor                                        │  │
│  │  - Debug Lambdas with breakpoints                    │  │
│  │  - IntelliSense & autocomplete                       │  │
│  │  - Run tasks (build, deploy, test)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌─────────────┬──────────┴──────────┬─────────────────┐  │
│  │             │                      │                  │  │
│  ▼             ▼                      ▼                  ▼  │
│ ┌─────┐  ┌──────────┐  ┌──────────────┐  ┌────────────┐ │
│ │Test │  │SAM Local │  │Python Direct │  │Serverless  │ │
│ │Event│  │   API    │  │    Test      │  │  Invoke    │ │
│ └─────┘  └──────────┘  └──────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ sam deploy / sls deploy
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           API Gateway (REST API)                   │    │
│  │  ┌──────────┬──────────┬──────────┬─────────────┐ │    │
│  │  │ POST     │  GET     │  POST    │    ...      │ │    │
│  │  │ /upload  │ /users   │ /orders  │  (21 more)  │ │    │
│  │  └─────┬────┴────┬─────┴────┬─────┴─────────────┘ │    │
│  └────────┼─────────┼──────────┼───────────────────────┘    │
│           │         │          │                             │
│           ▼         ▼          ▼                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Lambda Functions (24 total)            │   │
│  │                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │ file_upload  │  │ get_user     │  │  ...     │ │   │
│  │  │              │  │              │  │ (22 more)│ │   │
│  │  │ handler.py   │  │ handler.py   │  │          │ │   │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬─────┘ │   │
│  │         │                  │                │       │   │
│  │         └──────────┬───────┴────────────────┘       │   │
│  │                    │                                │   │
│  │                    ▼                                │   │
│  │         ┌─────────────────────┐                    │   │
│  │         │  Shared Helpers     │                    │   │
│  │         │  - JWT Auth         │                    │   │
│  │         │  - Response Format  │                    │   │
│  │         └─────────────────────┘                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AWS Services                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │    S3    │  │ DynamoDB │  │  Other Services  │ │   │
│  │  │ (files)  │  │  (data)  │  │  (SES, SNS, etc) │ │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Development Workflow

```
┌──────────────┐
│ Write Code   │  Edit Lambda handler in VSCode
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Test Local  │  Run test_local.py or SAM local
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Debug     │  Set breakpoints, inspect variables
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Git Commit  │  Commit to version control
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Deploy    │  sam deploy or serverless deploy
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Verify     │  Test deployed endpoint
└──────────────┘
```

## 📦 Lambda Function Structure

```
lambdas/
├── file_upload/              # Lambda 1
│   ├── __init__.py
│   └── handler.py           # Contains lambda_handler()
│
├── user_management/          # Lambda 2
│   ├── __init__.py
│   └── handler.py
│
├── order_processing/         # Lambda 3
│   ├── __init__.py
│   └── handler.py
│
└── ... (21 more lambdas)

Each handler.py:
├── Import shared helpers
├── Define lambda_handler(event, context)
├── JWT authentication
├── Parse request body
├── Business logic
└── Return standardized response
```

## 🔐 Request Flow with JWT

```
Client Request
     │
     │ HTTP Request with Bearer Token
     ▼
┌────────────────┐
│  API Gateway   │
└────────┬───────┘
         │
         │ Event object
         ▼
┌────────────────────┐
│  Lambda Function   │
│                    │
│  1. Extract token  │──┐
│     from headers   │  │
│                    │  │
│  2. JWT Helper     │◄─┘
│     validates      │
│     token          │
│                    │
│  3. Business       │
│     Logic          │
│                    │
│  4. Response       │◄─┐
│     Helper         │  │
│     formats        │──┘
│     output         │
└────────┬───────────┘
         │
         │ Response object
         ▼
┌────────────────┐
│  API Gateway   │
└────────┬───────┘
         │
         │ HTTP Response
         ▼
      Client
```

## 🌐 API Endpoint Structure

```
https://api.drishlio.com/
│
├── /upload                  → file_upload Lambda
│   └── POST                 Upload files to S3
│
├── /users
│   ├── GET /{id}           → get_user Lambda
│   ├── POST                → create_user Lambda
│   ├── PUT /{id}           → update_user Lambda
│   └── DELETE /{id}        → delete_user Lambda
│
├── /orders
│   ├── GET                 → list_orders Lambda
│   ├── GET /{id}          → get_order Lambda
│   ├── POST               → create_order Lambda
│   └── PUT /{id}          → update_order Lambda
│
└── ... (remaining endpoints for other 16 lambdas)
```

## 🗂️ Shared Resources

```
helpers/
│
├── jwt.py                    # JWT Authentication
│   ├── JWT.auth()           # Validate & decode token
│   └── JWT.generate_token() # Create new token
│
├── response.py               # Response Formatting
│   ├── Response.ok()        # 200 success
│   ├── Response.error()     # Error response
│   ├── Response.created()   # 201 created
│   └── Response.no_content()# 204 no content
│
└── [Add your own helpers]
    ├── database.py          # DB connections
    ├── email.py             # Email sending
    └── utils.py             # Utility functions
```

## 🔧 Environment Configuration

```
.env (local)
├── jwt_secret
├── aws_access_key_id
├── aws_secret_access_key
├── aws_bucket
├── aws_form_upload_folder
└── aws_gift_upload_folder

          │
          │ Loaded at runtime
          ▼

Lambda Environment Variables (deployed)
├── Set in template.yaml
├── Set in serverless.yml
└── Or in AWS Console/CLI
```

## 📊 Deployment Options

```
Local Code
    │
    ├─────────────────┬─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌──────────┐  ┌──────────────┐  ┌──────────────┐
│   SAM    │  │  Serverless  │  │  AWS CLI     │
│  Deploy  │  │  Framework   │  │  + Package   │
└────┬─────┘  └──────┬───────┘  └──────┬───────┘
     │               │                  │
     └───────────────┼──────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  CloudFormation│
            │     Stack      │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  Lambda + API  │
            │    Gateway     │
            └────────────────┘
```

## 🧪 Testing Strategies

```
1. Unit Testing
   └── Test individual functions with mock data

2. Local Integration Testing
   ├── test_local.py (direct Python)
   └── SAM local API (full API simulation)

3. Deployed Testing
   ├── Test in Dev environment
   ├── Integration tests
   └── End-to-end tests

4. Production Monitoring
   ├── CloudWatch Logs
   ├── CloudWatch Metrics
   └── X-Ray Tracing (optional)
```

## 🚀 CI/CD Pipeline (Future Enhancement)

```
GitHub Repository
     │
     │ Push/PR
     ▼
┌─────────────────┐
│  GitHub Actions │
│   or            │
│  AWS CodePipeline│
└────────┬────────┘
         │
         ├─── Run Tests
         │
         ├─── Lint Code
         │
         ├─── Build
         │
         └─── Deploy
              │
              ├─── Dev (auto)
              │
              ├─── Staging (auto)
              │
              └─── Production (manual approval)
```

---

This architecture provides:

-   ✅ Modularity (each Lambda is independent)
-   ✅ Reusability (shared helpers)
-   ✅ Testability (local testing)
-   ✅ Scalability (AWS auto-scaling)
-   ✅ Maintainability (organized structure)
-   ✅ Security (JWT auth, environment variables)
