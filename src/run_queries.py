#!/usr/bin/env python3
"""
run_queries.py — Group 07 SPARQL Query Execution Script
========================================================
Usage:
    python3 src/run_queries.py

This script:
1. Loads the inferred results graph (ontology/inferred-results.ttl).
2. Executes graspable_objects.rq and task_objects.rq.
3. Formats and saves the results into the results/ directory.
"""

import sys
from pathlib import Path

try:
    from rdflib import Graph
except ImportError:
    sys.exit("ERROR: Missing dependencies. Run: pip install rdflib")

BASE = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = BASE / "ontology"
QUERIES_DIR = BASE / "queries"
RESULTS_DIR = BASE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

INFERRED_OUT = ONTOLOGY_DIR / "inferred-results.ttl"

if not INFERRED_OUT.exists():
    sys.exit(f"ERROR: {INFERRED_OUT} not found. Please run src/run_inference.py first.")

print("=" * 60)
print(f"Loading inferred graph: {INFERRED_OUT.name}")
print("=" * 60)
g = Graph()
g.parse(INFERRED_OUT, format="turtle")

# ---------------------------------------------------------------------------
# Query 1: graspable_objects.rq
# ---------------------------------------------------------------------------
def run_graspable_objects():
    print("\n" + "=" * 60)
    print("Executing Query: graspable_objects.rq")
    print("=" * 60)
    query_file = QUERIES_DIR / "graspable_objects.rq"
    if not query_file.exists():
        print(f"File not found: {query_file}")
        return

    QUERY = query_file.read_text()
    # Prepend missing prefix for rdfs (rdflib SPARQL needs it explicitly)
    QUERY = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + QUERY
    results = g.query(QUERY)

    output_lines = []
    output_lines.append(f"{'obj':<55} {'label':<25} {'color':<10} {'objectLabel':<22} {'role'}")
    output_lines.append("-" * 140)

    count = 0
    for row in results:
        count += 1
        obj = str(row.obj).replace("https://hcis.io/ontology/aicapstone/2026/group07/", "g07:")
        label = str(row.label) if row.label else ""
        color = str(row.color) if row.color else ""
        olbl = str(row.objectLabel) if row.objectLabel else ""
        role = str(row.role).replace("https://hcis.io/ontology/aicapstone/2026/", "cap:") if row.role else ""
        output_lines.append(f"{obj:<55} {label:<25} {color:<10} {olbl:<22} {role}")

    output_text = "\n".join(output_lines)
    print(output_text)
    print("-" * 140)
    print(f"Summary: {count} object(s) inferred as cap:GraspableObject")

    out_file = RESULTS_DIR / "graspable_objects_output.txt"
    out_file.write_text(output_text + "\n")
    print(f"  Saved → {out_file}")

# ---------------------------------------------------------------------------
# Query 2: task_objects.rq
# ---------------------------------------------------------------------------
def run_task_objects():
    print("\n" + "=" * 60)
    print("Executing Query: task_objects.rq")
    print("=" * 60)
    query_file = QUERIES_DIR / "task_objects.rq"
    if not query_file.exists():
        print(f"File not found: {query_file}")
        return

    QUERY = query_file.read_text()
    results = g.query(QUERY)
    
    output_lines = []
    output_lines.append(f"{'obj':<35} {'type':<40} {'label':<20} {'role':<25} {'affordance'}")
    output_lines.append("-" * 140)
    
    for row in results:
        obj = str(row.obj).replace("https://hcis.io/ontology/aicapstone/2026/group07/", "g07:")
        typ = str(row.type).replace("https://hcis.io/ontology/aicapstone/2026/", "cap:")
        label = str(row.label) if row.label else ""
        role = str(row.role).replace("https://hcis.io/ontology/aicapstone/2026/", "cap:") if row.role else ""
        aff = str(row.affordance).replace("https://hcis.io/ontology/aicapstone/2026/", "cap:") if row.affordance else ""
        output_lines.append(f"{obj:<35} {typ:<40} {label:<20} {role:<25} {aff}")

    output_text = "\n".join(output_lines)
    print(output_text)

    out_file = RESULTS_DIR / "task_objects_output.txt"
    out_file.write_text(output_text + "\n")
    print(f"\n  Saved → {out_file}\n")

if __name__ == "__main__":
    run_graspable_objects()
    run_task_objects()
    print("Done. All query results exported.")
