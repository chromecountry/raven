#!/usr/bin/env python3

"""
Generate sample PDF receipts for testing
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime, timedelta
import random


def create_receipt_pdf(
    filename: str,
    merchant: str,
    amount: float,
    date: datetime
) -> None:
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    story.append(Paragraph(merchant.upper(), title_style))
    story.append(Spacer(1, 20))

    # Date and time
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1
    )
    story.append(Paragraph(f"Date: {date.strftime('%m/%d/%Y')}", date_style))
    story.append(Paragraph(f"Time: {date.strftime('%I:%M %p')}", date_style))
    story.append(Spacer(1, 20))

    # Receipt items
    items_data = [
        ['Item', 'Qty', 'Price', 'Total'],
        ['Sample Item', '1', f'${amount:.2f}', f'${amount:.2f}'],
    ]

    # Add some random items for variety
    if amount > 10:
        item_price = amount * 0.7
        items_data.append([
            'Additional Item',
            '1',
            f'${item_price:.2f}',
            f'${item_price:.2f}'
        ])
        remaining = amount - item_price
        if remaining > 0:
            items_data.append([
                'Tax/Service',
                '1',
                f'${remaining:.2f}',
                f'${remaining:.2f}'
            ])

    table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),  # Right align totals
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Total
    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=1,
        spaceAfter=20
    )
    story.append(Paragraph(f"TOTAL: ${amount:.2f}", total_style))

    # Footer
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1,
        textColor=colors.grey
    )
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you for your purchase!", footer_style))
    story.append(
        Paragraph("Receipt generated for testing purposes", footer_style)
    )

    doc.build(story)


def generate_sample_receipts() -> None:
    """Generate a set of sample receipt PDFs"""
    sample_dir = Path('sample_data/receipts')
    sample_dir.mkdir(parents=True, exist_ok=True)

    # Sample merchants and amounts
    merchants = [
        'Walmart Supercenter',
        'Starbucks Coffee',
        'Amazon.com',
        'Shell Gas Station',
        'Netflix',
        'Uber',
        'Whole Foods Market',
        'Apple Store',
        'Chipotle Mexican Grill',
        'CVS Pharmacy',
        'Spotify Premium',
        'Target Store',
        'DoorDash',
        'Costco Wholesale'
    ]

    # Generate receipts for the last 15 days
    base_date = datetime.now() - timedelta(days=15)

    for i, merchant in enumerate(merchants):
        # Generate a random amount between $5 and $200
        amount = round(random.uniform(5, 200), 2)
        date = base_date + timedelta(days=i)

        filename = sample_dir / f"receipt_{i+1:02d}_{merchant.lower().replace(' ', '_')}.pdf"
        create_receipt_pdf(str(filename), merchant, amount, date)
        print(f"Created: {filename}")


if __name__ == '__main__':
    generate_sample_receipts()
