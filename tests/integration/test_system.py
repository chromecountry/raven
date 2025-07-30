#!/usr/bin/env python3

"""
Test script for the receipt processing system
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path setup
from src.processors.pdf_parser import ReceiptParser  # noqa: E402
from src.processors.ledger_manager import LedgerManager  # noqa: E402
from src.processors.bank_processor import BankProcessor  # noqa: E402


def test_pdf_parsing() -> None:
    """Test PDF parsing with sample receipts"""
    print("Testing PDF parsing...")

    receipt_parser = ReceiptParser()
    receipts_dir = Path('data/sample_data/receipts')

    if not receipts_dir.exists():
        print("No sample receipts found. Run generate_sample_pdfs.py first.")
        return

    for pdf_file in receipts_dir.glob('*.pdf'):
        print(f"\nParsing {pdf_file.name}...")
        receipt_data = receipt_parser.parse_receipt(pdf_file)
        print(f"  Merchant: {receipt_data.get('merchant', 'Unknown')}")
        print(f"  Amount: {receipt_data.get('amount', 'Unknown')}")
        print(f"  Date: {receipt_data.get('date', 'Unknown')}")


def test_bank_comparison_with_matches() -> None:
    """Test bank statement comparison with matching transactions"""
    print("\nTesting bank statement comparison with matches...")

    ledger_manager = LedgerManager()
    bank_processor = BankProcessor(ledger_manager)

    # First, add some transactions to the ledger that match the bank statement
    matching_transactions = [
        {
            'amount': '45.67',
            'date': '01/15/2024',
            'merchant': 'Walmart Supercenter',
            'filename': 'walmart_receipt.pdf'
        },
        {
            'amount': '4.50',
            'date': '01/16/2024',
            'merchant': 'Starbucks Coffee',
            'filename': 'starbucks_receipt.pdf'
        },
        {
            'amount': '23.99',
            'date': '01/17/2024',
            'merchant': 'Amazon.com',
            'filename': 'amazon_receipt.pdf'
        }
    ]

    print("Adding matching transactions to ledger...")
    for tx in matching_transactions:
        ledger_manager.add_transaction(tx)
        print(f"  Added: {tx['merchant']} - ${tx['amount']}")

    # Also add some transactions that are only in the ledger
    ledger_only_transactions = [
        {
            'amount': '15.99',
            'date': '01/18/2024',
            'merchant': 'Local Coffee Shop',
            'filename': 'local_coffee_receipt.pdf'
        },
        {
            'amount': '89.15',
            'date': '01/19/2024',
            'merchant': 'Hardware Store',
            'filename': 'hardware_receipt.pdf'
        }
    ]

    print("Adding ledger-only transactions...")
    for tx in ledger_only_transactions:
        ledger_manager.add_transaction(tx)
        print(f"  Added: {tx['merchant']} - ${tx['amount']}")

    # Now test with bank statement
    csv_file = Path('data/sample_data/sample_bank_statement.csv')
    if not csv_file.exists():
        print("No sample bank statement found.")
        return

    filename = csv_file.name
    print(f"\nParsing {filename}...")
    bank_transactions = bank_processor.parse_csv(str(csv_file))
    print(f"Found {len(bank_transactions)} bank transactions")

    comparison = bank_processor.compare_transactions(bank_transactions)
    print("\nComparison Results:")
    print(f"  Matches: {len(comparison['matches'])}")
    print(f"  Ledger only: {len(comparison['ledger_only'])}")
    print(f"  Bank only: {len(comparison['bank_only'])}")

    # Show some details
    if comparison['matches']:
        print("\nMatching transactions:")
        for match in comparison['matches'][:3]:  # Show first 3
            bank = match['bank']
            date = bank['date']
            desc = bank['description']
            amount = bank['amount']
            print(f"  {date} | {desc} | ${amount}")

    if comparison['ledger_only']:
        print("\nLedger-only transactions:")
        for tx in comparison['ledger_only'][:3]:  # Show first 3
            print(f"  {tx['date']} | {tx['description']} | ${tx['amount']}")

    if comparison['bank_only']:
        print("\nBank-only transactions:")
        for tx in comparison['bank_only'][:3]:  # Show first 3
            print(f"  {tx['date']} | {tx['description']} | ${tx['amount']}")


def test_ledger_operations() -> None:
    """Test ledger operations"""
    print("\nTesting ledger operations...")

    ledger_manager = LedgerManager()

    # Add some test transactions
    test_transactions = [
        {
            'amount': '45.67',
            'date': '01/15/2024',
            'merchant': 'Walmart Supercenter',
            'filename': 'test_receipt.pdf'
        },
        {
            'amount': '4.50',
            'date': '01/16/2024',
            'merchant': 'Starbucks Coffee',
            'filename': 'test_receipt2.pdf'
        }
    ]

    for tx in test_transactions:
        ledger_manager.add_transaction(tx)
        print(f"Added transaction: {tx['merchant']} - ${tx['amount']}")

    transactions = ledger_manager.get_transactions()
    print(f"Total transactions in ledger: {len(transactions)}")


def main() -> int:
    """Main test function"""
    print("Receipt Processing System - Test Suite")
    print("=" * 50)

    try:
        test_pdf_parsing()
        test_ledger_operations()
        test_bank_comparison_with_matches()

        print("\n" + "=" * 50)
        print("All tests completed!")
        return 0

    except Exception as e:
        print(f"Error during testing: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
