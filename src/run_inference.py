#!/usr/bin/env python3
"""
run_inference.py — Group 07 OWL Reasoning + SPARQL Query Script
================================================================
Usage:
    python3 src/run_inference.py

This script:
1. Loads the group ontology and the course ontology (course-affordance.ttl).
2. Runs OWL RL / RDFS reasoning via owlrl to materialise inferred triples.
3. Exports the full inferred graph as ontology/inferred-results.ttl.

Dependencies:
    pip install rdflib owlrl
"""

import sys
from pathlib import Path

try:
    import owlrl
    from rdflib import OWL, RDF, RDFS, Graph, Namespace
    from rdflib.namespace import SKOS
except ImportError:
    sys.exit("ERROR: Missing dependencies. Run:  pip install rdflib owlrl")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # hw5/

ONTOLOGY_DIR = BASE / "ontology"
IMPORTS_DIR = ONTOLOGY_DIR / "imports"
QUERIES_DIR = BASE / "queries"
RESULTS_DIR = BASE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

GROUP_ONTOLOGY = ONTOLOGY_DIR / "group-ontology.ttl"
COURSE_ONTOLOGY = IMPORTS_DIR / "course-affordance.ttl"
INFERRED_OUT = ONTOLOGY_DIR / "inferred-results.ttl"

CAP = Namespace("https://hcis.io/ontology/aicapstone/2026/")
G07 = Namespace("https://hcis.io/ontology/aicapstone/2026/group07/")

# ---------------------------------------------------------------------------
# Step 1 — Load ontologies
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 1: Loading ontologies")
print("=" * 60)

g = Graph()
g.bind("cap", CAP)
g.bind("g07", G07)

g.parse(COURSE_ONTOLOGY, format="turtle")
print(f"  Loaded course ontology  : {COURSE_ONTOLOGY.name}  ({len(g)} triples so far)")

g.parse(GROUP_ONTOLOGY, format="turtle")
print(f"  Loaded group ontology   : {GROUP_ONTOLOGY.name}   ({len(g)} triples so far)")

# ---------------------------------------------------------------------------
# Step 2 — Run OWL RL reasoning
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("Step 2: Running OWL RL reasoning (owlrl)")
print("=" * 60)

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
print(f"  Triples after reasoning : {len(g)}")



# ---------------------------------------------------------------------------
# Step 3 — Export inferred graph
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("Step 3: Exporting inferred graph")
print("=" * 60)

g.serialize(destination=str(INFERRED_OUT), format="turtle")
print(f"  Saved → {INFERRED_OUT}")

print("Done. Inferred graph exported successfully.")
