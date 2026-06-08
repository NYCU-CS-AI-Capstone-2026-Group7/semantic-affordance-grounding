# 作業五：基於本體論的語意落地 (Ontology-based Semantic Grounding)

* **人工智慧專題 (Artificial Intelligence Capstone)**
* **授課教師：Chun-yien Chang <ccy@hptp.org>**
* **學期：2026年春季 (Spring 2026)**

---

## 導言 (Introduction)

本作業要求各小組為具備抓取（grasping）能力的機器人代理建構一個小型但語意明確的**本體論（Ontology）**。該本體論應藉由連結物件類型（object types）、任務角色（task roles）、操作可負性（manipulation affordances）以及可推導的抓取能力（inferable graspability），來使課程專案環境中感知到的物件語意落地（ground）。

預期產出為一個精簡且可測試的語意層（semantic layer），使一個以機器人為導向的知識庫（robot-oriented knowledge base）能夠回答以下問題：**環境中哪些物件是可抓取的，以及為什麼？**

---

## 1. 背景與動機 (Context and Motivation)

AI 專題課程專案讓學生接觸到物理人工智慧（Physical AI）的工作流程：真實世界數據收集、模擬中的重建、機器人運動生成與數據創建、策略訓練以及推導與評估。預定義的入門任務為：疊杯（cup stacking）、餐具排列（cutlery arrangement）與玩具積木收集（toy block collection）。

這些任務引入了諸如杯子（cups）、刀子（knife）、叉子（fork）、盤子（plate）、玩具積木（toy blocks）與籃子（basket）等物件類別。本作業在該管線中加入了一個**語意層**，要求學生不僅將這些物件描述為視覺標籤或模擬實體，還要將它們描述為本體論中具備類型（typed）、可查詢（queryable）且可推導（inferable）的實體。

技術動機在於，雖然學習到的策略可能在觀察、物件姿態（object poses）或動作軌跡（action trajectories）上運行，但當機器人代理必須解釋、驗證、重用或推廣其行為時，它也需要明確的語意知識。一個語意落地層可以聲明：藍色杯子是一個物理物件、是疊杯任務中的目標物件、是具有抓取可負性的物件，因此是一個被推導出可抓取的物件。這使得「識別（recognition）」與「落地（grounding）」之間的區別變得明確。

---

## 2. 學習目標 (Learning Objectives)

完成本作業後，學生應能夠：

1. 使用 RDF、RDFS 和 OWL 建構基本任務物件模型。
2. 區分物件類型（object type）、任務角色（task role）、可負性（affordance）和物件實體（object instance）。
3. 使用 OWL 類別公理（class axioms）或限制（restrictions）來支援推理。
4. 使用 SPARQL 查詢推導出的可抓取物件。
5. 在可重現的 GitHub 儲存庫中組織本體論、查詢、程式碼和報告檔案。
6. 解釋語意層如何互補機器人學習管線。

---

## 3. 概念基礎 (Conceptual Foundation)

### RDF、Turtle、OWL 和 SPARQL
RDF 將資訊表示為「主體-述詞-客體（subject-predicate-object）」三元組。Turtle 是一種用於編寫 RDF 圖的精簡文字語法，因此適用於小型課程本體論 and 易讀的範例。OWL 2 提供了定義類別（classes）、屬性（properties）、個體（individuals）、限制（restrictions）和具有正式意義的本體論公理（ontology axioms）的詞彙。SPARQL 是 RDF 圖的標準查詢語言，包括以 RDF 原生儲存的圖，或透過中間件公開的圖。

### 機器人本體論參考資料 (Robotics Ontology References)
本作業使用簡化的教學本體論，而非要求學生導入完整的機器人本體論。然而，其設計與主要的機器人知識表示傳統保持一致：
* **IEEE CORA / IEEE 1872-2015**：機器人與自動化的核心本體論，旨在提供基礎概念，以便在此之上建構更詳細的機器人本體論。
* **IEEE AuR / IEEE 1872.2-2021**：自主機器人本體論，將 CORA 擴展至自主系統的領域知識。
* **SOMA**：活動的社會物理模型（Socio-physical Model of Activities），用於為日常操作活動和具身代理（embodied agents）建模。
* **KnowRob**：一個機器人知識處理系統，旨在支援自主機器人完成日常操作任務所需的知識。

因此，課程本體論應被理解為一個刻意精簡的教育性設定：在頂層受到 CORA/AuR 的啟發，在操作與可負性層面受到 SOMA/KnowRob 的啟發，而在任務物件層面則具備課程專特性。為了保持課程本體論的輕量化，同時使其術語具備可追溯性，所選的課程術語可以使用 SKOS 與現有的機器人本體論詞彙進行對齊。這些映射僅用於文件化和語意交叉引用；本作業所需的推理行為仍由本地 OWL 公理定義。對齊原則、命名空間宣告和正式表達方式在附錄中提供。

---

## 4. 作業問題陳述 (Homework Problem Statement)

假設一個帶有夾爪（gripper）的機器人代理在任務環境中觀察到多個物件。機器人從感知或模擬中接收物件標籤（labels）、顏色（colors）以及可能的姿態座標系識別碼（pose-frame identifiers）。您的任務是**建構一個本體論，使機器人能夠在語意上落地這些觀察到的物件，並推導出哪些物件是可抓取的**。

您的本體論必須至少包含三個預定義課程任務中涉及的物件類型：

1. **疊杯 (Cup stacking)**：藍色杯子（blue cup）和粉紅色杯子（pink cup）。
2. **餐具排列 (Cutlery arrangement)**：刀子（knife）、叉子（fork）和盤子（plate）。
3. **玩具積木收集 (Toy block collection)**：玩具積木（toy blocks）和籃子（basket）。

針對自行定義進階任務的小組可以增加額外的物件類型和可負性，但仍必須包含上述基準物件詞彙。

---

## 5. 要求的本體論資源 (Required Ontology Resources)

您的本體論必須至少使用以下資源：
* `owl:Class`
* `owl:ObjectProperty`
* `owl:DatatypeProperty`
* `rdfs:subClassOf`
* `rdfs:label`
* `rdfs:comment` 或 `skos:definition`
* 至少一個支援推理的 `owl:Restriction` 或 `owl:equivalentClass` 模式
* 代表觀察到或模擬物件的物件實體（object instances）
* 至少一個顯示推導出的 `cap:GraspableObject` 實體的推理結果

每個主要的本體論實體（包括類別、物件屬性、資料屬性以及與任務相關的個體）都必須包含人類可讀的標籤和簡短的解釋性註釋。建議的註釋模式是使用 `rdfs:label` 提供可讀名稱，並使用 `rdfs:comment` 或 `skos:definition` 對該實體在課程專案情境中的含義進行簡明解釋。當學生需要澄清建模範圍、限制或預期用途時，也可以使用 `skos:scopeNote`。

這些註釋並不能取代正式的公理。它們使本體論對於人類讀者而言是可解釋的，並有助於解釋每個術語背後的建模承諾，而 OWL/RDFS 公理則負責分類、限制和推理行為。必要的註釋風格範例在 Listing 1, 2, 3 和 4 中提供。

---

## 6. 建議的建模區分 (Recommended Modeling Distinctions)

常見的建模錯誤是將每個與任務相關的物件都簡單地視為「可抓取的（graspable）」。本作業要求更精確的區分：

| 圖層 (Layer) | 意涵 (Meaning) | 範例物件 (Examples) |
| :--- | :--- | :--- |
| **物件類型 (Object type)** | 共享的課程類別 (Classes) | `cap:Cup`, `cap:Knife`, `cap:Fork`, `cap:Plate`, `cap:ToyBlock`, `cap:Basket` |
| **任務角色 (Task role)** | 共享的課程角色類別 | `cap:TargetObject`, `cap:ReferenceObject`, `cap:ContainerTarget`, `cap:CollectableObject` |
| **可負性 (Affordance)** | 共享的課程可負性類別 | `cap:GraspingAffordance`, `cap:SupportAffordance`, `cap:ContainmentAffordance`, `cap:StackabilityAffordance` |
| **實體 (Instance)** | 小組特定的個體 (Individuals) | `g05:blueCup01`, `g05:knife01`, `g05:block01` （註：`g05:` 為範例，每組需替換為自己的前綴） |
| **推導類別 (Inferred class)** | 推理器導出的類別成員資格 | `g05:blueCup01 rdf:type cap:GraspableObject` |

這個區分非常重要，因為在餐具排列任務中，盤子可能是放置參考（placement reference），而刀和叉是直接操作目標。在積木收集任務中，籃子可能是容器目標（container target），而玩具積木是可收集的抓取目標。盤子或籃子是否也應該是可抓取的，取決於小組如何為機器人的任務和夾爪能力建模。

---

## 7. 基礎本體論設定 (Base Ontology Profile)

學生可以使用以下基礎本體論設定作為起點。前綴 `cap:` 代表課程特定的 AI Capstone 本體論命名空間。

### 7.1 核心類別 (Core Classes)
Listing 1 顯示了完整課程本體論的開頭摘錄。它包括命名空間宣告、本體論級別的元數據以及核心類別詞彙的第一部分。完整的本體論以單個 Turtle 檔案提供：`course-affordance.ttl`。

**Listing 1: 課程本體論的開頭摘錄（包括命名空間宣告、本體論元數據和核心類別定義）**
```turtle
@prefix cap: <https://hcis.io/ontology/aicapstone/2026/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

# 本體論元數據
<https://hcis.io/ontology/aicapstone/2026>
    a owl:Ontology ;
    rdfs:label "AI Capstone 2026 Course Ontology"@en ;
    rdfs:comment "A reduced educational ontology profile for semantic and affordance grounding of graspable objects in the AI Capstone 2026 course project."@en ;
    dcterms:title "AI Capstone 2026 Course Ontology"@en ;
    dcterms:description "This ontology defines a compact course vocabulary for representing physical task objects, task roles, manipulation affordances, grounding identifiers, and inferable graspability in the AI Capstone 2026 Physical AI project."@en ;
    dcterms:creator cap:ccyontologist ;
    dcterms:created "2026-05-22"^^xsd:date ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    vann:preferredNamespacePrefix "cap" ;
    vann:preferredNamespaceUri "https://hcis.io/ontology/aicapstone/2026/" .

cap:ccyontologist
    a foaf:Person ;
    foaf:name "Chun-yien Chang"@en ;
    foaf:mbox <mailto:ccy@hptp.org> .

# 核心類別
cap:PhysicalObject
    a owl:Class ;
    rdfs:label "physical object"@en ;
    rdfs:comment "A material object in the task environment that may be perceived, manipulated, used as a reference object, or assigned a task role."@en .

# ... 為了節省空間而省略；請參閱完整的本體論檔案。
```

### 7.2 屬性 (Properties)
Listing 2 說明了預期的註釋風格、定義域（domain）和值域（range）宣告，以及本體論級別語意關係與管線落地識別碼之間的區別。

**Listing 2: 物件屬性與資料屬性摘錄**
```turtle
# 屬性
cap:hasAffordance
    a owl:ObjectProperty ;
    rdfs:domain cap:PhysicalObject ;
    rdfs:range cap:Affordance ;
    rdfs:label "has affordance"@en ;
    rdfs:comment "Relates a physical object to an affordance associated with that object in the task context."@en .

cap:hasTaskRole
    a owl:ObjectProperty ;
    rdfs:domain cap:PhysicalObject ;
    rdfs:range cap:TaskRole ;
    rdfs:label "has task role"@en ;
    rdfs:comment "Relates a physical object to the role it plays in a task."@en .

cap:hasTargetObject
    a owl:ObjectProperty ;
    rdfs:domain cap:Task ;
    rdfs:range cap:PhysicalObject ;
    rdfs:label "has target object"@en ;
    rdfs:comment "Relates a task to a physical object that is directly acted upon in that task."@en .

cap:canBeManipulatedBy
    a owl:ObjectProperty ;
    rdfs:domain cap:PhysicalObject ;
    rdfs:range cap:EndEffector ;
    rdfs:label "can be manipulated by"@en ;
    rdfs:comment "Relates a physical object to an end effector capable of manipulating it."@en .

cap:hasObjectLabel
    a owl:DatatypeProperty ;
    rdfs:domain cap:PhysicalObject ;
    rdfs:range xsd:string ;
    rdfs:label "has object label"@en ;
    rdfs:comment "Records the object label used by perception, simulation, or task documentation."@en .

# ... 為了節省空間而省略；請參閱完整的本體論檔案。
```

---

## 8. 本體論 URI 與命名空間規範 (Ontology URI and Namespace Policy)

上述引入的課程本體論使用前綴 `cap:` 來表示本作業中提供的共享詞彙：
```turtle
@prefix cap: <https://hcis.io/ontology/aicapstone/2026/> .
```

此命名空間保留給課程級別的術語，例如 `cap:PhysicalObject`、`cap:GraspableObject`、`cap:hasAffordance` 和 `cap:hasPoseFrame`。各組在引用共享的課程詞彙時應重用這些術語，但**不應**直接在 `cap:` 命名空間下放置其特定任務的類別、實體或擴充。

每個小組必須為其提交的本體論定義自己的本體論 URI 和命名空間。各組必須參考 Listing 1 中的本體論元數據範例，並為其自己的本體論提供相同種類的元數據：標題、描述、創建者資訊、創建日期、許可證、首選命名空間前綴和首選命名空間 URI。例如，小組可以定義如下的命名空間：
```turtle
@prefix g05: <https://hcis.io/ontology/aicapstone/2026/group05/> .
```

在這種模式中，`cap:` 表示共享的課程本體論，而 `g05:` 表示該小組自己的建模空間。課程術語可以直接重用，但小組特定的物件類別、任務變體、個體或額外的可負性應在小組命名空間下宣告。

---

## 9. 課程物件層 (Course Object Layer)

以下物件層涵蓋了三個入門級任務。Listing 3 顯示了完整課程本體論中課程特定物件類別的摘錄。學生可以透過增加額外的物件類別、可負性和任務角色來擴充此圖層以用於進階任務。

**Listing 3: 課程特定物件類別摘錄**
```turtle
# 課程物件
cap:Cup
    a owl:Class ;
    rdfs:subClassOf cap:PhysicalObject ;
    rdfs:label "cup"@en ;
    rdfs:comment "A container-like object used in the cup-stacking task."@en ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty cap:hasAffordance ;
        owl:someValuesFrom cap:GraspingAffordance
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty cap:hasAffordance ;
        owl:someValuesFrom cap:StackabilityAffordance
    ] .

cap:Knife
    a owl:Class ;
    rdfs:subClassOf cap:PhysicalObject ;
    rdfs:label "knife"@en ;
    rdfs:comment "A cutlery object to be placed in the cutlery-arrangement task."@en ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty cap:hasAffordance ;
        owl:someValuesFrom cap:GraspingAffordance
    ] .

# ... 為了節省空間而省略；請參閱完整的本體論檔案。
```

---

## 10. 環境實體 (Environment Instances)

學生必須建立代表任務環境中物件的物件實體（個體）。提交的本體論必須包含所有三個預定義任務中涉及的基準物件實體，無論小組選擇哪個入門任務：
* 疊杯任務中的藍杯和粉杯。
* 餐具排列任務中的刀、叉和盤。
* 玩具積木收集任務中的玩具積木和籃子。

這些個體應在小組特定的命名空間下宣告，而其語意類型 and 屬性則可以重用共享的 `cap:` 詞彙。在下面的範例中，`g05:` 僅作為範例小組前綴。每個小組必須將其替換為其自身實際的小組命名空間。

**Listing 4: 小組特定的物件實體範例**
```turtle
@prefix cap: <https://hcis.io/ontology/aicapstone/2026/> .
@prefix g05: <https://hcis.io/ontology/aicapstone/2026/group05/> .

# 在此範例中，g05: 是第 5 組的範例前綴。
# 每個小組應將其替換為其自身特定的命名空間。

g05:blueCup01
    a cap:Cup ;
    rdfs:label "blue cup 01"@en ;
    rdfs:comment "The blue cup instance defined by Group 05 for the baseline cup-stacking task."@en ;
    cap:hasColor "blue" ;
    cap:hasObjectLabel "blue_cup" ;
    cap:hasTaskRole cap:TargetObject ;
    cap:hasPoseFrame "world/object_blue_cup" .

# 使用相同的模式定義其餘的基準任務物件：
# 粉色杯子、刀子、叉子、盤子、玩具積木和籃子。
# 如果小組定義了額外的任務，則增加進階任務物件。
```

---

## 11. 推理模式 (Reasoning Pattern)

在定義了共享詞彙、課程特定的物件類別和環境實體之後，下一步是指定如何推導出可抓取性。核心推理目標是 `cap:GraspableObject`。

概念上，該類別在描述邏輯（Description Logic）中可定義如下：

$$cap:GraspableObject \equiv cap:PhysicalObject \sqcap \exists cap:hasAffordance.cap:GraspingAffordance$$

這意味著，可抓取物件被定義為「具有至少一個抓取可負性（`cap:GraspingAffordance`）的物理物件（`cap:PhysicalObject`）」。

在 OWL/Turtle 中，相同的建模模式可以序列化為一個 `owl:equivalentClass` 公理，其中包含 `owl:intersectionOf` 表達式和一個存在限制（existential restriction）：

**Listing 5: 可抓取物件推理模式的 OWL/Turtle 序列化**
```turtle
cap:GraspableObject
    a owl:Class ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            cap:PhysicalObject
            [ a owl:Restriction ;
              owl:onProperty cap:hasAffordance ;
              owl:someValuesFrom cap:GraspingAffordance
            ]
        )
    ] .
```

### 預期的推導（Inference）邏輯：
> 如果某個個體是 `cap:PhysicalObject`，且具有至少一個指向 `cap:GraspingAffordance` 的 `cap:hasAffordance` 關係，則該個體可被自動分類為 `cap:GraspableObject`。

對於本作業，所需的推理功能是基於 OWL 類別定義、子類別公理和存在限制的**類別分類（class classification）**。特別是，推理器（reasoner）應能夠使用諸如 `owl:equivalentClass`、`owl:intersectionOf` 和 `owl:someValuesFrom` 等公理將個體自動分類到 `cap:GraspableObject` 下。

有多種工作流可支援此要求：
* **Protégé** 配合 OWL 2 DL 推理器（如 HermiT 或 Pellet）適合直接檢查推導出的類別成員資格。
* **Java 工作流**可以使用 **Apache Jena** 進行 RDF 解析和 SPARQL 查詢，但小組必須驗證所選的 Jena 推理設定是否支援其本體論中使用的 OWL 模式。
* 使用 **RDFLib 的 Python 工作流**僅在小組清楚記錄了用於推導 `cap:GraspableObject` 成員資格的額外推理機制時才可被接受。

例如，如果每個 `cap:Cup` 都被建模為具有某種抓取可負性，那麼僅當所選的推理工作流支援所需的存在限制模式時，類型為 `cap:Cup` 的個體（例如 `g05:blueCup01`）才應被自動分類到 `cap:GraspableObject` 下。

此要求遵循上述定義中使用的 OWL 建模建構；學生應諮詢其所選工具的文檔，以確認對相關 OWL 推理功能的支援。

---

## 12. 查詢要求 (Query Requirement)

每個小組必須提供至少一個 SPARQL 查詢來檢索推導出的可抓取物件。該查詢應在**推導模型（inferred model）**上執行，而不僅僅是在原始宣告的圖（asserted graph）上。

**Listing 6: 用於推導出的可抓取物件之 SPARQL 查詢**
```sparql
PREFIX cap: <https://example.org/aicapstone/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?obj ?label ?role
WHERE {
    ?obj a cap:GraspableObject .
    OPTIONAL { ?obj cap:hasObjectLabel ?label . }
    OPTIONAL { ?obj cap:hasTaskRole ?role . }
}
ORDER BY ?obj
```

### 預期查詢結果：
預期結果應包含諸如 `cap:blueCup01`、`cap:pinkCup01`、`cap:knife01`、`cap:fork01` 和 `cap:block01` 等物件，前提是該小組使用了建議的類別公理。是否包含 `cap:plate01` 或 `cap:basket01` 取決於小組是否在其任務情境中明確將其建模為可抓取的。

OWL 推理與 SPARQL 查詢在本作業中扮演不同的角色：
* **OWL 推理模式**在本體論層面定義了 `cap:GraspableObject`，並允許推導出新的類別成員資格（新語意）。
* **SPARQL 查詢**則用於從已宣告或推導出的 RDF 圖中檢索數據。例如，SPARQL 屬性路徑（property path）可以搜尋類型為 `cap:GraspingAffordance` 或其子類別之一的可負性個體：
  `?affordance rdf:type/rdfs:subClassOf* cap:GraspingAffordance .`

然而，這仍然只是查詢層面的圖模式（graph pattern）；它本身並不能建立 `cap:GraspableObject` 在本體論層面的含義。因此，學生應使用 OWL 定義可抓取性，透過推理工作流對個體進行分類，並使用 SPARQL 檢索推導出的結果。

---

## 13. 技術方案選項 (Technology Options)

學生可以使用以下工作流之一。無論使用哪種工作流，都需要本體論和查詢檔案。

### 13.1 選項 A：Protégé 工作流 (Protégé Workflow)
1. 在 Protégé 中建立或開啟 Turtle 本體論。
2. 檢查類別層次結構、物件屬性、資料屬性和個體。
3. 執行推理器，例如本地安裝中可用的 HermiT 或 Pellet。
4. 驗證所選個體是否被推導為 `cap:GraspableObject`。
5. 將本體論匯出為 Turtle。
6. 在報告中附上推導出的類別成員資格截圖。

### 13.2 選項 B：Apache Jena 工作流 (Apache Jena Workflow)
Apache Jena 支援 RDF 數據處理、本體論模型、推理、SPARQL 查詢、SHACL 以及諸如 TDB2 的持久性三元組存儲。一個最小的命令列工作流為：

**Listing 7: 可能的 Jena CLI 工作流**
```bash
# 藉由嘗試解析檔案來驗證 Turtle 語法。
riot --validate ontology/course-affordance.ttl

# 查詢本地 RDF 檔案。推理支援可能需要程式碼或 Fuseki 設定。
arq --data ontology/course-affordance.ttl --query queries/graspable_objects.rq
```
為了進行推理，學生可以實現一個簡單的 Java 程式，該程式將本體論載入到推理模型中，並在推導出的圖上運行 SPARQL 查詢。

### 13.3 選項 C：Python RDFLib 工作流 (Python RDFLib Workflow)
RDFLib 可以解析 Turtle 並執行 SPARQL 查詢，但完整的 OWL 推理並非其預設強項。選擇 Python 的小組應：
* 使用 RDFLib 進行解析和查詢，外加一個獨立的推理器，或
* 清楚記錄其推理是透過額外的規則層（rule layer）實現，而非完整的 OWL 推理。

僅當小組清楚展示 `cap:GraspableObject` 成員資格是如何導出而非手動宣告時，純 Python 解決方案在本作業中才可被接受。

### 13.4 選項 D：Fuseki 端點工作流 (Fuseki Endpoint Workflow)
進階小組可以將本體論載入到 Apache Jena Fuseki 中，設定推理數據集，並透過網頁 UI 或 HTTP 查詢端點。此選項為自選。如果使用，儲存庫應包含配置說明和查詢範例。

---

## 14. Jena 的最小 Java 範例 (Minimal Java Example for Jena)

以下 Java 骨架說明了預期的工作流。學生可以對其進行調整。

**Listing 8: 最小的 Jena 風格推理 and 查詢工作流**
```java
import org.apache.jena.rdf.model.*;
import org.apache.jena.reasoner.*;
import org.apache.jena.reasoner.rulesys.*;
import org.apache.jena.query.*;
import org.apache.jena.util.FileManager;

public class GraspableQuery {
    public static void main(String[] args) {
        String ontologyPath = "ontology/course-affordance.ttl";
        String queryPath = "queries/graspable_objects.rq";
        
        Model base = FileManager.getInternal().loadModel(ontologyPath);
        
        Reasoner reasoner = ReasonerRegistry.getOWLReasoner();
        InfModel infModel = ModelFactory.createInfModel(reasoner, base);
        
        String queryString = FileManager.getInternal().readWholeFileAsUTF8(queryPath);
        Query query = QueryFactory.create(queryString);
        
        try (QueryExecution qe = QueryExecutionFactory.create(query, infModel)) {
            ResultSet results = qe.execSelect();
            ResultSetFormatter.out(System.out, results, query);
        }
    }
}
```
如果此程式未產生預期結果，學生應檢查推理器是否支援本體論中使用的確切 OWL 模式。他們可以簡化該模式或實現 Jena 規則（Jena rule），前提是報告中明確解釋了推理機制。

---

## 15. 可選的 SHACL 驗證 (Optional SHACL Validation)

SHACL 在本作業中並非強制，但推薦給想要區分「推理」與「驗證」的小組。OWL 用於推導類別成員資格；而 SHACL 可用於檢查提交的圖是否滿足要求的結構限制。

### 可能的驗證限制：
* 每個 `cap:PhysicalObject` 實體必須至少具有一個 `cap:hasObjectLabel`。
* 每個任務目標（task target）必須至少具有一個 `cap:hasTaskRole`。
* 每個旨在作為操作目標（manipulation target）的物件必須至少具有一個 `cap:hasAffordance`。
* 每個進階任務必須定義至少一個新物件類別以及一個新可負性或任務角色。

---

## 16. 交付成果 (Deliverables)

每個小組必須準備一個公開或課程可存取的 GitHub 儲存庫，並在對應的 E3 作業頁面上提交其連結。儲存庫必須包含小組撰寫的本體論、導入的本體論檔案、SPARQL 查詢、推理結果、文件以及下方說明的報告。

### 16.1 GitHub 儲存庫結構 (GitHub Repository Structure)

**Listing 9: 要求的儲存庫結構**
```text
semantic-affordance-grounding/
|-- README.md
|-- report.pdf                       # 或 report.md
|-- ontology/
|   |-- group-ontology.ttl           # 小組提交的主本體論
|   |-- inferred-results.ttl         # 推理後要求的推導圖
|   `-- imports/
|       |-- course-affordance.ttl     # 提供的課程本體論
|       `-- ...                      # 其他導入的本體論（若有使用）
|-- queries/
|   |-- graspable_objects.rq
|   `-- task_objects.rq              # 選填，但推薦提供
|-- results/
|   |-- graspable_objects_output.txt
|   `-- screenshots/                 # 推薦用於 Protégé/Fuseki 工作流的截圖
|-- src/                             # Java 或 Python 程式碼（若有使用）
|   `-- ...
`-- LICENSE                          # 選填
```

小組提交的主本體論應為 `ontology/group-ontology.ttl`。檔案 `ontology/imports/course-affordance.ttl` 是提供的課程本體論，應被視為導入的依賴項，而非小組自己的本體論。如果小組明確使用其他導入的標準本體論，也可以將其放置在 `ontology/imports/` 下。README 必須解釋哪些本體論檔案是由小組撰寫的，哪些檔案是導入的資源。

當透過圖形介面（例如 Protégé 或 Apache Jena Fuseki）驗證推理或查詢結果時，截圖是選填但推薦的。對於命令列工作流，只要結果可重現，儲存已保存的文字或 CSV 輸出檔案即足夠。

### 16.2 README 要求 (README Requirements)
`README.md` 必須包含：
1. 專案標題與小組成員。
2. 選擇的任務。
3. 本體論設計的簡短解釋。
4. 建模物件及其可負性的表格。
5. 命名空間規範，包括小組專特定術語使用哪個命名空間。
6. 運行查詢的說明。
7. 預期查詢輸出。
8. 解釋什麼是被推理出來的，而不僅僅是被手動宣告的。
9. 解釋 `ontology/inferred-results.ttl` 是如何生成的。
10. 指向本體論檔案、查詢檔案、原始碼和結果檔案的連結。

### 16.3 要求的提交組件 (Required Submission Components)

| 儲存庫項目 | 要求細節 |
| :--- | :--- |
| **README.md** | 必須解釋儲存庫結構、本體論設計、命名空間使用、導入的資源、查詢執行、推理工作流和預期結果。 |
| **report.pdf (或 .md)** | 報告應解釋儲存庫內容和本體論設計，包括設計基本原理、命名空間規範、重用和新引入的術語、關鍵公理和限制、推理模式、查詢結果、設計選擇、局限性以及小組想要討論的任何額外問題。 |
| **ontology/** | 必須包含小組撰寫的本體論，路徑為 `ontology/group-ontology.ttl`。此檔案應定義小組命名空間、任務實體、要求的註釋以及任何小組特定的擴充。推導圖必須導出並包含在 `ontology/inferred-results.ttl` 中。`ontology/imports/` 資料夾必須包含提供的 `course-affordance.ttl`，因為課程本體論是要求的共享詞彙。如果明確使用其他導入的本體論，也可以放置在該處。 |
| **queries/** | 必須至少包含 `queries/graspable_objects.rq`，該查詢檢索推導出的 `cap:GraspableObject` 個體。額外的查詢（例如 `queries/task_objects.rq`）是選填但推薦的。 |
| **results/** | 必須包含保存的查詢輸出，例如 `results/graspable_objects_output.txt`。當推理或查詢結果透過圖形介面（例如 Protégé 或 Apache Jena Fuseki）驗證時，截圖可放置在 `results/screenshots/` 下。 |
| **src/** | 可包含工作流中使用的額外程式碼、設定檔或腳本。此資料夾不作為獨立的交付成果進行評分，但在可用時應包含在內，以方便排除故障和提高重現性。 |

---

## 17. 評分標準 (Assessment Rubric)

| 評分準則 | 權重 | 指標與要求 |
| :--- | :--- | :--- |
| **本體論完整性 (Ontology completeness)** | 25% | 存在要求的 OWL/RDFS 資源；涵蓋所有基準任務物件；物件屬性和資料屬性有意義；主要本體論實體包含可讀的標籤以及註釋或定義。 |
| **語意豐富度 (Semantic richness)** | 25% | 物件類型、任務角色、可負性和實體被清晰區分；定義不僅僅是扁平的標籤。 |
| **推理與查詢 (Reasoning and query)** | 30% | 使用了至少一個非平凡的推理；導出了推導圖；透過 SPARQL 檢索推導出的可抓取物件；結果可重現。 |
| **儲存庫與文件 (Repository and documentation)** | 20% | GitHub 儲存庫井然有序；README 完整；報告解釋了建模選擇和局限性。 |

---

## 18. 常見建模誤區 (Common Modeling Pitfalls)

1. **誤區一：手動宣告所有結果。** 
   不要簡單地編寫 `cap:blueCup01 a cap:GraspableObject.`。至少有一些可抓取性結果必須是被推理器推導出來的。
2. **誤區二：混淆任務相關性與可抓取性。** 
   籃子可能與玩具積木收集任務相關，但它並不是直接要被抓取的物件。
3. **誤區三：混淆類別（Class）與實體（Instance/Individual）。** 
   `cap:Cup` 是一個類別；而 `cap:blueCup01` 是一個個體。
4. **誤區四：過度使用標籤。** 
   `rdfs:label` 或 `cap:hasObjectLabel` 不能替代類別成員資格和可負性建模。
5. **誤區五：僅查詢原始圖（Raw graph）。** 
   如果在沒有推理器的情況下運行查詢，推導出的類別成員資格將不會出現在查詢結果中。

---

## 19. 對進階小組的建議擴充 (Suggested Extension for Advanced Groups)

進階小組可以在以下一個或多個方向上擴充本體論：
* 增加特定於夾爪的限制，例如物件寬度、質量估計或可變形性（deformability）。
* 在語意上為任務成功標準（task success criteria）建模。
* 將物件實體連接到模擬物件名稱或姿態座標系（pose frames）。
* 增加對所需任務物件結構的 SHACL 驗證。
* 將本體論導出的可抓取性與策略（policy）成功或失敗案例進行比較。

---

## 20. 結論 (Conclusion)

本作業將本體論工程視為物理 AI（Physical AI）的實用語意基礎架構。核心要求是展示一個完整的**語意落地閉環**：
1. 感知到的物件。
2. 類別定義。
3. 可負性表示。
4. 推理模式。
5. 推導出的可抓取性。
6. 可查詢的結果。

這個閉環使得物件知識變得明確，從而在機器人學習管線（robot learning pipeline）中是可檢查、可重用且可討論的。

---

## 附錄：課程本體論的 SKOS 對齊 (Appendix: SKOS Alignment for the Course Ontology)

SKOS（Simple Knowledge Organization System，簡單知識組織系統）是 W3C 用於表示概念體系、標籤、定義、註釋以及術語之間映射關係的詞彙。在本附錄中，SKOS 被用作一個輕量級的概念建模層，用於將選定的課程本體論術語與來自現有機器人或基礎本體論的術語聯繫起來。當目標是語意可追溯性而非完全 OWL 級別的公理化或推理對齊時，此用法是合適的。

因此，下方的映射應被理解為概念對齊和文件連結。它們澄清了教育性詞彙如何與更廣泛的本體論工程術語相關聯，而無需課程本體論重現外部本體論系統的完整正式承諾。

### 正式詮釋 (Formal Interpretation)
令 $C$ 為課程本體論術語集，$E$ 為外部本體論術語集。一個輕量級的對齊關係可以表示為：

$$align \subseteq C \times R_{SKOS} \times E$$

其中：

$$R_{SKOS} = \{exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch\}$$

對於課程術語 $c \in C$、外部術語 $e \in E$ 以及 SKOS 映射關係 $r \in R_{SKOS}$，一個對齊斷言的格式為：
`align(c, r, e).`

例如：
`align(cap:RobotAgent, skos:closeMatch, cora:Robot).`

此斷言應被理解為課程術語與外部術語之間的語意交叉引用。以下對 SKOS 映射的詮釋將是**錯誤**的：
`cap:RobotAgent ≡ cora:Robot.` （錯誤）

同樣地：
`align(cap:GraspingAffordance, skos:relatedMatch, soma:Grasping)`
並不暗示類別等效。它僅表明課程級別的抓取可負性概念與用於操作導向本體論建模的外部術語在概念上相關。

### 建模原則 (Modeling Principle)
課程本體論刻意小於其所引用的外部本體論系統。因此，SKOS 映射應被解釋為文檔級別的對齊，而非 OWL 類別公理。特別是，僅當兩個映射術語具有可證明的等價含義和相容的身份條件時，才應使用 `skos:exactMatch`。對於本作業，大多數映射應使用 `skos:closeMatch`、`skos:broadMatch` 或 `skos:relatedMatch`。

這些映射不決定本作業的 OWL 推理行為。它們提供對外部術語的可追溯性，而本地 OWL 公理定義了諸如 `cap:GraspableObject` 等術語所需的分類行為。

### 命名空間宣告 (Namespace Declarations)

**Listing 10: 外部本體論命名空間**
```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix cora: <http://purl.org/ieee1872-owl/cora-bare#> .
@prefix sumocora: <http://purl.org/ieee1872-owl/sumo-cora#> .
@prefix soma: <http://www.ease-crc.org/ont/SOMA.owl#> .
@prefix dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#> .
@prefix corax: <http://purl.org/ieee1872-owl/corax#> .
@prefix knowrob: <http://knowrob.org/kb/knowrob.owl#> .
```

### SKOS 對齊範例 (Example SKOS Alignment)
Listing 11 顯示了用於課程本體論的 SKOS 對齊摘錄。該摘錄說明了如何記錄所選課程術語並將其與外部本體論詞彙聯繫起來。完整的對齊檔案位於：`course-alignment.ttl`。

**Listing 11: 所選課程本體論術語之 SKOS 對齊摘錄**
```turtle
cap:RobotAgent
    skos:prefLabel "robot agent"@en ;
    skos:definition "A robot or robot-controlled agent that can perceive, reason about, and manipulate objects in the task environment."@en ;
    skos:closeMatch cora:Robot ;
    skos:relatedMatch sumocora:Agent ;
    skos:scopeNote "The course term is aligned with CORA at the level of robot-as-agent or robot-as-system. It remains locally defined for the purposes of this homework."@en .

cap:ManipulationTask
    skos:prefLabel "manipulation task"@en ;
    skos:definition "A robot task in which an agent changes the pose, state, or arrangement of physical objects."@en ;
    skos:broadMatch dul:Task ;
    skos:relatedMatch soma:Manipulating ;
    skos:scopeNote "The course term covers the project tasks, including cup stacking, cutlery arrangement, and toy block collection."@en .

cap:GraspingAffordance
    skos:prefLabel "grasping affordance"@en ;
    skos:definition "An affordance by which an object can be grasped, held, lifted, or repositioned by a robot gripper."@en ;
    skos:relatedMatch soma:Disposition ;
    skos:relatedMatch soma:Grasping ;
    skos:scopeNote "The course term is represented locally as an affordance class. SOMA models affordance-like knowledge through dispositions and task-oriented action descriptions; therefore relatedMatch is used rather than exactMatch."@en .

# ... 省略了額外的對齊；請參閱完整的對齊檔案。
```

---

## 參考文獻 (References)

[1] W3C RDF Working Group, *RDF 1.1 Turtle: Terse RDF Triple Language*, W3C Recommendation, 2014. [Online]. Available: https://www.w3.org/TR/turtle/.

[2] W3C OWL Working Group, *OWL 2 Web Ontology Language Document Overview*, W3C Recommendation, 2012. [Online]. Available: https://www.w3.org/TR/owl2-overview/.

[3] W3C OWL Working Group, *OWL 2 Web Ontology Language Primer*, W3C Recommendation, 2012. [Online]. Available: https://www.w3.org/TR/owl2-primer/.

[4] W3C SPARQL Working Group, *SPARQL 1.1 Query Language*, W3C Recommendation, 2013. [Online]. Available: https://www.w3.org/TR/sparql11-query/.

[5] IEEE Standards Association, *IEEE 1872-2015: IEEE Standard Ontologies for Robotics and Automation*, IEEE Standard, 2015. [Online]. Available: https://standards.ieee.org/standard/1872-2015.html.

[6] IEEE Standards Association, *IEEE 1872.2-2021: IEEE Standard for Autonomous Robotics Ontology*, IEEE Standard, 2021.

[7] EASE CRC, *SOMA: Socio-physical Model of Activities Documentation*, Ontology documentation, 2026. [Online]. Available: https://ease-crc.github.io/soma/.

[8] M. Tenorth and M. Beetz, “KnowRob: A Knowledge Processing Infrastructure for Cognition-enabled Robots,” *The International Journal of Robotics Research*, vol. 32, no. 5, pp. 566–590, 2013. doi: 10.1177/0278364913481635.

[9] M. Beetz, D. Beßler, A. Haidu, M. Pomarlan, A. K. Bozcuoglu, and G. Bartels, “KnowRob 2.0: A 2nd Generation Knowledge Processing Framework for Cognition-enabled Robotic Agents,” in *2018 IEEE International Conference on Robotics and Automation (ICRA)*, 2018, pp. 512–519. doi: 10.1109/ICRA.2018.8460964.

[10] The HermiT Development Team, *HermiT OWL Reasoner*, http://www.hermit-reasoner.com/, OWL 2 DL reasoner.

[11] The Apache Software Foundation, *Reasoners and Rule Engines: Jena Inference Support*, https://jena.apache.org/documentation/inference/, Apache Jena documentation.

[12] Apache Jena Project, *Apache Jena Documentation*, Project documentation, 2026. [Online]. Available: https://jena.apache.org/documentation/.
