#!/bin/bash

# Configuration Management Script

set -e

ENV=${1:-prd}

case $ENV in
    dev|stg|prd)
        echo "Setting up $ENV environment..."
        ;;
    *)
        echo "Usage: $0 [dev|stg|prd]"
        echo "Default: prd"
        exit 1
        ;;
esac

# Create environment-specific credentials
if [ ! -f "src/core/credentials_${ENV}.py" ]; then
    echo "Creating credentials for $ENV environment..."
    cp src/core/credentials.py.skel src/core/credentials_${ENV}.py
    echo "Please edit src/core/credentials_${ENV}.py with your $ENV credentials"
fi

# Create environment-specific config
if [ ! -f "cfg/${ENV}/config.py" ]; then
    echo "Creating config for $ENV environment..."
    cat > cfg/${ENV}/config.py << EOF
#!/usr/bin/env python3

"""
Configuration for $ENV environment
"""

import os
from pathlib import Path

# Environment-specific settings
ENV_NAME = '$ENV'

# Import environment-specific credentials
try:
    from src.core.credentials_${ENV} import *
except ImportError:
    print(f"Warning: credentials_${ENV}.py not found")
    from src.core.credentials import *

# Environment-specific paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'ledger'
BEANCOUNT_FILE = DATA_DIR / 'ledger_${ENV}.beancount'
ATTACHMENTS_DIR = PROJECT_ROOT / 'data' / 'attachments'

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
EOF
fi

echo "Configuration for $ENV environment is ready!" 