#!/usr/bin/env python3

"""
Beancount ledger manager for storing and retrieving transactions
"""

from datetime import datetime
from typing import Dict, List, Optional
from beancount.core import data
from beancount.core.amount import Amount
from beancount.core.number import D
from beancount.parser import printer
from src.core.config import BEANCOUNT_FILE


class LedgerManager:
    def __init__(self) -> None:
        self.entries = []
        self._ensure_accounts_exist()
        self._load_ledger()

    def _ensure_accounts_exist(self) -> None:
        """Ensure required accounts exist in the ledger"""
        # Define the accounts we need
        accounts = [
            ('Assets:Checking', 'USD'),
            ('Expenses:Receipts', 'USD')
        ]

        # Check if accounts already exist
        existing_accounts = set()
        for entry in self.entries:
            if isinstance(entry, data.Open):
                existing_accounts.add(entry.account)

        # Create account opening entries if they don't exist
        for account_name, currency in accounts:
            if account_name not in existing_accounts:
                account_entry = data.Open(
                    meta=data.new_metadata(BEANCOUNT_FILE, 0),
                    date=datetime(1970, 1, 1).date(),  # Unix epoch date
                    account=account_name,
                    currencies=[currency],
                    booking=None
                )
                self.entries.append(account_entry)

    def _load_ledger(self) -> None:
        """Load existing ledger entries"""
        if BEANCOUNT_FILE.exists():
            try:
                from beancount.parser import parser
                entries, errors, options = parser.parse_file(
                    str(BEANCOUNT_FILE)
                )
                if not errors:
                    self.entries = entries
            except Exception:
                # If parsing fails, start with empty entries
                self.entries = []

    def add_transaction(self, receipt_data: Dict[str, Optional[str]]) -> None:
        """Add a transaction from receipt data"""
        if not receipt_data.get('amount'):
            return

        amount = D(receipt_data['amount'].replace('$', ''))
        date = self._parse_date(receipt_data.get('date'))
        merchant = receipt_data.get('merchant', 'Unknown')

        # Create Beancount transaction
        transaction = data.Transaction(
            meta=data.new_metadata(BEANCOUNT_FILE, 0),
            date=date,
            flag='*',
            payee=merchant,
            narration='Receipt from email',
            tags=set(),
            links=set(),
            postings=[
                data.Posting(
                    account='Expenses:Receipts',
                    units=Amount(amount, 'USD'),
                    cost=None,
                    price=None,
                    flag=None,
                    meta=None
                ),
                data.Posting(
                    account='Assets:Checking',
                    units=Amount(-amount, 'USD'),
                    cost=None,
                    price=None,
                    flag=None,
                    meta=None
                )
            ]
        )

        self.entries.append(transaction)
        self._save_ledger()

    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string to datetime"""
        if not date_str:
            return datetime.now().date()

        try:
            return datetime.strptime(date_str, '%m/%d/%y').date()
        except ValueError:
            try:
                return datetime.strptime(date_str, '%m/%d/%Y').date()
            except ValueError:
                return datetime.now().date()

    def _save_ledger(self) -> None:
        """Save ledger to file"""
        with open(BEANCOUNT_FILE, 'w') as f:
            # Write account opening entries first
            for entry in self.entries:
                if isinstance(entry, data.Open):
                    f.write(printer.format_entry(entry))

            # Then write transactions
            for entry in self.entries:
                if isinstance(entry, data.Transaction):
                    f.write(printer.format_entry(entry))

    def get_transactions(self) -> List[Dict]:
        """Get all transactions as dictionaries"""
        transactions = []
        for entry in self.entries:
            if isinstance(entry, data.Transaction):
                transactions.append({
                    'date': entry.date,
                    'payee': entry.payee,
                    'amount': str(entry.postings[0].units.number),
                    'currency': str(entry.postings[0].units.currency)
                })
        return transactions
