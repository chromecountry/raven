#!/usr/bin/env python3

"""
Bank statement comparison tool
"""

import sys
from typing import Dict
from ledger_manager import LedgerManager
from bank_processor import BankProcessor


def compare_bank_statement(csv_path: str) -> Dict:
    """Compare bank statement with ledger"""
    ledger_manager = LedgerManager()
    bank_processor = BankProcessor(ledger_manager)

    print(f'Parsing bank statement: {csv_path}')
    bank_transactions = bank_processor.parse_csv(csv_path)

    print(f'Found {len(bank_transactions)} bank transactions')
    ledger_count = len(ledger_manager.get_transactions())
    print(f'Found {ledger_count} ledger transactions')

    comparison = bank_processor.compare_transactions(bank_transactions)

    return comparison


def print_comparison(comparison: Dict) -> None:
    """Print comparison results"""
    print('\n' + '='*50)
    print('COMPARISON RESULTS')
    print('='*50)

    print(f'\nMatching Transactions ({len(comparison["matches"])}):')
    print('-' * 40)
    for match in comparison['matches']:
        bank = match['bank']
        print(f'{bank["date"]} | {bank["description"]} | ${bank["amount"]}')

    print(f'\nLedger Only ({len(comparison["ledger_only"])}):')
    print('-' * 40)
    for tx in comparison['ledger_only']:
        print(f'{tx["date"]} | {tx["description"]} | ${tx["amount"]}')

    print(f'\nBank Only ({len(comparison["bank_only"])}):')
    print('-' * 40)
    for tx in comparison['bank_only']:
        print(f'{tx["date"]} | {tx["description"]} | ${tx["amount"]}')


def main() -> int:
    """Main entry point"""
    if len(sys.argv) != 2:
        print('Usage: python bank_comparison.py <csv_file>')
        return 1

    csv_path = sys.argv[1]

    try:
        comparison = compare_bank_statement(csv_path)
        print_comparison(comparison)
        return 0
    except Exception as e:
        print(f'Error: {e}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
