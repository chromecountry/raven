#!/usr/bin/env python3

"""
Configuration settings for the receipt processing system
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Import credentials
try:
    from .credentials import (
        EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD,
        FAVA_HOST, FAVA_PORT
    )
except ImportError:
    # Fallback to environment variables if credentials.py doesn't exist
    load_dotenv()
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'imap.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '993'))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    FAVA_HOST = os.getenv('FAVA_HOST', 'localhost')
    FAVA_PORT = int(os.getenv('FAVA_PORT', '5000'))

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'ledger'
BEANCOUNT_FILE = DATA_DIR / 'ledger.beancount'
ATTACHMENTS_DIR = PROJECT_ROOT / 'data' / 'attachments'

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
