#!/bin/bash

# Setup script for Drishlio Lambda project
# This script sets up the development environment

set -e

echo "🚀 Setting up Drishlio Lambda Project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please update it with your credentials."
else
    echo "✓ .env file already exists"
fi

# Check if AWS CLI is installed
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI is installed"
else
    echo "⚠️  AWS CLI is not installed. Consider installing it for easier deployment."
fi

# Check if SAM CLI is installed
if command -v sam &> /dev/null; then
    echo "✓ AWS SAM CLI is installed"
else
    echo "⚠️  AWS SAM CLI is not installed. Install it for local testing: pip install aws-sam-cli"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your AWS credentials and configuration"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Test locally: python test_local.py"
echo "4. Or start SAM local API: sam local start-api --env-vars .env"
echo ""
