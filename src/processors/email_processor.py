#!/usr/bin/env python3

"""
Email processor for fetching emails with PDF attachments
"""

import email
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from imapclient import IMAPClient
from src.core.config import (
    EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD, ATTACHMENTS_DIR
)


class EmailProcessor:
    def __init__(self) -> None:
        self.client = None
        self._connect()

    def _connect(self) -> None:
        """Connect to email server"""
        if not EMAIL_USER or not EMAIL_PASSWORD:
            raise ValueError('Email credentials not configured')

        self.client = IMAPClient(EMAIL_HOST)
        try:
            self.client.login(EMAIL_USER, EMAIL_PASSWORD)
        except Exception as exc:
            raise RuntimeError('Failed to login to email server') from exc

    def fetch_pdf_attachments(self, folder: str = 'INBOX') -> List[Tuple[str, Path]]:
        """Fetch emails with PDF attachments"""
        if not self.client:
            raise RuntimeError('Email client not connected')
        try:
            self.client.select_folder(folder)
            messages = self.client.search(['UNSEEN'])
        except Exception as exc:
            raise RuntimeError('Failed to fetch emails') from exc

        attachments = []
        for msg_id in messages:
            response = self.client.fetch([msg_id], ['RFC822'])
            email_body = response[msg_id][b'RFC822']
            email_message = email.message_from_bytes(email_body)

            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                filename = part.get_filename()
                if filename and filename.lower().endswith('.pdf'):
                    # Save attachment
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_path = ATTACHMENTS_DIR / f"{timestamp}_{filename}"
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    attachments.append((filename, file_path))

        return attachments

    def close(self) -> None:
        """Close email connection"""
        if self.client:
            self.client.logout()
