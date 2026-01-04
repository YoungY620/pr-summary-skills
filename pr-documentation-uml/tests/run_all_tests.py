#!/usr/bin/env python3
"""
Run all tests for the PR Documentation with UML skill.

Usage:
    python3 run_all_tests.py
"""

import sys
import subprocess
from pathlib import Path


def run_test(test_file: Path) -> bool:
    """Run a single test file and return success status."""
    print(f"\n{'='*80}")
    print(f"Running: {test_file.name}")
    print('='*80)
    
    result = subprocess.run(
        [sys.executable, str(test_file)],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def main():
    """Run all test files."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found!")
        return 1
    
    print(f"Found {len(test_files)} test files")
    
    results = {}
    for test_file in test_files:
        results[test_file.name] = run_test(test_file)
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print('='*80)
    
    passed = sum(1 for success in results.values() if success)
    failed = len(results) - passed
    
    for test_name, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! ✅")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

