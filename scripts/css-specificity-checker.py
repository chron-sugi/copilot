#!/usr/bin/env python3
"""
CSS Specificity Checker

Analyzes CSS selectors and calculates specificity scores according to W3C spec.
Flags selectors that exceed recommended specificity thresholds.

Usage:
    python css-specificity-checker.py <css-file>
    python css-specificity-checker.py --selector "#nav .menu li a"
    python css-specificity-checker.py styles.css --threshold "0,2,3,3"
    python css-specificity-checker.py styles.css --format json

Author: Generated for WebDev AI Agent
"""

import re
import sys
import argparse
import json
from typing import Tuple, List, Dict
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class CSSSpecificityCalculator:
    """
    Calculate CSS selector specificity according to W3C specification.
    Specificity is represented as (inline, ids, classes, elements).
    """

    # Default threshold for BEM-style low-specificity CSS
    DEFAULT_THRESHOLD = (0, 1, 3, 3)

    def __init__(self, threshold: Tuple[int, int, int, int] = None):
        """Initialize calculator with optional custom threshold."""
        self.threshold = threshold or self.DEFAULT_THRESHOLD

    def calculate(self, selector: str) -> Tuple[int, int, int, int]:
        """
        Calculate specificity for a CSS selector.

        Returns: (inline, ids, classes, elements)
        """
        # Handle inline styles
        if 'style=' in selector.lower():
            return (1, 0, 0, 0)

        # Clean selector
        cleaned = self._clean_selector(selector)

        # Count IDs
        ids = len(re.findall(r'#[\w-]+', cleaned))

        # Count classes, attributes, and pseudo-classes
        classes = (
            len(re.findall(r'\.[\w-]+', cleaned)) +  # .class
            len(re.findall(r'\[[\w\-=~|^$*"\':\s]+\]', cleaned)) +  # [attr]
            self._count_pseudo_classes(cleaned)
        )

        # Count elements and pseudo-elements
        elements = (
            self._count_elements(cleaned) +
            len(re.findall(r'::?(?:before|after|first-line|first-letter|backdrop|placeholder|marker|selection)', cleaned))
        )

        return (0, ids, classes, elements)

    def _clean_selector(self, selector: str) -> str:
        """Remove strings and comments from selector."""
        # Remove string content to avoid false matches
        cleaned = re.sub(r'"[^"]*"', '""', selector)
        cleaned = re.sub(r"'[^']*'", "''", cleaned)
        return cleaned.strip()

    def _count_pseudo_classes(self, selector: str) -> int:
        """Count pseudo-classes, handling :not(), :is(), :where() correctly."""
        count = 0

        # Standard pseudo-classes (not pseudo-elements)
        pseudo_classes = re.findall(
            r':(?!not|is|where|has)(?!before|after|first-line|first-letter)[\w-]+',
            selector
        )
        count += len(pseudo_classes)

        # Handle :not() - counts argument specificity, not :not itself
        not_matches = re.findall(r':not\(([^)]+)\)', selector)
        for arg in not_matches:
            spec = self.calculate(arg)
            count += spec[2]  # Add classes from argument

        # Handle :is() and :has() - use highest specificity of arguments
        is_matches = re.findall(r':(?:is|has)\(([^)]+)\)', selector)
        for args in is_matches:
            selectors = args.split(',')
            max_classes = max((self.calculate(s.strip())[2] for s in selectors), default=0)
            count += max_classes

        # :where() always has 0 specificity

        return count

    def _count_elements(self, selector: str) -> int:
        """Count element selectors."""
        # Split by combinators and whitespace
        parts = re.split(r'[\s>+~]+', selector)
        count = 0

        for part in parts:
            # Remove IDs, classes, attributes, and pseudo-classes to isolate element
            element = re.sub(r'#[\w-]+', '', part)
            element = re.sub(r'\.[\w-]+', '', element)
            element = re.sub(r'\[[\w\-=~|^$*"\':\s]+\]', '', element)
            element = re.sub(r':[\w-]+(?:\([^)]*\))?', '', element)
            element = element.strip()

            # If something remains and it's not a combinator, it's an element
            if element and element not in ['>', '+', '~', ',']:
                # Check if it looks like an element name
                if re.match(r'^[a-zA-Z][\w-]*', element):
                    count += 1

        return count

    def format_specificity(self, spec: Tuple[int, int, int, int]) -> str:
        """Format specificity as readable string."""
        return f"{spec[0]},{spec[1]},{spec[2]},{spec[3]}"

    def is_high_specificity(self, spec: Tuple[int, int, int, int]) -> bool:
        """Check if specificity exceeds threshold."""
        return spec > self.threshold

    def analyze_selector(self, selector: str) -> Dict:
        """Analyze a selector and return detailed results."""
        spec = self.calculate(selector)
        return {
            'selector': selector,
            'specificity': self.format_specificity(spec),
            'specificity_tuple': spec,
            'is_high': self.is_high_specificity(spec),
            'threshold': self.format_specificity(self.threshold)
        }


class CSSFileAnalyzer:
    """Analyze CSS files for specificity issues."""

    def __init__(self, calculator: CSSSpecificityCalculator):
        self.calculator = calculator

    def extract_selectors(self, css_content: str) -> List[str]:
        """Extract all selectors from CSS content."""
        selectors = []

        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

        # Remove @media, @keyframes, etc. content but keep selectors inside
        # Simple extraction: find everything before {
        matches = re.findall(r'([^{}]+)\{', css_content)

        for match in matches:
            # Skip @rules
            if match.strip().startswith('@'):
                continue

            # Split by comma for multiple selectors
            parts = match.split(',')
            for part in parts:
                selector = part.strip()
                if selector and not selector.startswith('@'):
                    selectors.append(selector)

        return selectors

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a CSS file and return results."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"Failed to read file: {e}"}

        selectors = self.extract_selectors(content)
        results = []
        high_specificity_count = 0

        for selector in selectors:
            analysis = self.calculator.analyze_selector(selector)
            results.append(analysis)
            if analysis['is_high']:
                high_specificity_count += 1

        return {
            'file': str(file_path),
            'total_selectors': len(selectors),
            'high_specificity_count': high_specificity_count,
            'threshold': self.calculator.format_specificity(self.calculator.threshold),
            'selectors': results
        }


def parse_threshold(threshold_str: str) -> Tuple[int, int, int, int]:
    """Parse threshold string like '0,1,3,3' into tuple."""
    try:
        parts = [int(x.strip()) for x in threshold_str.split(',')]
        if len(parts) != 4:
            raise ValueError("Threshold must have 4 values")
        return tuple(parts)
    except Exception as e:
        print(f"Error: Invalid threshold format. Use '0,1,3,3' format. ({e})")
        sys.exit(1)


def print_results(analysis: Dict, format_type: str = 'text'):
    """Print analysis results in specified format."""
    if format_type == 'json':
        print(json.dumps(analysis, indent=2))
        return

    if 'error' in analysis:
        print(f"Error: {analysis['error']}")
        return

    print(f"\nCSS Specificity Analysis: {analysis['file']}")
    print("=" * 70)
    print(f"Total selectors: {analysis['total_selectors']}")
    print(f"High specificity: {analysis['high_specificity_count']}")
    print(f"Threshold: {analysis['threshold']}")
    print()

    if analysis['high_specificity_count'] > 0:
        print("⚠️  High Specificity Selectors:")
        print("-" * 70)
        for item in analysis['selectors']:
            if item['is_high']:
                print(f"  {item['specificity']:12} | {item['selector']}")
        print()

    print("All Selectors:")
    print("-" * 70)
    for item in analysis['selectors']:
        marker = "⚠️ " if item['is_high'] else "✓ "
        print(f"{marker} {item['specificity']:12} | {item['selector']}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CSS Specificity Checker - Analyze CSS selector specificity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s styles.css
  %(prog)s --selector "#nav .menu li a"
  %(prog)s styles.css --threshold "0,2,4,4"
  %(prog)s styles.css --format json
        """
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='CSS file to analyze'
    )
    parser.add_argument(
        '--selector',
        help='Analyze a single selector'
    )
    parser.add_argument(
        '--threshold',
        default='0,1,3,3',
        help='Specificity threshold (default: 0,1,3,3 for BEM-style CSS)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Parse threshold
    threshold = parse_threshold(args.threshold)
    calculator = CSSSpecificityCalculator(threshold)

    # Single selector mode
    if args.selector:
        analysis = calculator.analyze_selector(args.selector)
        if args.format == 'json':
            print(json.dumps(analysis, indent=2))
        else:
            print(f"\nSelector: {analysis['selector']}")
            print(f"Specificity: {analysis['specificity']}")
            print(f"Threshold: {analysis['threshold']}")
            print(f"Status: {'⚠️  HIGH' if analysis['is_high'] else '✓ OK'}")
        return

    # File analysis mode
    if not args.file:
        parser.print_help()
        return

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)

    analyzer = CSSFileAnalyzer(calculator)
    analysis = analyzer.analyze_file(file_path)
    print_results(analysis, args.format)

    # Exit with error code if high specificity found
    if analysis.get('high_specificity_count', 0) > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
