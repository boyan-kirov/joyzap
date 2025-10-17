"""
Local testing script for Lambda functions
Run this to test your Lambda functions locally without SAM
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example: Test file upload lambda
def test_file_upload():
    from lambdas.file_upload.handler import lambda_handler
    
    # Sample event
    event = {
        "headers": {
            "Authorization": "Bearer test-token-here"
        },
        "body": json.dumps({
            "file": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            "file_name": "test_image",
            "is_gift": False
        })
    }
    
    # Mock context
    context = {}
    
    # Call the handler
    result = lambda_handler(event, context)
    
    print("Response Status Code:", result.get('statusCode'))
    print("Response Body:", json.dumps(json.loads(result.get('body', '{}')), indent=2))
    
    return result


if __name__ == "__main__":
    print("=" * 50)
    print("Testing File Upload Lambda")
    print("=" * 50)
    
    try:
        test_file_upload()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
