# -*- coding: UTF-8 -*-

'''
Module
    demo_runner.py
Info
    Creates a demo package, runs ats_coverage.py, and generates demo_README.md
    with real coverage data and directory structure.
Execute
    python3 tests/demo_runner.py
'''

import os
import shutil
import subprocess
from pathlib import Path

def main():
    print("=== Running Real-world Demo ===")
    
    # 1. Create demo_package
    pkg_dir = Path("demo_package")
    pkg_dir.mkdir(exist_ok=True)
    
    (pkg_dir / "__init__.py").write_text(
        "def greet(name: str) -> str:\n"
        "    if not name:\n"
        "        return 'Hello, Guest!'\n"
        "    return f'Hello, {name}!'\n",
        encoding="utf-8"
    )
    
    (pkg_dir / "calculator.py").write_text(
        "def multiply(a: int, b: int) -> int:\n"
        "    return a * b\n\n"
        "def divide(a: int, b: int) -> float:\n"
        "    if b == 0:\n"
        "        raise ValueError('Cannot divide by zero')\n"
        "    return a / b\n",
        encoding="utf-8"
    )

    # 2. Create test file
    test_dir = Path("tests")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "demo_test.py"
    
    test_file.write_text(
        "import unittest\n"
        "from demo_package import greet\n"
        "from demo_package.calculator import multiply\n\n"
        "class DemoTest(unittest.TestCase):\n"
        "    def test_greet(self):\n"
        "        self.assertEqual(greet('Vladimir'), 'Hello, Vladimir!')\n"
        "    def test_multiply(self):\n"
        "        self.assertEqual(multiply(3, 4), 12)\n",
        encoding="utf-8"
    )

    # 3. Create initial README.md
    readme_content = (
        "# Demo Project\n\n"
        "This is an example project for testing the ats_coverage tool.\n\n"
        "### Tool structure\n"
        "<details>\n"
        "<summary>Structure</summary>\n"
        "</details>\n\n"
        "### Code coverage\n"
        "<details>\n"
        "<summary>Coverage</summary>\n"
        "</details>\n\n"
        "### Docs\n"
    )
    
    # If README.md already exists, back it up
    has_original_readme = os.path.exists("README.md")
    if has_original_readme:
        shutil.move("README.md", "README.md.bak")
        
    Path("README.md").write_text(readme_content, encoding="utf-8")

    try:
        # 4. Run ats_coverage.py script
        print("Running: python3 ats_coverage.py demo_package")
        result = subprocess.run(
            ["python3", "ats_coverage.py", "demo_package"],
            capture_output=True,
            text=True
        )
        
        print("\n--- Script Console ---")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print("-----------------------\n")
        
        # 5. Move README.md to demo_README.md
        if os.path.exists("README.md"):
            shutil.move("README.md", "demo_README.md")
            print("Successfully generated: demo_README.md")
            
    finally:
        # Restore original README.md if it existed
        if has_original_readme and os.path.exists("README.md.bak"):
            shutil.move("README.md.bak", "README.md")
            
        # Clean up temporary tests and demo packages to keep workspace clean
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)
        if test_file.exists():
            test_file.unlink()
            
        # If tests folder is empty, delete it
        if test_dir.exists() and not os.listdir(test_dir):
            test_dir.rmdir()

    print("\nDone! You can open 'demo_README.md' in your editor to see the result.")

if __name__ == "__main__":
    main()
