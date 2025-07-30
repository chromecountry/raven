#!/usr/bin/env python3

"""
Bank statement processor for parsing CSV files and comparing with ledger
"""

import csv
from datetime import datetime
from typing import Dict, List
from src.processors.ledger_manager import LedgerManager


class BankProcessor:
    def __init__(self, ledger_manager: LedgerManager) -> None:
        self.ledger_manager = ledger_manager

    def parse_csv(self, csv_path: str) -> List[Dict]:
        """Parse bank statement CSV file using pure Python"""
        try:
            transactions = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transaction = {
                        'date': self._parse_date(row.get('Date', '')),
                        'description': row.get('Description', ''),
                        'amount': row.get('Amount', 0),
                        'type': row.get('Type', '')
                    }
                    transactions.append(transaction)

            return transactions
        except Exception as e:
            print(f'Error parsing CSV: {e}')
            return []

    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime"""
        try:
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    return datetime.strptime(date_str.strip(), fmt).date()
                except ValueError:
                    continue
            return datetime.now().date()
        except Exception:
            return datetime.now().date()

    def compare_transactions(self, bank_transactions: List[Dict]) -> Dict:
        """Compare bank transactions with ledger"""
        ledger_transactions = self.ledger_manager.get_transactions()

        # Normalize amounts for comparison
        bank_normalized = self._normalize_transactions(bank_transactions)
        ledger_normalized = self._normalize_transactions(ledger_transactions)

        # Find matches
        matches = []
        ledger_only = []
        bank_only = []

        for bank_tx in bank_normalized:
            matched = False
            for ledger_tx in ledger_normalized:
                if self._transactions_match(bank_tx, ledger_tx):
                    matches.append({
                        'bank': bank_tx,
                        'ledger': ledger_tx
                    })
                    matched = True
                    break
            if not matched:
                bank_only.append(bank_tx)

        # Find ledger-only transactions
        for ledger_tx in ledger_normalized:
            matched = False
            for match in matches:
                if match['ledger'] == ledger_tx:
                    matched = True
                    break
            if not matched:
                ledger_only.append(ledger_tx)

        return {
            'matches': matches,
            'ledger_only': ledger_only,
            'bank_only': bank_only
        }

    def _normalize_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Normalize transaction format for comparison"""
        normalized = []
        for tx in transactions:
            # Convert amount to float, handling string formatting
            amount_str = str(tx.get('amount', 0))
            amount = float(amount_str.replace('$', '').replace(',', ''))
            
            normalized.append({
                'date': tx.get('date'),
                'amount': amount,
                'description': tx.get('description', tx.get('payee', ''))
            })
        return normalized

    def _transactions_match(self, tx1: Dict, tx2: Dict) -> bool:
        """Check if two transactions match"""
        # Simple matching logic - can be enhanced
        amount_match = abs(tx1['amount'] - tx2['amount']) < 0.01
        date_match = tx1['date'] == tx2['date']
        
        return amount_match and date_match
