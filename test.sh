#!/usr/bin/env bash
# usage: ./test.sh account_id junit-path coverage-path

pwd=$(pwd)
JUNIT_PATH=${1-${pwd}/reports/junit.xml}
COVERAGE_PATH=${2-${pwd}/reports/coverage.xml}

echo "Junit Path: $JUNIT_PATH"
echo "Coverage Path: $COVERAGE_PATH"

echo "Running tests"
pytest --cov --cov-report=term-missing -v
