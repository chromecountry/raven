#!/usr/bin/env python3

"""
Unit tests for email processor time window functionality
"""

import unittest
from datetime import date, datetime
from unittest.mock import Mock, patch
from src.processors.email_processor import EmailProcessor


class TestEmailProcessorTimeWindow(unittest.TestCase):
    """Test time window constraints in email processing"""

    def setUp(self):
        """Set up test fixtures"""
        with patch('src.processors.email_processor.EMAIL_USER', 'test@example.com'), \
             patch('src.processors.email_processor.EMAIL_PASSWORD', 'password'), \
             patch('src.processors.email_processor.EMAIL_HOST', 'imap.example.com'):
            self.processor = EmailProcessor()

    def test_fetch_pdf_attachments_no_time_window(self):
        """Test fetching emails without time window constraints"""
        with patch.object(self.processor, 'client') as mock_client:
            mock_client.search.return_value = [1, 2, 3]
            mock_client.fetch.return_value = {
                1: {b'RFC822': b'email content'},
                2: {b'RFC822': b'email content'},
                3: {b'RFC822': b'email content'}
            }
            
            with patch('email.message_from_bytes') as mock_parse:
                mock_message = Mock()
                mock_message.walk.return_value = [Mock()]
                mock_parse.return_value = mock_message
                
                result = self.processor.fetch_pdf_attachments()
                
                # Verify search was called with UNSEEN only
                mock_client.search.assert_called_with(['UNSEEN'])
                self.assertEqual(result, [])

    def test_fetch_pdf_attachments_with_start_date(self):
        """Test fetching emails with start date constraint"""
        start_date = date(2024, 1, 1)
        
        with patch.object(self.processor, 'client') as mock_client:
            mock_client.search.return_value = [1]
            mock_client.fetch.return_value = {
                1: {b'RFC822': b'email content'}
            }
            
            with patch('email.message_from_bytes') as mock_parse:
                mock_message = Mock()
                mock_message.walk.return_value = [Mock()]
                mock_parse.return_value = mock_message
                
                result = self.processor.fetch_pdf_attachments(start_date=start_date)
                
                # Verify search was called with SINCE criteria
                expected_criteria = ['UNSEEN', 'SINCE 01-Jan-2024']
                mock_client.search.assert_called_with(expected_criteria)
                self.assertEqual(result, [])

    def test_fetch_pdf_attachments_with_end_date(self):
        """Test fetching emails with end date constraint"""
        end_date = date(2024, 1, 31)
        
        with patch.object(self.processor, 'client') as mock_client:
            mock_client.search.return_value = [1]
            mock_client.fetch.return_value = {
                1: {b'RFC822': b'email content'}
            }
            
            with patch('email.message_from_bytes') as mock_parse:
                mock_message = Mock()
                mock_message.walk.return_value = [Mock()]
                mock_parse.return_value = mock_message
                
                result = self.processor.fetch_pdf_attachments(end_date=end_date)
                
                # Verify search was called with BEFORE criteria
                expected_criteria = ['UNSEEN', 'BEFORE 01-Feb-2024']
                mock_client.search.assert_called_with(expected_criteria)
                self.assertEqual(result, [])

    def test_fetch_pdf_attachments_with_date_range(self):
        """Test fetching emails with both start and end date constraints"""
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 31)
        
        with patch.object(self.processor, 'client') as mock_client:
            mock_client.search.return_value = [1]
            mock_client.fetch.return_value = {
                1: {b'RFC822': b'email content'}
            }
            
            with patch('email.message_from_bytes') as mock_parse:
                mock_message = Mock()
                mock_message.walk.return_value = [Mock()]
                mock_parse.return_value = mock_message
                
                result = self.processor.fetch_pdf_attachments(
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Verify search was called with both SINCE and BEFORE criteria
                expected_criteria = [
                    'UNSEEN', 
                    'SINCE 01-Jan-2024',
                    'BEFORE 01-Feb-2024'
                ]
                mock_client.search.assert_called_with(expected_criteria)
                self.assertEqual(result, [])

    def test_get_email_date_valid(self):
        """Test extracting valid email date"""
        mock_message = Mock()
        mock_message.get.return_value = 'Mon, 15 Jan 2024 10:30:00 +0000'
        
        with patch('email.utils.parsedate_to_datetime') as mock_parse:
            mock_parse.return_value = datetime(2024, 1, 15, 10, 30, 0)
            
            result = self.processor._get_email_date(mock_message)
            
            self.assertEqual(result, date(2024, 1, 15))

    def test_get_email_date_invalid(self):
        """Test extracting invalid email date"""
        mock_message = Mock()
        mock_message.get.return_value = 'invalid date'
        
        with patch('email.utils.parsedate_to_datetime') as mock_parse:
            mock_parse.side_effect = ValueError('Invalid date')
            
            result = self.processor._get_email_date(mock_message)
            
            self.assertIsNone(result)

    def test_get_email_date_missing(self):
        """Test extracting missing email date"""
        mock_message = Mock()
        mock_message.get.return_value = None
        
        result = self.processor._get_email_date(mock_message)
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main() 