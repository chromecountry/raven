#!/usr/bin/env python3

"""
Email processor for fetching emails with PDF attachments
"""

import email
from email import message
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Tuple, Optional
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

        print(f'Connecting to {EMAIL_HOST}...')
        self.client = IMAPClient(EMAIL_HOST)
        try:
            print(f'Logging in as {EMAIL_USER}...')
            self.client.login(EMAIL_USER, EMAIL_PASSWORD)
            print('Login successful')
        except Exception as exc:
            print(f'Login failed: {exc}')
            raise RuntimeError('Failed to login to email server') from exc

    def fetch_pdf_attachments(
        self,
        folder: str = 'INBOX',
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Tuple[str, Path]]:
        """Fetch emails with PDF attachments within optional time window"""
        if not self.client:
            raise RuntimeError('Email client not connected')

        try:
            print(f'Selecting folder: {folder}')
            self.client.select_folder(folder)

            # Build search criteria
            search_criteria = ['UNSEEN']

            if start_date:
                date_str = start_date.strftime("%d-%b-%Y")
                search_criteria.append(('SINCE', date_str))

            if end_date:
                next_day = end_date + timedelta(days=1)
                date_str = next_day.strftime("%d-%b-%Y")
                search_criteria.append(('BEFORE', date_str))

            print(f'Search criteria: {search_criteria}')
            messages = self.client.search(search_criteria)
            print(f'Found {len(messages)} unread messages')
        except Exception as exc:
            print(f'Search failed: {exc}')
            raise RuntimeError('Failed to fetch emails') from exc

        attachments = []
        for msg_id in messages:
            print(f'Processing message {msg_id}...')
            response = self.client.fetch([msg_id], ['RFC822'])
            email_body = response[msg_id][b'RFC822']
            email_message = email.message_from_bytes(email_body)

            # Check email date if time window is specified
            if start_date or end_date:
                email_date = self._get_email_date(email_message)
                if email_date:
                    print(f'  Email date: {email_date}')
                    if start_date and email_date < start_date:
                        print(f'  Skipping - before start date {start_date}')
                        continue
                    if end_date and email_date > end_date:
                        print(f'  Skipping - after end date {end_date}')
                        continue
                else:
                    print('  Could not parse email date')

            pdf_count = 0
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                filename = part.get_filename()
                if filename and filename.lower().endswith('.pdf'):
                    pdf_count += 1
                    print(f'  Found PDF attachment: {filename}')
                    # Save attachment
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_path = ATTACHMENTS_DIR / f"{timestamp}_{filename}"
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    attachments.append((filename, file_path))

            if pdf_count == 0:
                print('  No PDF attachments found')

        return attachments

    def _get_email_date(
        self,
        email_message: message.Message
    ) -> Optional[date]:
        """Extract email date from message headers"""
        date_str = email_message.get('Date')
        if not date_str:
            return None

        try:
            # Parse email date string
            parsed_date = email.utils.parsedate_to_datetime(date_str)
            return parsed_date.date()
        except (TypeError, ValueError):
            return None

    def close(self) -> None:
        """Close email connection"""
        if self.client:
            self.client.logout()
