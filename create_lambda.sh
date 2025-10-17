#!/bin/bash

# Script to create a new Lambda function from template
# Usage: ./create_lambda.sh <function_name> <http_method> <path>

set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./create_lambda.sh <function_name> [http_method] [path]"
    echo "Example: ./create_lambda.sh user_management post /users"
    exit 1
fi

FUNCTION_NAME=$1
HTTP_METHOD=${2:-post}
API_PATH=${3:-/$FUNCTION_NAME}

# Convert function_name to CamelCase for CloudFormation
CAMEL_CASE=$(echo $FUNCTION_NAME | sed -r 's/(^|_)([a-z])/\U\2/g')
FUNCTION_CLASS="${CAMEL_CASE}Function"

echo "🚀 Creating new Lambda function: $FUNCTION_NAME"

# Create directory structure
LAMBDA_DIR="lambdas/$FUNCTION_NAME"
if [ -d "$LAMBDA_DIR" ]; then
    echo "❌ Lambda function '$FUNCTION_NAME' already exists!"
    exit 1
fi

mkdir -p "$LAMBDA_DIR"

# Create __init__.py
cat > "$LAMBDA_DIR/__init__.py" << EOF
# $CAMEL_CASE Lambda module
EOF

# Create handler.py from template
cat > "$LAMBDA_DIR/handler.py" << 'EOF'
"""
Lambda handler for FUNCTION_NAME
"""
import os
import sys
import json

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response


def lambda_handler(event, context):
    """
    Lambda handler function for FUNCTION_NAME.
    
    Args:
        event: Lambda event object containing request data
        context: Lambda context object
        
    Returns:
        Response object with statusCode, headers, and body
    """
    try:
        # Authenticate request
        jwt_helper = JWT(os.environ["jwt_secret"])
        decoded_token = jwt_helper.auth(event)
        
        # Parse request body
        body_data = {}
        if isinstance(event.get("body"), dict):
            body_data = event["body"]
        elif isinstance(event.get("body"), str):
            body_data = json.loads(event["body"])
        
        # TODO: Implement your Lambda logic here
        result = {
            "message": "FUNCTION_NAME executed successfully",
            "user_id": decoded_token.get("user_id"),
            "data": body_data
        }
        
        return Response.ok(result)
        
    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
    except json.JSONDecodeError as e:
        return Response.error(400, str(e), "Invalid JSON in request body")
    except KeyError as e:
        return Response.error(400, str(e), f"Missing required field: {str(e)}")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
EOF

# Replace FUNCTION_NAME placeholder
sed -i "s/FUNCTION_NAME/$FUNCTION_NAME/g" "$LAMBDA_DIR/handler.py"

# Create test event
TEST_EVENT_DIR="tests/events"
mkdir -p "$TEST_EVENT_DIR"

cat > "$TEST_EVENT_DIR/${FUNCTION_NAME}_event.json" << EOF
{
    "resource": "$API_PATH",
    "path": "$API_PATH",
    "httpMethod": "$(echo $HTTP_METHOD | tr '[:lower:]' '[:upper:]')",
    "headers": {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json"
    },
    "queryStringParameters": null,
    "pathParameters": null,
    "body": "{\"test\":\"data\"}",
    "isBase64Encoded": false
}
EOF

echo "✓ Created Lambda directory structure"
echo "✓ Created handler.py"
echo "✓ Created test event"

# Add to template.yaml
echo ""
echo "📝 Add this to template.yaml under Resources section:"
echo ""
cat << EOF
  $FUNCTION_CLASS:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: drishlio-$FUNCTION_NAME
      CodeUri: .
      Handler: lambdas.$FUNCTION_NAME.handler.lambda_handler
      Description: Lambda function for $FUNCTION_NAME
      Events:
        Api:
          Type: Api
          Properties:
            Path: $API_PATH
            Method: $HTTP_METHOD
EOF

echo ""
echo "📝 Add this to serverless.yml under functions section:"
echo ""
cat << EOF
  $(echo $FUNCTION_NAME | sed 's/_//g'):
    handler: lambdas/$FUNCTION_NAME/handler.lambda_handler
    name: \${self:provider.stage}-$FUNCTION_NAME
    description: Lambda function for $FUNCTION_NAME
    timeout: 30
    events:
      - http:
          path: ${API_PATH#/}
          method: $HTTP_METHOD
          cors: true
EOF

echo ""
echo "✅ Lambda function '$FUNCTION_NAME' created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $LAMBDA_DIR/handler.py with your logic"
echo "2. Add the function to template.yaml and serverless.yml (see above)"
echo "3. Test locally: python -c 'from $LAMBDA_DIR.handler import lambda_handler; print(lambda_handler({}, {}))'"
echo ""
