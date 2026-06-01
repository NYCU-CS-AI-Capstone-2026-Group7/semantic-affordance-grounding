#!/usr/bin/env python3
"""
validate_shacl.py — Group 07 SHACL Validation Script
=====================================================
Usage:
    python3 src/validate_shacl.py

This script:
1. Loads the inferred results graph (ontology/inferred-results.ttl).
2. Loads the SHACL shapes (ontology/shapes.ttl).
3. Validates the data graph against the shapes using pyshacl.
4. Outputs the report to results/shacl_report.txt.
"""

import sys
from pathlib import Path

try:
    from rdflib import Graph
    from pyshacl import validate
except ImportError:
    sys.exit("ERROR: Missing dependencies. Run: pip install rdflib pyshacl")

BASE = Path(__file__).resolve().parent.parent

ONTOLOGY_DIR = BASE / "ontology"
RESULTS_DIR = BASE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

INFERRED_FILE = ONTOLOGY_DIR / "inferred-results.ttl"
SHAPES_FILE = ONTOLOGY_DIR / "shapes.ttl"

if not INFERRED_FILE.exists():
    sys.exit(f"ERROR: Inferred file not found at {INFERRED_FILE}. Run run_inference.py first.")

if not SHAPES_FILE.exists():
    sys.exit(f"ERROR: SHACL shapes not found at {SHAPES_FILE}.")

print("=" * 60)
print("SHACL validation of the inferred graph")
print("=" * 60)

print(f"Loading data graph: {INFERRED_FILE.name}")
data_graph = Graph()
data_graph.parse(INFERRED_FILE, format="turtle")

print(f"Loading shape graph: {SHAPES_FILE.name}")
shacl_graph = Graph()
shacl_graph.parse(SHAPES_FILE, format="turtle")

print("Validating...")
conforms, results_graph, results_text = validate(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    inference="none",
    advanced=True,
    serialize_report_graph=True,
)

report_file = RESULTS_DIR / "shacl_report.txt"
report_file.write_text(str(results_text))

if conforms:
    print("  SHACL validation: CONFORMS")
else:
    print(f"  SHACL validation: FAIL — report saved to {report_file}")
    print(results_text)
    sys.exit(1)
