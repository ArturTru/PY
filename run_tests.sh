#!/bin/bash
set -e

scope="${1:-all}"

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

case "$scope" in
    all) pytest tests/ -v ;;
    smoke) pytest tests/smoke -v -m smoke ;;
    acceptance) pytest tests/acceptance -v -m acceptance ;;
    ui) pytest tests/smoke/test_ui.py tests/acceptance/test_ui.py -v ;;
    api) pytest tests/smoke/test_api.py tests/acceptance/test_api.py -v ;;
    *)
        echo "usage: ./run_tests.sh [all|smoke|acceptance|ui|api]"
        exit 1
        ;;
esac
