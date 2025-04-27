#!/usr/bin/env python3
"""
Run all tests with coverage and generate a comprehensive report.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Change to the Django project directory
    os.chdir(Path(__file__).parent)
    
    # Clear previous coverage data
    subprocess.run(["coverage", "erase"], check=True)
    
    # Run tests with coverage
    print("=== Running all tests with coverage ===")
    
    # Run Django tests with coverage
    cmd = [
        "coverage", "run", "--source=.",
        "manage.py", "test",
        "--exclude-tag=slow",
        "tests.unit"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Some tests failed, but continuing to generate coverage report")
    
    # Generate coverage report
    print("\n=== Coverage Report ===")
    subprocess.run(["coverage", "report"], check=True)
    
    # Generate HTML report
    print("\nGenerating HTML coverage report...")
    subprocess.run(["coverage", "html"], check=True)
    print("HTML coverage report available at: htmlcov/index.html")
    
    # Update the TestGapUnitNew.md file with latest coverage data
    update_test_gap_report()
    
    return 0

def update_test_gap_report():
    """Update the TestGapUnitNew.md file with latest coverage data"""
    print("\n=== Updating TestGapUnitNew.md with latest coverage data ===")
    
    # Get coverage data in JSON format
    result = subprocess.run(
        ["coverage", "json", "-o", "coverage.json"],
        check=True
    )
    
    # Parse the JSON data
    import json
    with open('coverage.json', 'r') as f:
        coverage_data = json.load(f)
    
    # Extract module coverage information
    modules = []
    for file_path, data in coverage_data['files'].items():
        if '/site-packages/' in file_path or '/env/' in file_path or '/venv/' in file_path:
            continue
            
        if file_path.startswith('./'):
            module_name = file_path[2:]
        else:
            module_name = file_path
            
        if not module_name.endswith('.py'):
            continue
            
        statements = data['summary']['num_statements']
        missing = data['summary']['missing_lines']
        covered = statements - missing
        coverage_pct = data['summary']['percent_covered']
        
        status = '✅' if coverage_pct >= 90 else '⚠️' if coverage_pct >= 50 else '❌'
        
        modules.append({
            'module': module_name,
            'statements': statements,
            'missing': missing,
            'coverage': f"{coverage_pct:.0f}%",
            'status': status
        })
    
    # Sort modules by name
    modules.sort(key=lambda x: x['module'])
    
    # Generate markdown table
    table_rows = []
    table_rows.append("| Module | Statements | Missed | Coverage | Status |")
    table_rows.append("|--------|-----------|--------|----------|--------|")
    
    for module in modules:
        table_rows.append(f"| {module['module']} | {module['statements']} | {module['missing']} | {module['coverage']} | {module['status']} |")
    
    # Read existing file
    test_gap_path = '/Users/hongyuanfan/Downloads/lianV3-501a294797023b7f3fa802ddb963f1a4b1577785/backenddjango/tests/TestGapUnitNew.md'
    with open(test_gap_path, 'r') as f:
        content = f.read()
    
    # Replace the coverage matrix section
    import re
    table_text = "\n".join(table_rows)
    replacement = f"## Current Test Coverage Matrix\n\n{table_text}\n\n## Test Execution Issues"
    updated_content = re.sub(
        r'## Current Test Coverage Matrix\n\n.*?\n\n## Test Execution Issues', 
        replacement, 
        content, 
        flags=re.DOTALL
    )
    
    # Update the file
    with open(test_gap_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated {test_gap_path} with latest coverage data")
    
    # Clean up
    os.remove('coverage.json')

if __name__ == "__main__":
    sys.exit(main())
