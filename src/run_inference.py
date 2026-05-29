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
4. Executes the SPARQL queries from queries/ and saves results to results/.

Dependencies:
    pip install rdflib owlrl
"""

import sys
from pathlib import Path

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL
    from rdflib.namespace import SKOS
    import owlrl
except ImportError:
    sys.exit("ERROR: Missing dependencies. Run:  pip install rdflib owlrl")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent  # hw5/

ONTOLOGY_DIR  = BASE / "ontology"
IMPORTS_DIR   = ONTOLOGY_DIR / "imports"
QUERIES_DIR   = BASE / "queries"
RESULTS_DIR   = BASE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

GROUP_ONTOLOGY  = ONTOLOGY_DIR / "group-ontology.ttl"
COURSE_ONTOLOGY = IMPORTS_DIR  / "course-affordance.ttl"
INFERRED_OUT    = ONTOLOGY_DIR / "inferred-results.ttl"

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

# ---------------------------------------------------------------------------
# Step 4 — SPARQL: graspable objects
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("Step 4: Querying inferred GraspableObject individuals")
print("=" * 60)

QUERY_GRASPABLE = (QUERIES_DIR / "graspable_objects.rq").read_text()

# Prepend missing prefix for rdfs (rdflib SPARQL needs it explicitly)
QUERY_GRASPABLE = (
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + QUERY_GRASPABLE
)

results = g.query(QUERY_GRASPABLE)

output_lines = []
output_lines.append(f"{'obj':<55} {'label':<25} {'color':<10} {'objectLabel':<22} {'role'}")
output_lines.append("-" * 140)

for row in results:
    obj   = str(row.obj).replace("https://hcis.io/ontology/aicapstone/2026/group07/", "g07:")
    label = str(row.label)       if row.label       else ""
    color = str(row.color)       if row.color       else ""
    olbl  = str(row.objectLabel) if row.objectLabel else ""
    role  = str(row.role).replace("https://hcis.io/ontology/aicapstone/2026/", "cap:") if row.role else ""
    output_lines.append(f"{obj:<55} {label:<25} {color:<10} {olbl:<22} {role}")

output_text = "\n".join(output_lines)
print(output_text)

out_file = RESULTS_DIR / "graspable_objects_output.txt"
out_file.write_text(output_text + "\n")
print(f"\n  Saved → {out_file}")

# ---------------------------------------------------------------------------
# Step 5 — Summary
# ---------------------------------------------------------------------------
graspable_uris = [str(row.obj) for row in g.query(QUERY_GRASPABLE)]
print()
print("=" * 60)
print(f"Summary: {len(graspable_uris)} object(s) inferred as cap:GraspableObject")
print("=" * 60)
for uri in sorted(graspable_uris):
    short = uri.replace("https://hcis.io/ontology/aicapstone/2026/group07/", "g07:")
    print(f"  ✓ {short}")

print()
print("Done. All outputs written successfully.")
