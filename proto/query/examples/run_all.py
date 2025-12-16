#!/usr/bin/env python3
"""
Run All Examples - Execute all query examples

Runs all example scripts and reports results.
Useful for testing that all examples construct valid queries.
"""

import sys
import importlib.util
from pathlib import Path


def run_example_module(module_path: Path) -> tuple[bool, str]:
    """
    Run an example module and return success status
    
    Args:
        module_path: Path to Python module
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Load module dynamically
        spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
        if spec is None or spec.loader is None:
            return False, "Could not load module"
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_path.stem] = module
        spec.loader.exec_module(module)
        
        # Run main function if exists
        if hasattr(module, 'main'):
            module.main()
            return True, ""
        else:
            return False, "No main() function found"
            
    except Exception as e:
        return False, str(e)


def main():
    """Run all example files"""
    examples_dir = Path(__file__).parent
    
    # List of example files to run
    example_files = [
        "basic_queries.py",
        "advanced_queries.py",
        "ecommerce_examples.py",
        "query_builder.py"
    ]
    
    print("=" * 70)
    print("RUNNING ALL QUERY EXAMPLES")
    print("=" * 70)
    print()
    
    results = []
    
    for example_file in example_files:
        example_path = examples_dir / example_file
        
        if not example_path.exists():
            print(f"⚠️  Skipping {example_file} (not found)")
            results.append((example_file, False, "File not found"))
            continue
        
        print(f"Running {example_file}...")
        print("-" * 70)
        
        success, error = run_example_module(example_path)
        results.append((example_file, success, error))
        
        if success:
            print(f"✓ {example_file} completed successfully")
        else:
            print(f"✗ {example_file} failed: {error}")
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print()
    
    if passed < total:
        print("Failed examples:")
        for filename, success, error in results:
            if not success:
                print(f"  - {filename}: {error}")
        print()
        sys.exit(1)
    else:
        print("All examples passed! ✓")
        sys.exit(0)


if __name__ == "__main__":
    main()
