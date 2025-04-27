#!/usr/bin/env python3
"""
Run unit tests under tests/unit/, track coverage, output missing features to markdown.
"""

import os
import sys
import subprocess
from pathlib import Path
import json
import re

def main():
    PROJECT_ROOT = Path("/Users/hongyuanfan/Downloads/lianV3-501a294797023b7f3fa802ddb963f1a4b1577785/backenddjango")
    os.chdir(PROJECT_ROOT)
    TEST_REPORT_PATH = PROJECT_ROOT / "tests" / "TestCoverageReport.md"

    subprocess.run(["coverage", "erase"], check=True)

    result = subprocess.run(
        "find tests/unit -name 'test_*.py' | sort",
        shell=True, check=True, capture_output=True, text=True
    )
    test_files = result.stdout.strip().split('\n')
    total_files = len(test_files)

    print(f"Found {total_files} test files to run")

    successful_tests = 0
    failed_tests = []

    for i, test_file in enumerate(test_files, 1):
        if not test_file.endswith('.py'):
            continue

        print(f"\n[{i}/{total_files}] Running {test_file}...")
        coverage_cmd = ["coverage", "run"]
        if i > 1:
            coverage_cmd.append("--append")

        cmd = coverage_cmd + ["-m", "pytest", test_file, "-v"]

        try:
            subprocess.run(cmd, check=True)
            successful_tests += 1
        except subprocess.CalledProcessError:
            failed_tests.append(test_file)
            print(f"❌ Test failed: {test_file}")

    subprocess.run(["coverage", "report"], check=True)
    subprocess.run(["coverage", "html"], check=True)
    subprocess.run(["coverage", "json", "-o", "coverage.json"], check=True)

    write_test_coverage_report(test_files, failed_tests, TEST_REPORT_PATH)
    update_test_gap_report()
    detect_missing_features(TEST_REPORT_PATH)  # [NEW]

    return 0

def write_test_coverage_report(all_tests, failed_tests, report_path):
    with open('coverage.json', 'r') as f:
        coverage_data = json.load(f)

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
        coverage_pct = data['summary']['percent_covered']

        modules.append({
            'module': module_name,
            'statements': statements,
            'missing': missing,
            'coverage_pct': coverage_pct
        })

    modules.sort(key=lambda x: x['coverage_pct'])

    md_lines = []
    md_lines.append("# 🧪 Test Coverage Report\n")
    md_lines.append("## 📄 Summary\n")
    md_lines.append(f"- Total test files found: **{len(all_tests)}**")
    md_lines.append(f"- Successful tests: **{len(all_tests) - len(failed_tests)}**")
    md_lines.append(f"- Failed tests: **{len(failed_tests)}**\n")

    if failed_tests:
        md_lines.append("## ❌ Failed Tests\n")
        for test in failed_tests:
            md_lines.append(f"- {test}")
        md_lines.append("")
    else:
        md_lines.append("✅ All tests passed!\n")

    md_lines.append("## 📈 Module Coverage Overview\n")
    md_lines.append("| Module | Statements | Missed | Coverage |")
    md_lines.append("|--------|------------|--------|----------|")

    for module in modules:
        md_lines.append(f"| {module['module']} | {module['statements']} | {module['missing']} | {module['coverage_pct']:.0f}% |")

    with open(report_path, 'w') as f:
        f.write("\n".join(md_lines))

    print(f"\n✅ Test coverage summary written to: {report_path}")

def update_test_gap_report():
    try:
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
    except FileNotFoundError:
        print("❌ coverage.json not found.")
        return

    test_gap_path = 'tests/TestGapUnitNew.md'
    try:
        with open(test_gap_path, 'r') as f:
            content = f.read()

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
            coverage_pct = data['summary']['percent_covered']
            status = '✅' if coverage_pct >= 90 else '⚠️' if coverage_pct >= 50 else '❌'

            modules.append({
                'module': module_name,
                'statements': statements,
                'missing': missing,
                'coverage': f"{coverage_pct:.0f}%",
                'status': status
            })

        modules.sort(key=lambda x: x['module'])

        table_rows = []
        table_rows.append("| Module | Statements | Missed | Coverage | Status |")
        table_rows.append("|--------|------------|--------|----------|--------|")

        for module in modules:
            table_rows.append(f"| {module['module']} | {module['statements']} | {module['missing']} | {module['coverage']} | {module['status']} |")

        table_text = "\n".join(table_rows)
        replacement = f"## Current Test Coverage Matrix\n\n{table_text}\n\n## Test Execution Issues"

        updated_content = re.sub(
            r'## Current Test Coverage Matrix\n\n.*?\n\n## Test Execution Issues',
            replacement,
            content,
            flags=re.DOTALL
        )

        with open(test_gap_path, 'w') as f:
            f.write(updated_content)

        print(f"✅ Updated {test_gap_path}")
    except FileNotFoundError:
        print(f"Warning: {test_gap_path} not found. Skipping update.")

    os.remove('coverage.json')

def detect_missing_features(report_path):
    """Detect missing test classes, functions, services, views, models."""
    print("\n=== Detecting Missing Features for Testing ===\n")
    missing_classes = []
    missing_functions = []
    missing_services = []
    missing_views = []
    missing_models = []

    result = subprocess.run(["coverage", "report", "-m"], capture_output=True, text=True)
    report_text = result.stdout

    lines = report_text.splitlines()
    for line in lines:
        if '/services/' in line and "%" in line and get_coverage_from_line(line) < 90:
            missing_services.append(line.strip())
        if '/views.py' in line and "%" in line and get_coverage_from_line(line) < 90:
            missing_views.append(line.strip())
        if '/models.py' in line and "%" in line and get_coverage_from_line(line) < 90:
            missing_models.append(line.strip())
        if 'def ' in line:
            missing_functions.append(line.strip())
        if 'class ' in line:
            missing_classes.append(line.strip())

    # Append to existing report
    with open(report_path, 'a') as f:
        f.write("\n\n## 🧩 Missing Features Detected\n")

        f.write("\n### ❌ Missing Services\n")
        for item in missing_services:
            f.write(f"- {item}\n")

        f.write("\n### ❌ Missing Views\n")
        for item in missing_views:
            f.write(f"- {item}\n")

        f.write("\n### ❌ Missing Models\n")
        for item in missing_models:
            f.write(f"- {item}\n")

        f.write("\n### ❌ Missing Classes (Code)\n")
        for item in missing_classes:
            f.write(f"- {item}\n")

        f.write("\n### ❌ Missing Functions (Code)\n")
        for item in missing_functions:
            f.write(f"- {item}\n")

def get_coverage_from_line(line):
    parts = re.split(r'\s+', line.strip())
    if len(parts) < 5:
        return 100
    try:
        return int(parts[-1].replace("%", ""))
    except Exception:
        return 100

if __name__ == "__main__":
    sys.exit(main())
