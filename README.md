# AI Capstone 2026 - Homework 5: Ontology-based Semantic Grounding

**Group 07** | National Yang Ming Chiao Tung University (NYCU) - Computer Science Dept.

## 1. Project Title & Group Members
* **Project Title:** Group 07 Semantic Affordance Grounding Artifact
* **Members:**
  * 112550169 潘仰祐 | 112550095 葉羽宸 | 112550141 王佳欣
  * 112550194 徐凡懿 | 113550173 曹育誠 | 113550050 陳建霖

## 2. Selected Task(s)
Our group modeled the environment objects and semantic grounding for all three baseline tasks defined in the course project:
1. **Cup Stacking:** Incorporating target cups and reference cups.
2. **Cutlery Arrangement:** Incorporating manipulation targets (knife, fork) and a placement reference (plate).
3. **Toy Block Collection:** Incorporating collectable objects (toy blocks) and a container target (basket).

## 3. Ontology Design & Advanced Features
Our ontology (`group-ontology.ttl`) grounds perceived simulation objects into queryable semantic entities. The design imports the core course vocabulary (`course-affordance.ttl`) and extends it with specific instances (`g07:`). 

**Advanced Extension (Gripper Constraints):** Beyond the baseline requirements, we introduced hardware-specific constraints. We defined a `parallelGripper01` as an `EndEffector` with a specific `hasApproxWidth` ("0.08"). Objects explicitly state their manipulability via `canBeManipulatedBy` and their own `hasApproxWidth`, correlating the physical dimensions of the gripper with the graspable targets. We also successfully generated automated documentation using **Widoco**, which is available in the `docs/` directory.

## 4. Modeled Objects & Affordances Table
| Instance URI (`g07:`) | Object Class | Asserted Affordance(s) | Task Role |
| :--- | :--- | :--- | :--- |
| `blueCup01` | `cap:Cup` | `cap:GraspingAffordance`, `cap:StackabilityAffordance` | `cap:TargetObject` |
| `pinkCup01` | `cap:Cup` | `cap:GraspingAffordance`, `cap:StackabilityAffordance` | `cap:TargetObject` |
| `knife01` | `cap:Knife` | `cap:GraspingAffordance` | `cap:TargetObject` |
| `fork01` | `cap:Fork` | `cap:GraspingAffordance` | `cap:TargetObject` |
| `plate01` | `cap:Plate` | `cap:SupportAffordance` | `cap:ReferenceObject` |
| `toyBlock01` | `cap:ToyBlock` | `cap:GraspingAffordance` | `cap:CollectableObject` |
| `toyBlock02` | `cap:ToyBlock` | `cap:GraspingAffordance` | `cap:CollectableObject` |
| `basket01` | `cap:Basket` | `cap:ContainmentAffordance` | `cap:ContainerTarget` |

## 5. Namespace Policy
* **`cap:`** (`https://hcis.io/ontology/aicapstone/2026/`): Course vocabulary for base classes and properties.
* **`g07:`** (`https://hcis.io/ontology/aicapstone/2026/group07/`): Group-specific environment instances and metadata.

## 6. Instructions for Running the Query
To generate the inferred graph and run the SPARQL queries, execute the Python inference script:

```bash
python3 src/run_inference.py
```

## 7. Expected Query Output
When executing `graspable_objects.rq` on the inferred graph, the query will return the following 6 distinct objects. Note that `plate01` and `basket01` are correctly excluded as they do not possess a grasping affordance.

| obj | label | color | objectLabel | role |
| :--- | :--- | :--- | :--- | :--- |
| g07:blueCup01 | blue cup 01 | blue | blue_cup | cap:TargetObject |
| g07:fork01 | fork 01 | silver | cutlery_fork | cap:TargetObject |
| g07:knife01 | knife 01 | silver | cutlery_knife | cap:TargetObject |
| g07:pinkCup01 | pink cup 01 | pink | pink_cup | cap:TargetObject |
| g07:toyBlock01 | toy block 01 | red | toy_block_red | cap:CollectableObject |
| g07:toyBlock02 | toy block 02 | blue | toy_block_blue | cap:CollectableObject |

## 8. Explanation of Inference vs. Assertion
We did not manually assert `g07:blueCup01` as a `cap:GraspableObject`. Instead, `cap:GraspableObject` is defined conceptually using an `owl:equivalentClass` combined with an `owl:intersectionOf` axiom.

The Description Logic pattern is:
`cap:GraspableObject ≡ cap:PhysicalObject ⊓ ∃cap:hasAffordance.cap:GraspingAffordance`

Since `blueCup01` is asserted as a `cap:Cup` (which is a subclass of `cap:PhysicalObject`) and is asserted to have a `cap:GraspingAffordance`, the OWL reasoner dynamically classifies it under `cap:GraspableObject` during the reasoning phase.

## 9. Generation of inferred-results.ttl
The file `ontology/inferred-results.ttl` contains the full graph including all implicit triples explicitly materialized. It is generated automatically by running `src/run_inference.py`. The script loads the original `group-ontology.ttl` (along with its imports) and uses the `owlrl` Python package (an OWL 2 RL Reasoner) to expand the graph. The reasoner evaluates the axioms and exports the newly classified individuals and triples into this new `.ttl` file.

## 10. Repository Links
* **Repository:** [NYCU-CS-AI-Capstone-2026-Group7/semantic-affordance-grounding](https://github.com/NYCU-CS-AI-Capstone-2026-Group7/semantic-affordance-grounding)
* **Ontology File:** [ontology/group-ontology.ttl](ontology/group-ontology.ttl)
* **Query File:** [queries/graspable_objects.rq](queries/graspable_objects.rq)
* **Source Code:** [src/run_inference.py](src/run_inference.py)
* **Result Files:** 
  * [ontology/inferred-results.ttl](ontology/inferred-results.ttl)
  * [results/graspable_objects_output.txt](results/graspable_objects_output.txt)

---

## Implementation Details & Workflow

### Repository Structure
```
.
├── ontology/
│   ├── group-ontology.ttl       # Our group's specific instances and assertions
│   ├── shapes.ttl               # SHACL validation shapes
│   ├── inferred-results.ttl     # The generated ontology after reasoning
│   └── imports/
│       └── course-affordance.ttl # Base course vocabulary
├── queries/
│   └── graspable_objects.rq     # SPARQL query for extracting graspable objects
├── results/                     # Output results (query outputs, SHACL reports)
├── src/
│   ├── run_inference.py         # Main script for reasoning and executing SPARQL
│   └── validate_shacl.py        # Script for validating the graph using SHACL
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Imported Resources
Our ontology imports the course base vocabulary:
* `course-affordance.ttl` is imported to provide the foundational classes (`cap:PhysicalObject`, `cap:Affordance`, etc.) and object properties (`cap:hasAffordance`, `cap:hasTaskRole`, etc.). This allows us to instantiate objects like `cap:Cup` and attach affordances while maintaining consistency with the assignment specifications.

### Reasoning Workflow
1. **Load Ontologies:** Load both `course-affordance.ttl` and `group-ontology.ttl` into an RDF graph using `rdflib`.
2. **OWL RL Reasoning:** Use `owlrl.DeductiveClosure` in `run_inference.py` to materialize inferred triples based on OWL semantics.
3. **Export:** Serialize the fully expanded graph to `ontology/inferred-results.ttl`.
4. **SPARQL Query:** Execute `graspable_objects.rq` on the materialized graph to extract our target graspable objects and save the formatted output to `results/`.
5. **SHACL Validation:** We validate the inferred graph against constraints defined in `shapes.ttl` using `validate_shacl.py` to ensure correctness (e.g., confirming all objects have valid properties).

### SHACL Validation
We utilize SHACL (Shapes Constraint Language) to validate the integrity of our knowledge graph. The shapes are defined in `ontology/shapes.ttl`.
To execute the SHACL validation independently, run:
```bash
python3 src/validate_shacl.py
```
This validates the generated `ontology/inferred-results.ttl` graph against the shape definitions, ensuring that all inferred individuals conform to our expected data model.