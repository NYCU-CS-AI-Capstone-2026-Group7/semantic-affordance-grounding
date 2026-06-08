# AI Capstone 2026 Homework 5: 基於本體論的語意落地報告

**Group 07** | *國立陽明交通大學資訊工程學系*

## 小組成員
* 112550169 潘仰祐
* 112550095 葉羽宸
* 112550141 王佳欣
* 112550194 徐凡懿
* 113550173 曹育誠
* 113550050 陳建霖

---

## 1. 簡介與版本庫內容

本報告描述了由 Group 07 為實體人工智慧（Physical AI）機器人代理所開發的語意落地層（Semantic Grounding Layer）。在機器人操控任務中，代理必須架起橋樑，連接底層的原始感測數據（如 RGB-D 影像和 3D 座標系框架）與高層的抽象目標。我們的本體模型針對三個基準課程任務建模了環境物件和語意落地：
1. **疊杯任務 (Cup Stacking)**：將目標杯子疊放到參考位置。
2. **餐具排列 (Cutlery Arrangement)**：將操控目標（刀、叉）相對於放置參考物（盤子）進行排列。
3. **玩具積木收集 (Toy Block Collection)**：收集散落的玩具積木並將其放入容器（籃子）中。

### 版本庫結構與檔案配置
版本庫的結構旨在實現模組化開發、推理、驗證和查詢執行。以下是目錄佈局和檔案配置的詳細說明：

* [ontology/](ontology/)
  * [group-ontology.ttl](ontology/group-ontology.ttl)：小組特定的主本體檔案，包含環境個體、物理屬性（如寬度、顏色）、任務角色、協調框架的定義，以及用於推斷物件可抓取性的自訂類別等價公理。
  * [inferred-results.ttl](ontology/inferred-results.ttl)：包含所有宣告和推理三元組的實體化 RDF 圖。運行 Python 推理管線時會自動生成。
  * [shapes.ttl](ontology/shapes.ttl)：使用 SHACL（形狀約束語言）編寫的結構約束，用於驗證資料完整性（例如，在採取行動前，確保每個實體物件都具有顏色、位姿框架和近似寬度）。
  * [imports/](ontology/imports/)
    * [course-affordance.ttl](ontology/imports/course-affordance.ttl)：核心課程詞彙，提供基礎類別（如 `cap:PhysicalObject`、`cap:EndEffector`、`cap:Affordance`、`cap:GraspingAffordance`、`cap:ContainmentAffordance`、`cap:SupportAffordance`、`cap:StackabilityAffordance`、`cap:TaskRole`、`cap:TargetObject`、`cap:ReferenceObject`、`cap:ContainerTarget`、`cap:CollectableObject`、`cap:Cup`、`cap:Knife`、`cap:Fork`、`cap:Plate`、`cap:ToyBlock`、`cap:Basket`）。
    * [course-alignment.ttl](ontology/imports/course-alignment.ttl)：對齊公理，將課程術語對齊到標準化的上層本體（DUL、CORA 和 SOMA）。
* [queries/](queries/)
  * [graspable_objects.rq](queries/graspable_objects.rq)：SPARQL 查詢，旨在檢索動態歸類於推論類別 `cap:GraspableObject` 下的所有物件，以及它們的標籤、顏色和角色。
  * [task_objects.rq](queries/task_objects.rq)：SPARQL 查詢，列出所有環境物件、其子類別類型、角色和關聯的動作可能性（Affordance），以便於驗證整個圖形。
* [results/](results/)
  * [graspable_objects_output.txt](results/graspable_objects_output.txt)：可抓取物件查詢執行的格式化輸出。
  * [task_objects_output.txt](results/task_objects_output.txt)：完整任務物件驗證查詢執行的格式化輸出。
  * [shacl_report.txt](results/shacl_report.txt)：儲存 SHACL 約束檢查驗證輸出的日誌檔案。
* [src/](src/)
  * [run_inference.py](src/run_inference.py)：Python 腳本，解析來源本體並運行 OWL 2 RL 推理機以實體化並序列化推理三元組。
  * [run_queries.py](src/run_queries.py)：Python 腳本，針對推論圖執行 SPARQL 查詢並匯出格式化結果。
  * [validate_shacl.py](src/validate_shacl.py)：Python 腳本，針對 SHACL 形狀驗證推論圖，以強制執行資料完整性。

---

## 2. 本體設計原理與命名空間政策

### 2.1 設計原理與建模邏輯
核心建模策略將物件的靜態分類學描述（物件是什麼，例如杯子或盤子）與其特定任務的角色（它們如何運作，例如目標物件或參考物件）以及它們的行動能力（可以用它們做什麼，例如抓取或堆疊）進行了解耦。

* **實體物件 (`cap:PhysicalObject`)**：代表環境中的物理事物。我們定義了子類別，如 `cap:Cup`、`cap:Knife`、`cap:Fork`、`cap:Plate`、`cap:ToyBlock` 和 `cap:Basket`。
* **動作可能性/可負擔性 (`cap:Affordance`)**：代表物件提供給機器人的行動可能性。例如，杯子具有 `cap:GraspingAffordance`（抓取動作可能性）和 `cap:StackabilityAffordance`（疊放動作可能性）。盤子提供 `cap:SupportAffordance`（支撐動作可能性），而籃子提供 `cap:ContainmentAffordance`（容納動作可能性）。
* **任務角色 (`cap:TaskRole`)**：代表與任務相關的特徵。例如，在疊杯過程中，`g07:blueCup01` 作為 `cap:TargetObject`（目標物件）。在餐具排列中，`g07:plate01` 作為 `cap:ReferenceObject`（參考物件）。在玩具積木收集中，`g07:basket01` 扮演 `cap:ContainerTarget`（容器目標）的角色。

透過這種方式結構化本體，機器人規劃器可以在運行時查詢本體，以確定哪些物件是可抓取的、在何處放置物件（參考物 vs. 容器目標），以及要將哪些物理參數（顏色、寬度、座標框架）傳遞給運動規劃器。

#### 進階特徵：硬體特定的夾爪約束
除了基本要求外，我們還整合了硬體特定的約束，以將代理落地到真實的物理限制中。我們定義了 `cap:EndEffector` 類別，並建立了一個代表機器人物理夾爪的實例：
```turtle
g07:parallelGripper01
    a cap:EndEffector ;
    rdfs:label "parallel gripper 01"@en ;
    rdfs:comment "The parallel-jaw gripper used by Group 07's robot arm in all three baseline tasks."@en ;
    cap:hasApproxWidth "0.08"^^xsd:decimal .
```
環境中的每個可抓取目標都使用 `cap:hasApproxWidth` 指定其物理寬度，並透過 `cap:canBeManipulatedBy` 參照其相容性：
```turtle
g07:blueCup01
    cap:hasApproxWidth "0.075"^^xsd:decimal ;
    cap:canBeManipulatedBy g07:parallelGripper01 .
```
這種建模允許機器人查詢特定的目標物件是否符合其末端執行器的物理限制。如果物件的寬度超過夾爪的最大張開度（例如，如果我們有一個寬度為 0.15 米的大箱子），機器人就可以確定該物件無法被操縱，從而防止機械碰撞和規劃失敗。

#### 語意豐富性 vs. 扁平標籤
為了確保我們的知識圖譜對人類開發人員和下游 AI 組件（例如從本體定義構建任務計劃的 LLM）都保持可讀性，我們避免使用扁平的文字識別碼。每個主要的類別、屬性和個體都富含人類可讀的元數據：
* `rdfs:label`：提供可讀的、本地化的字串名稱（例如 `"blue cup 01"@en`）。
* `rdfs:comment`：描述目的、上下文或建模假設。
* `skos:definition` 和 `skos:scopeNote`：詳細說明精確的語意定義和實作指南，以防止手動宣告謬誤。

### 2.2 命名空間政策
為了防止詞彙污染並確保乾淨的整合，我們在共享課程定義和小组自訂之間保持嚴格的分離：

* **課程通用命名空間 (`cap:`)**
  * 前綴：`cap`
  * URI：`https://hcis.io/ontology/aicapstone/2026/`
  * 用途：嚴格保留給共享的、基礎的課程詞彙類別和屬性。
* **小組自訂命名空間 (`g07:`)**
  * 前綴：`g07`
  * URI：`https://hcis.io/ontology/aicapstone/2026/group07/`
  * 用途：專門用於我們小組特定的環境實例（個體）、硬體約束和進階語意定義的命名空間。

---

## 3. 複用與新引入的術語

為了保持與專案規範的一致性，我們複用了課程本體中的類別和屬性，並使用自訂個體對其進行了擴充。這些術語分類如下：

### 3.1 複用術語（來自課程詞彙）
* **核心類別**：`cap:PhysicalObject`、`cap:EndEffector`、`cap:Affordance`、`cap:GraspingAffordance`、`cap:ContainmentAffordance`、`cap:SupportAffordance`、`cap:StackabilityAffordance`、`cap:TaskRole`、`cap:TargetObject`、`cap:ReferenceObject`、`cap:ContainerTarget`、`cap:CollectableObject`、`cap:Cup`、`cap:Knife`、`cap:Fork`、`cap:Plate`、`cap:ToyBlock`、`cap:Basket`。
* **物件屬性**：`cap:hasAffordance`、`cap:hasTaskRole`、`cap:canBeManipulatedBy`。
* **資料型態屬性**：`cap:hasColor` (string)、`cap:hasObjectLabel` (string)、`cap:hasPoseFrame` (string)、`cap:hasApproxWidth` (decimal)。

### 3.2 新引入的術語（小組自訂新增物與個體）
* **元數據小組**：`g07:team07`（定義為代表我們學生團隊的 `foaf:Group`）。
* **夾爪實例**：`g07:parallelGripper01`（代表我們特定的機器人末端執行器）。
* **動作可能性個體**（由物件連結的共享實例）：
  * `g07:graspingAffordance01` (`cap:GraspingAffordance`)
  * `g07:containmentAffordance01` (`cap:ContainmentAffordance`)
  * `g07:supportAffordance01` (`cap:SupportAffordance`)
  * `g07:stackabilityAffordance01` (`cap:StackabilityAffordance`)
* **環境物件實例**：
  * 疊杯任務：`g07:blueCup01` (型態: `cap:Cup`)、`g07:pinkCup01` (型態: `cap:Cup`)。
  * 餐具排列任務：`g07:knife01` (型態: `cap:Knife`)、`g07:fork01` (型態: `cap:Fork`)、`g07:plate01` (型態: `cap:Plate`)。
  * 玩具積木收集任務：`g07:toyBlock01` (型態: `cap:ToyBlock`)、`g07:toyBlock02` (型態: `cap:ToyBlock`)、`g07:basket01` (型態: `cap:Basket`)。

---

## 4. 核心公理、限制與推理模式

### 4.1 可抓取性的存在限制
本專案的一個關鍵要求是避免手動宣告物件是可抓取的。相反地，可抓取性是使用描述邏輯（Description Logic, DL）概念化建模的：

`cap:GraspableObject ≡ cap:PhysicalObject ⊓ ∃cap:hasAffordance.cap:GraspingAffordance`

在 Turtle 語法中，我們使用 `owl:equivalentClass` 結合 `owl:intersectionOf` 和一個存在限制 `owl:Restriction`（在屬性 `cap:hasAffordance` 上使用 `owl:someValuesFrom`）來實現此定義：

```turtle
cap:GraspableObject
    a owl:Class ;
    rdfs:label "graspable object"@en ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            cap:PhysicalObject
            [   a owl:Restriction ;
                owl:onProperty cap:hasAffordance ;
                owl:someValuesFrom cap:GraspingAffordance
            ]
        )
    ] .
```

### 4.2 推理模式：逐步追蹤
為了說明 OWL RL 推理機如何推導出可抓取性，請考慮個體 `g07:blueCup01`。推理順序如下：

1. **圖形中的宣告事實**：
   * `g07:blueCup01 a cap:Cup .`
   * `g07:blueCup01 cap:hasAffordance g07:graspingAffordance01 .`
   * `g07:graspingAffordance01 a cap:GraspingAffordance .`
2. **子類別繼承推理**：
   * 課程本體定義了 `cap:Cup rdfs:subClassOf cap:PhysicalObject .`
   * 使用子類別繼承規則（特別是 OWL 2 RL 中的規則 `cax-sco`），推理機推斷出：
     $$\text{g07:blueCup01} \in \text{cap:PhysicalObject}$$
3. **存在限制推理**：
   * 由於 `g07:blueCup01` 具有指向 `g07:graspingAffordance01` 的屬性 `cap:hasAffordance`，且 `g07:graspingAffordance01` 屬於 `cap:GraspingAffordance` 類別，因此該個體滿足存在限制：
     $$\text{g07:blueCup01} \in \exists\text{cap:hasAffordance}.\text{cap:GraspingAffordance}$$
4. **交集與等價類別推理**：
   * 因為 `g07:blueCup01` 同時滿足這兩個交集條件，所以它被歸類到它們的交集類別中。
   * 透過類別等價公理（`owl:equivalentClass`），推理機動態推斷出 `g07:blueCup01` 屬於 `cap:GraspableObject`：
     $$\text{g07:blueCup01} \in \text{cap:GraspableObject}$$
   * 新的三元組 `g07:blueCup01 rdf:type cap:GraspableObject` 被實體化到推論圖中。

### 4.3 Python 推理管線
我們根據課程指南的 **Option C** 實作了 Python 推理管線（`src/run_inference.py`）：
* 我們使用 `rdflib` 將 `course-affordance.ttl` 和 `group-ontology.ttl` 載入到 RDF 圖中。
* We run the OWL 2 RL reasoner by executing `owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)`. 這會計算圖在 OWL 2 RL 語意下的演繹閉包，評估交集和限制公理。
* 實體化的三元組被序列化並匯出到 `ontology/inferred-results.ttl`，使標準 SPARQL 引擎能夠直接查詢分類結果。

---

## 5. 查詢結果

### 5.1 SPARQL 查詢 1：可抓取物件
在實體化圖上執行了 SPARQL 查詢 `queries/graspable_objects.rq`，以檢索所有推論出的可抓取個體：

```sparql
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?obj ?label ?color ?objectLabel ?role
WHERE {
    ?obj a cap:GraspableObject .
    OPTIONAL { ?obj rdfs:label         ?label       . FILTER(lang(?label) = "en") }
    OPTIONAL { ?obj cap:hasColor       ?color       . }
    OPTIONAL { ?obj cap:hasObjectLabel ?objectLabel . }
    OPTIONAL { ?obj cap:hasTaskRole    ?role        . }
}
ORDER BY ?obj
```

#### 執行輸出表格
查詢精確地回傳了 6 個可抓取目標：

| 物件 URI | 標籤 | 顏色 | 物件標籤 | 物件角色 |
| :--- | :--- | :--- | :--- | :--- |
| `g07:blueCup01` | blue cup 01 | blue | blue_cup | `cap:TargetObject` |
| `g07:fork01` | fork 01 | silver | cutlery_fork | `cap:TargetObject` |
| `g07:knife01` | knife 01 | silver | cutlery_knife | `cap:TargetObject` |
| `g07:pinkCup01` | pink cup 01 | pink | pink_cup | `cap:TargetObject` |
| `g07:toyBlock01` | toy block 01 | red | toy_block_red | `cap:CollectableObject` |
| `g07:toyBlock02` | toy block 02 | blue | toy_block_blue | `cap:CollectableObject` |

### 5.2 驗證與盲點分析：排除參考物件與容器物件
至關重要的是，**`g07:plate01`**（在餐具排列任務中用作放置參考）和 **`g07:basket01`**（在玩具積木收集任務中用作收集目的地）被**正確地排除**在查詢輸出之外。

* `g07:plate01` 被宣告了 `cap:SupportAffordance`，但沒有 `cap:GraspingAffordance`。
* `g07:basket01` 被宣告了 `cap:ContainmentAffordance`，但沒有 `cap:GraspingAffordance`。

由於推理機嚴格評估存在限制，只有具有 `cap:GraspingAffordance` 的實體物件才會被歸類在 `cap:GraspableObject` 下。這避免了將任務中涉及的每個物件都視為抓取目標的常見建模錯誤。透過將任務角色與物理動作可能性解耦，我們防止了機器人嘗試對重型表面（如盤子）或大型容器（如籃子）執行無效的抓取動作。

### 5.3 SPARQL 查詢 2：完整任務物件驗證
我們還執行了 `queries/task_objects.rq` 以驗證每個實例是否被正確分類和標註。在推理過程中，OWL RL 引擎生成了代表在 `owl:intersectionOf` 和 `owl:Restriction` 定義中定義的匿名交集類別的空白節點（例如 `nb299a8a0607644d58d2893a5b6b47f80b7`）。序列化中這些空白節點的存在證實了 OWL 2 RL 推理機成功評估了存在限制約束。

---

## 6. 設計選擇與討論

### 6.1 透過 SHACL 解耦推理和結構驗證
在我們的實作中，我們將 OWL 2 RL 推理與 SHACL 驗證相結合。這是一個深思熟慮的技術選擇，旨在處理 OWL 的開放世界假設（OWA）與執行安全所需的封閉世界假設（CWA）之間的差異：

1. **開放世界假設下推理 (OWL)**：OWL 假設如果缺少某項資訊，它只是未知而非錯誤。如果我們對杯子建模但省略了其座標位姿框架，OWL 推理仍然會成功而不會拋出錯誤。
2. **驗證下封閉世界假設 (SHACL)**：在物理機器人控制中，缺少參數（例如未指定物件的顏色、位姿框架或物理寬度）將導致運動規劃器或感知系統崩潰。我們使用 SHACL（定義在 `ontology/shapes.ttl`）來強制執行資料完整性。

我們的 SHACL 形狀定義了對實體物件的嚴格要求：
```turtle
cap:PhysicalObjectShape
    a sh:NodeShape ;
    sh:target [
        a sh:SPARQLTarget ;
        sh:select """
            PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
            SELECT ?this WHERE {
                ?this a cap:PhysicalObject .
                FILTER NOT EXISTS { ?this a cap:EndEffector . }
            }
        """ ;
    ] ;
    sh:property [
        sh:path cap:hasObjectLabel ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path cap:hasApproxWidth ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path cap:hasPoseFrame ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path cap:hasColor ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path cap:hasTaskRole ;
        sh:class cap:TaskRole ;
        sh:minCount 1 ;
    ] .
```

* **SPARQL 目標 (Target)**：我們使用 `sh:SPARQLTarget` 來選擇所有 `cap:PhysicalObject` 實例，*但排除* `cap:EndEffector`。這可以防止我們的機器人夾爪（`g07:parallelGripper01`）針對特定於環境物件的屬性（如 `hasPoseFrame`）進行驗證，因為夾爪是一個持久的硬體組件，而不是感知到的目標物件。
* **屬性約束**：它保證了每個任務物件都具有至少一個顏色、標籤、寬度和座標框架。

運行 `validate_shacl.py` 輸出 `SHACL validation: CONFORMS`，證明我們的知識圖譜在結構上是完整的，並已為安全物理執行做好準備。

---

## 7. 限制與未來改進

### 7.1 Python 中 OWL 2 RL 的表達力限制
我們的推理管線使用 Python 的 `owlrl` 引擎，該引擎受限於 OWL 2 RL 配置檔。OWL 2 RL 旨在對大型三元組庫進行多項式時間推理。然而，它缺乏對完整 OWL 2 DL 結構的支持，例如複雜的屬性鏈或一般的基數限制。如果我們的環境模型需要高表達力的 DL 邏輯，我們將不得不將我們的管線遷移到重型 Java 基底推理框架（例如 Pellet 或 HermiT），這些框架很難整合到即時的 Python 基底機器人技術棧中。

### 7.2 靜態 vs. 動態動作可能性 (Affordances)
目前，動作可能性在語意網中表示為靜態的、宣告的事實。在真實的物理環境中，物件的可抓取性是動態且與上下文相關的。諸如運動學可達性、工作空間雜亂度、關節極限飽和度、物件朝向和表面摩擦力等因素，決定了機器人是否能成功抓取物件。
* *未來改進*：將本體連接到幾何模擬器（例如 PyBullet、MoveIt）。我們可以編寫規則，根據即時空間檢查動態更新 RDF 圖形，改變 `cap:GraspingAffordance` 的宣告。

### 7.3 自動夾爪相容性推理
目前，每個物件的 `canBeManipulatedBy` 關係都是手動宣告的。動態推導這種關係會更具魯棒性。藉由比較目標物件的 `cap:hasApproxWidth` 與夾爪的開口寬度（`g07:parallelGripper01`），推理機應該自動確定夾爪是否可以抓取該物件。
* *未來改進*：實作 SWRL（語意網規則語言）規則或 SPARQL 構造查詢，以評估數值條件（例如 `objectWidth <= gripperWidth`）來動態推導出 `cap:canBeManipulatedBy` 關係，從而消除手動相容性宣告的需求。

---

## 8. 結論

藉由實作這個語意落地層，Group 07 成功建立了一個結構化的知識庫，架起了高層符號任務規劃與底層物理機器人控制之間的橋樑。藉由利用 OWL 2 RL 推理，物件的可抓取性是從物理屬性動態推導出來的，而不是手動寫死的，從而避免了建模錯誤。SHACL 驗證的整合保證了資料圖形在採取行動前符合嚴格的模式，為安全實體人工智慧（Physical AI）行為提供了強健、可驗證的基礎。
