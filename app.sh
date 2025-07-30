#!/usr/bin/env bash

# Raven Receipt Processing System
# Main application script

set -e

# Default environment
ENV=${PROJECT_ENV_TYPE:-prd}

show_usage() {
    echo "Raven Receipt Processing System"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  process-emails [START_DATE] [END_DATE]  Process emails with optional date range"
    echo "  launch-fava                              Launch Fava web interface"
    echo "  compare-bank                             Compare bank statement with ledger"
    echo "  setup                                    Setup the project"
    echo "  test                                     Run tests"
    echo "  help                                     Show this help"
    echo ""
    echo "Options:"
    echo "  --env ENV                                Environment (dev|stg|prd, default: prd)"
    echo "  --help                                   Show this help"
    echo ""
    echo "Date Format: YYYY-MM-DD (e.g., 2024-01-15)"
    echo ""
    echo "Examples:"
    echo "  $0 process-emails"
    echo "  $0 process-emails 2024-01-01 2024-01-31"
    echo "  $0 launch-fava"
    echo "  $0 --env dev process-emails 2024-01-01"
    echo "  $0 compare-bank data/sample_data/sample_bank_statement.csv"
}

# Parse command line arguments
COMMAND=""
CSV_FILE=""
START_DATE=""
END_DATE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        process-emails)
            COMMAND="$1"
            shift
            # Check for date arguments
            if [[ -n "$1" && "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                START_DATE="$1"
                shift
                if [[ -n "$1" && "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                    END_DATE="$1"
                    shift
                fi
            fi
            ;;
        launch-fava|setup|test|help)
            COMMAND="$1"
            shift
            ;;
        compare-bank)
            COMMAND="$1"
            if [[ -n "$2" && "$2" != --* ]]; then
                CSV_FILE="$2"
                shift 2
            else
                shift
            fi
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Set environment
export ENV

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Execute command
case $COMMAND in
    process-emails)
        echo "Processing emails in $ENV environment..."
        if [[ -n "$START_DATE" ]]; then
            echo "Date range: $START_DATE"
            if [[ -n "$END_DATE" ]]; then
                echo " to $END_DATE"
            fi
        fi
        PYTHONPATH=. python src/ui/main.py process-emails "$START_DATE" "$END_DATE"
        ;;
    launch-fava)
        echo "Launching Fava in $ENV environment..."
        PYTHONPATH=. python src/ui/main.py launch-fava
        ;;
    compare-bank)
        if [ -z "$CSV_FILE" ]; then
            echo "Error: CSV file required for compare-bank command"
            echo "Usage: $0 compare-bank <csv_file>"
            exit 1
        fi
        echo "Comparing bank statement: $CSV_FILE"
        PYTHONPATH=. python src/ui/bank_comparison.py "$CSV_FILE"
        ;;
    setup)
        echo "Setting up project..."
        ./tools/setup.sh
        ;;
    test)
        echo "Running tests..."
        python tests/integration/test_system.py
        ;;
    help|"")
        show_usage
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_usage
        exit 1
        ;;
esac 