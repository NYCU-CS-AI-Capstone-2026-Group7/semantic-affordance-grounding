# AI Capstone 2026 - 作業五：基於本體論的語意落地 (Ontology-based Semantic Grounding)

**第 7 組 (Group 07)** | 國立陽明交通大學 (NYCU) - 資訊工程學系

---

## 1. 專案標題與小組成員

**專案標題：** Group 07 語意可負性落地產出 (Group 07 Semantic Affordance Grounding Artifact)

| 學號 | 姓名 | 貢獻 |
| :--- | :--- | :--- |
| 112550169 | 潘仰祐 | — |
| 112550095 | 葉羽宸 | — |
| 112550141 | 王佳欣 | 程式碼修改；報告審查 |
| 112550194 | 徐凡懿 | 程式碼修改；報告審查 |
| 113550173 | 曹育誠 | — |
| 113550050 | 陳建霖 | SHACL 與查詢程式碼；README 審查 |

---

## 2. 選擇的任務

我們小組為課程專案中定義的所有三個基準任務建模了環境物件與語意落地：

1. **疊杯 (Cup Stacking)**：包含目標杯子（target cups）與參考杯子（reference cups）。
2. **餐具排列 (Cutlery Arrangement)**：包含操作目標（刀、叉）與放置參考（盤子）。
3. **玩具積木收集 (Toy Block Collection)**：包含可收集物件（玩具積木）與容器目標（籃子）。

---

## 3. 本體論設計與進階功能

我們的本體論（`group-ontology.ttl`）將感知到的模擬物件落地為可查詢的語意實體。此設計導入了核心課程詞彙（`course-affordance.ttl`）並使用小組特定的實體（`g07:`）對其進行擴充。

**進階擴充（夾爪限制）：** 除了基準要求之外，我們還引入了硬體特定的限制。我們定義了 `parallelGripper01` 作為一個 `EndEffector`，並具備特定的 `hasApproxWidth`（約略寬度 "0.08"）。物件透過 `canBeManipulatedBy` 以及它們自身的 `hasApproxWidth` 來明確聲明其可操作性，從而將夾爪的物理尺寸與可抓取的目標物件進行關聯。

---

## 4. 建模物件與可負性對照表

| 實體 URI (`g07:`) | 物件類別 | 宣告的可負性 (Asserted Affordances) | 任務角色 |
| :--- | :--- | :--- | :--- |
| `blueCup01` | `cap:Cup` | `cap:GraspingAffordance`, `cap:StackabilityAffordance` | `cap:TargetObject` |
| `pinkCup01` | `cap:Cup` | `cap:GraspingAffordance`, `cap:StackabilityAffordance` | `cap:TargetObject` |
| `knife01` | `cap:Knife` | `cap:GraspingAffordance` | `cap:TargetObject` |
| `fork01` | `cap:Fork` | `cap:GraspingAffordance` | `cap:TargetObject` |
| `plate01` | `cap:Plate` | `cap:SupportAffordance` | `cap:ReferenceObject` |
| `toyBlock01` | `cap:ToyBlock` | `cap:GraspingAffordance` | `cap:CollectableObject` |
| `toyBlock02` | `cap:ToyBlock` | `cap:GraspingAffordance` | `cap:CollectableObject` |
| `basket01` | `cap:Basket` | `cap:ContainmentAffordance` | `cap:ContainerTarget` |

---

## 5. 命名空間規範

* **`cap:`** (`https://hcis.io/ontology/aicapstone/2026/`)：基礎類別和屬性的課程詞彙。
* **`g07:`** (`https://hcis.io/ontology/aicapstone/2026/group07/`)：小組特定的環境實體與元數據。

---

## 6. 查詢運行說明

若要生成推導圖並運行 SPARQL 查詢，請按照以下步驟操作：

1. **運行推理**（生成 `ontology/inferred-results.ttl`）：
   ```bash
   python3 src/run_inference.py
   ```

2. **運行查詢**（執行 `graspable_objects.rq` 和 `task_objects.rq`）：
   ```bash
   python3 src/run_queries.py
   ```

---

## 7. 預期查詢輸出

在推導圖（inferred graph）上執行 `graspable_objects.rq` 時，查詢將返回以下 6 個不同的物件。請注意，`plate01` 和 `basket01` 已被正確排除，因為它們不具備抓取可負性（grasping affordance）。

| obj | label | color | objectLabel | role |
| :--- | :--- | :--- | :--- | :--- |
| `g07:blueCup01` | blue cup 01 | blue | blue_cup | `cap:TargetObject` |
| `g07:fork01` | fork 01 | silver | cutlery_fork | `cap:TargetObject` |
| `g07:knife01` | knife 01 | silver | cutlery_knife | `cap:TargetObject` |
| `g07:pinkCup01` | pink cup 01 | pink | pink_cup | `cap:TargetObject` |
| `g07:toyBlock01` | toy block 01 | red | toy_block_red | `cap:CollectableObject` |
| `g07:toyBlock02` | toy block 02 | blue | toy_block_blue | `cap:CollectableObject` |

---

## 8. 推理 vs. 宣告說明

我們並未手動將 `g07:blueCup01` 宣告為 `cap:GraspableObject`。相反地，`cap:GraspableObject` 是在概念上使用 `owl:equivalentClass` 結合 `owl:intersectionOf` 公理來定義的。

其描述邏輯（Description Logic）模式為：

$$cap:GraspableObject \equiv cap:PhysicalObject \sqcap \exists cap:hasAffordance.cap:GraspingAffordance$$

由於 `blueCup01` 被宣告為 `cap:Cup`（其為 `cap:PhysicalObject` 的子類別），且被宣告具備 `cap:GraspingAffordance`，因此 OWL 推理器會在推理階段動態地將其分類到 `cap:GraspableObject` 之下。

---

## 9. inferred-results.ttl 的生成

檔案 `ontology/inferred-results.ttl` 包含了完整的圖，其中包括所有被明確實體化（materialized）的隱式三元組（implicit triples）。它是藉由執行 `src/run_inference.py` 自動生成的。

該腳本載入原始的 `group-ontology.ttl`（連同其導入的內容），並使用 `owlrl` Python 套件（一個 OWL 2 RL 推理器）來擴展該圖。推理器評估這些公理，並將新分類的個體和三元組匯出到此新的 `.ttl` 檔案中。

---

## 10. 儲存庫連結

* **GitHub 儲存庫：** [NYCU-CS-AI-Capstone-2026-Group7/semantic-affordance-grounding](https://github.com/NYCU-CS-AI-Capstone-2026-Group7/semantic-affordance-grounding)
* **本體論檔案：** [ontology/group-ontology.ttl](ontology/group-ontology.ttl)
* **查詢檔案：** [queries/graspable_objects.rq](queries/graspable_objects.rq)
* **原始碼：**
  * [src/run_inference.py](src/run_inference.py)
  * [src/run_queries.py](src/run_queries.py)
* **結果檔案：**
  * [ontology/inferred-results.ttl](ontology/inferred-results.ttl)
  * [results/graspable_objects_output.txt](results/graspable_objects_output.txt)
  * [results/task_objects_output.txt](results/task_objects_output.txt)

---

## 實作細節與工作流 (Implementation Details & Workflow)

### 儲存庫結構 (Repository Structure)

```text
.
├── ontology/
│   ├── group-ontology.ttl       # 我們小組特定的實體與宣告
│   ├── shapes.ttl               # SHACL 驗證形狀 (shapes)
│   ├── inferred-results.ttl     # 推理後生成的本體論
│   └── imports/
│       ├── course-affordance.ttl # 基礎課程詞彙
│       └── course-alignment.ttl # 對齊公理，將課程術語映射至標準頂層本體論 (CORA, SOMA)
├── queries/
│   ├── graspable_objects.rq     # 用於擷取可抓取物件的 SPARQL 查詢
│   └── task_objects.rq          # （選填）用於驗證所有物件及其角色的 SPARQL 查詢
├── results/                     # 輸出結果（查詢輸出、SHACL 報告）
├── src/
│   ├── run_inference.py         # 用於實體化推導圖的腳本
│   ├── run_queries.py           # 用於在推導圖上執行 SPARQL 查詢的腳本
│   └── validate_shacl.py        # 用於使用 SHACL 驗證圖的腳本
├── requirements.txt             # Python 依賴項
└── README.md                    # 本檔案
```

### 導入的資源 (Imported Resources)

我們的本體論導入了課程基礎詞彙：

* `course-affordance.ttl` 被導入以提供基礎類別（`cap:PhysicalObject`、`cap:Affordance` 等）和物件屬性（`cap:hasAffordance`、`cap:hasTaskRole` 等）。這使我們能夠實體化諸如 `cap:Cup` 等物件並附加可負性，同時保持與作業規格書的一致性。

### 推理工作流 (Reasoning Workflow)

1. **載入本體論**：使用 `rdflib` 將 `course-affordance.ttl` 和 `group-ontology.ttl` 載入到 RDF 圖中。
2. **OWL RL 推理**：在 `run_inference.py` 中使用 `owlrl.DeductiveClosure` 根據 OWL 語意實體化推導出的三元組。
3. **匯出**：將完整擴展的圖序列化為 `ontology/inferred-results.ttl`。
4. **SPARQL 查詢**：使用 `run_queries.py` 在實體化的圖上執行查詢（`graspable_objects.rq`、`task_objects.rq`），並將格式化後的輸出儲存至 `results/` 下。
5. **SHACL 驗證**：我們使用 `validate_shacl.py` 根據 `shapes.ttl` 中定義的限制來驗證推導出的圖，以確保其正確性（例如，確認所有物件均具有有效的屬性）。

### SHACL 驗證 (SHACL Validation)

我們利用 SHACL（Shapes Constraint Language，形狀限制語言）來驗證知識圖譜的完整性。形狀（shapes）定義在 `ontology/shapes.ttl` 中。

若要獨立執行 SHACL 驗證，請運行：

```bash
python3 src/validate_shacl.py
```

這將根據形狀定義驗證生成的 `ontology/inferred-results.ttl` 圖，確保所有推導出的個體均符合我們預期的數據模型。
