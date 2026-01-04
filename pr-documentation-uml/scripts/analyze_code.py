#!/usr/bin/env python3
"""
Python Code Static Analysis Tool

Extracts accurate code structure information including:
- Classes (names, inheritance, methods, attributes)
- Functions (names, parameters, return types)
- Imports and dependencies
- Type annotations
- Decorators

Usage:
    python analyze_code.py <file_path> [--format json|text]
    python analyze_code.py file1.py file2.py
"""

from __future__ import annotations

import ast
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Parameter:
    """Function/method parameter information."""
    name: str
    annotation: str | None = None
    default: str | None = None


@dataclass
class Method:
    """Class method information."""
    name: str
    parameters: list[Parameter] = field(default_factory=list)
    return_type: str | None = None
    decorators: list[str] = field(default_factory=list)
    is_static: bool = False
    is_class_method: bool = False
    is_property: bool = False
    docstring: str | None = None


@dataclass
class Attribute:
    """Class attribute information."""
    name: str
    annotation: str | None = None
    value: str | None = None


@dataclass
class ClassInfo:
    """Class definition information."""
    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[Method] = field(default_factory=list)
    attributes: list[Attribute] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    docstring: str | None = None


@dataclass
class Function:
    """Standalone function information."""
    name: str
    parameters: list[Parameter] = field(default_factory=list)
    return_type: str | None = None
    decorators: list[str] = field(default_factory=list)
    docstring: str | None = None


@dataclass
class Import:
    """Import statement information."""
    module: str
    names: list[str] = field(default_factory=list)
    alias: str | None = None
    is_from_import: bool = False


@dataclass
class FileAnalysis:
    """Complete file analysis result."""
    file_path: str
    imports: list[Import] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)


class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor for extracting code structure."""

    def __init__(self):
        self.imports: list[Import] = []
        self.classes: list[ClassInfo] = []
        self.functions: list[Function] = []
        self._current_class: ClassInfo | None = None

    def visit_Import(self, node: ast.Import):
        """Handle 'import module' statements."""
        for alias in node.names:
            self.imports.append(Import(
                module=alias.name,
                alias=alias.asname,
                is_from_import=False
            ))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Handle 'from module import name' statements."""
        module = node.module or ""
        names = [alias.name for alias in node.names]
        self.imports.append(Import(
            module=module,
            names=names,
            is_from_import=True
        ))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Extract class definition."""
        # Save previous class context
        prev_class = self._current_class

        # Extract base classes
        bases = [self._get_name(base) for base in node.bases]

        # Extract decorators
        decorators = [self._get_name(dec) for dec in node.decorator_list]

        # Get docstring
        docstring = ast.get_docstring(node)

        # Create class info
        class_info = ClassInfo(
            name=node.name,
            bases=bases,
            decorators=decorators,
            docstring=docstring
        )

        self._current_class = class_info

        # Visit class body to extract methods and attributes
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method = self._extract_function(item, is_method=True)
                class_info.methods.append(method)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # Class attribute with type annotation
                attr = Attribute(
                    name=item.target.id,
                    annotation=self._get_annotation(item.annotation),
                    value=self._get_value(item.value) if item.value else None
                )
                class_info.attributes.append(attr)
            elif isinstance(item, ast.Assign):
                # Class attribute without annotation
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attr = Attribute(
                            name=target.id,
                            value=self._get_value(item.value)
                        )
                        class_info.attributes.append(attr)

        self.classes.append(class_info)

        # Restore class context
        self._current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Extract function definition (standalone, not method)."""
        if self._current_class is None:
            # This is a standalone function
            func = self._extract_function(node, is_method=False)
            self.functions.append(func)
        # If inside a class, it's already handled by visit_ClassDef

    def _extract_function(self, node: ast.FunctionDef, is_method: bool) -> Method | Function:
        """Extract function/method information."""
        # Extract parameters
        params = []
        args = node.args

        # Regular arguments
        for i, arg in enumerate(args.args):
            # Skip 'self' and 'cls'
            if is_method and i == 0 and arg.arg in ('self', 'cls'):
                continue

            param = Parameter(
                name=arg.arg,
                annotation=self._get_annotation(arg.annotation)
            )

            # Check for default value
            defaults_offset = len(args.args) - len(args.defaults)
            if i >= defaults_offset:
                default_index = i - defaults_offset
                param.default = self._get_value(args.defaults[default_index])

            params.append(param)

        # Extract return type
        return_type = self._get_annotation(node.returns)

        # Extract decorators
        decorators = [self._get_name(dec) for dec in node.decorator_list]

        # Get docstring
        docstring = ast.get_docstring(node)

        if is_method:
            # Detect special method types
            is_static = 'staticmethod' in decorators
            is_class_method = 'classmethod' in decorators
            is_property = 'property' in decorators or any('property' in d for d in decorators)

            return Method(
                name=node.name,
                parameters=params,
                return_type=return_type,
                decorators=decorators,
                is_static=is_static,
                is_class_method=is_class_method,
                is_property=is_property,
                docstring=docstring
            )
        else:
            return Function(
                name=node.name,
                parameters=params,
                return_type=return_type,
                decorators=decorators,
                docstring=docstring
            )

    def _get_name(self, node: ast.expr) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_name(node.value)
            return f"{value}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        elif isinstance(node, ast.Subscript):
            value = self._get_name(node.value)
            slice_str = self._get_annotation(node.slice)
            return f"{value}[{slice_str}]"
        else:
            return ast.unparse(node)

    def _get_annotation(self, node: ast.expr | None) -> str | None:
        """Extract type annotation as string."""
        if node is None:
            return None
        return ast.unparse(node)

    def _get_value(self, node: ast.expr | None) -> str | None:
        """Extract value as string."""
        if node is None:
            return None
        try:
            return ast.unparse(node)
        except Exception:
            return repr(node)


def analyze_file(file_path: Path) -> FileAnalysis:
    """Analyze a Python file and extract code structure."""
    try:
        source_code = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return FileAnalysis(file_path=str(file_path))

    try:
        tree = ast.parse(source_code, filename=str(file_path))
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}", file=sys.stderr)
        return FileAnalysis(file_path=str(file_path))

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return FileAnalysis(
        file_path=str(file_path),
        imports=analyzer.imports,
        classes=analyzer.classes,
        functions=analyzer.functions
    )


def format_text(analysis: FileAnalysis) -> str:
    """Format analysis result as human-readable text."""
    lines = []
    lines.append(f"File: {analysis.file_path}")
    lines.append("")

    # Imports
    if analysis.imports:
        lines.append("Imports:")
        for imp in analysis.imports:
            if imp.is_from_import:
                names_str = ", ".join(imp.names)
                lines.append(f"  - from {imp.module} import {names_str}")
            else:
                alias_str = f" as {imp.alias}" if imp.alias else ""
                lines.append(f"  - import {imp.module}{alias_str}")
        lines.append("")

    # Classes
    if analysis.classes:
        lines.append("Classes:")
        for cls in analysis.classes:
            bases_str = f"({', '.join(cls.bases)})" if cls.bases else ""
            lines.append(f"  {cls.name}{bases_str}")

            if cls.decorators:
                lines.append(f"    Decorators: {', '.join(cls.decorators)}")

            if cls.attributes:
                lines.append("    Attributes:")
                for attr in cls.attributes:
                    type_str = f": {attr.annotation}" if attr.annotation else ""
                    value_str = f" = {attr.value}" if attr.value else ""
                    lines.append(f"      - {attr.name}{type_str}{value_str}")

            if cls.methods:
                lines.append("    Methods:")
                for method in cls.methods:
                    # Method signature
                    params_str = ", ".join(
                        f"{p.name}: {p.annotation}" if p.annotation else p.name
                        for p in method.parameters
                    )
                    return_str = f" -> {method.return_type}" if method.return_type else ""

                    # Method type prefix
                    prefix = "+"
                    if method.is_property:
                        prefix = "@property"
                    elif method.is_static:
                        prefix = "@staticmethod"
                    elif method.is_class_method:
                        prefix = "@classmethod"
                    elif method.name.startswith("_") and not method.name.startswith("__"):
                        prefix = "-"

                    lines.append(f"      {prefix} {method.name}({params_str}){return_str}")

            lines.append("")

    # Functions
    if analysis.functions:
        lines.append("Functions:")
        for func in analysis.functions:
            params_str = ", ".join(
                f"{p.name}: {p.annotation}" if p.annotation else p.name
                for p in func.parameters
            )
            return_str = f" -> {func.return_type}" if func.return_type else ""
            lines.append(f"  {func.name}({params_str}){return_str}")

            if func.decorators:
                lines.append(f"    Decorators: {', '.join(func.decorators)}")

        lines.append("")

    return "\n".join(lines)


def format_json(analysis: FileAnalysis) -> str:
    """Format analysis result as JSON."""
    return json.dumps(asdict(analysis), indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python code structure for accurate UML generation"
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Python file(s) to analyze"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()

    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            continue

        if not file_path.suffix == ".py":
            print(f"Warning: Skipping non-Python file: {file_path}", file=sys.stderr)
            continue

        analysis = analyze_file(file_path)

        if args.format == "json":
            print(format_json(analysis))
        else:
            print(format_text(analysis))

        # Add separator between multiple files
        if len(args.files) > 1:
            print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()

