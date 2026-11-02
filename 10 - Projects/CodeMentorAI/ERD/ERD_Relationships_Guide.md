# CodeMentorAI — Complete ERD Relationship & Crow's Foot Guide

This guide provides the authoritative blueprint for connecting all **27 tables** in `Drawio.md` according to the live Supabase database schema (`Schema.md`) and project architectural standards.

---

## 1. ERD Notation & Syntax Quick Reference

### 1.1 Line Types: Identifying vs. Non-Identifying

| Line Type | Visual Style | Database Concept | When to Use | Draw.io XML Style |
| :--- | :---: | :--- | :--- | :--- |
| **Identifying Relationship** | **Solid Line** (`————`) | Child identity depends on the parent. | The parent's Primary Key (PK) forms **part of or all of the child's Primary Key**. | `dashed=0;` |
| **Non-Identifying Relationship** | **Broken / Dashed Line** (`- - - -`) | Child possesses its own independent identity. | The child table has its own independent surrogate PK (e.g. UUID); the parent's PK is merely a foreign key (FK) attribute. | `dashed=1;` |

---

### 1.2 Crow's Foot Modality & Cardinality Symbols

| Symbol | Draw.io Arrowhead Name | Cardinality Text | Meaning | Rule in Supabase Schema |
| :---: | :--- | :--- | :--- | :--- |
| **`\|\|`** | `ERone` / `ERmandOne` | **Exactly One** *(One and only one)* | Mandatory parent or child; must exist exactly once. | Foreign key column is `NOT NULL` and required. |
| **`O\|`** | `ERzeroToOne` | **Zero or One** *(Optional one)* | Optional single record; either exists once or not at all. | Foreign key column is `NULLABLE` (or optional 1:1 subtype). |
| **`O{`** | `ERzeroToMany` | **Zero or Many** *(Optional many)* | Zero, one, or multiple related records can exist. | Standard 1:N relationship (e.g. a user may have 0 or many submissions). |
| **`\|{`** | `ERoneToMany` | **One or Many** *(Mandatory many)* | At least one related child record must exist. | Mandatory child composition (e.g. an assessment must have $\ge 1$ challenge). |

---

## 2. Master Domain Connection Catalog

---

### Cluster 1: User Identity, Profiles, Wallets & Streaks

```
Profiles (1) ----<0..1> Mentor_Profiles
Profiles (1) ----<0..1> User_Wallets
Profiles (1) ----<0..1> User_Streaks
Profiles (1) ----<0..N> Coin_Transactions
Profiles (1) ----<0..N> Notifications
```

#### 1.1 `Profiles` $\to$ `Mentor_Profiles`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Mentor_Profiles.User_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: `Mentor_Profiles` has its own surrogate `Ment_Id` PK)*.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Mentor_Profiles` $\to$ **`O|` Zero or One** (`endArrow=ERzeroToOne;`)
* **Relationship Type**: **1:1 Optional Subtype**
* **Verb / Center Label**: **`registers as`**
* **Natural Reading**:
  * *Forward*: One `Profile` optionally **registers as** Zero or One `Mentor_Profile`.
  * *Reverse*: A `Mentor_Profile` belongs to **Exactly One** `Profile`.

#### 1.2 `Profiles` $\to$ `User_Wallets`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `User_Wallets.User_Id` (or `Uwl_Id`)
* **Line Type**: **Solid Line** (`dashed=0;`) if `User_Id` is PK in DB; **Broken Line** (`dashed=1;`) if using surrogate `Uwl_Id`.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `User_Wallets` $\to$ **`||` Exactly One** (or **`O|` Zero or One**) (`endArrow=ERmandOne;` or `ERzeroToOne;`)
* **Relationship Type**: **1:1 Identifying Extension**
* **Verb / Center Label**: **`owns`**
* **Natural Reading**:
  * *Forward*: One `Profile` **owns** Exactly One `User_Wallet`.
  * *Reverse*: A `User_Wallet` is owned by **Exactly One** `Profile`.

#### 1.3 `Profiles` $\to$ `User_Streaks`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `User_Streaks.User_Id` (or `Ust_Id`)
* **Line Type**: **Solid Line** (`dashed=0;`) if `User_Id` is PK in DB; **Broken Line** (`dashed=1;`) if using surrogate `Ust_Id`.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `User_Streaks` $\to$ **`||` Exactly One** (or **`O|` Zero or One**) (`endArrow=ERmandOne;` or `ERzeroToOne;`)
* **Relationship Type**: **1:1 Identifying Extension**
* **Verb / Center Label**: **`maintains`**
* **Natural Reading**:
  * *Forward*: One `Profile` **maintains** Exactly One `User_Streak`.
  * *Reverse*: A `User_Streak` is tracked for **Exactly One** `Profile`.

#### 1.4 `Profiles` $\to$ `Coin_Transactions`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Coin_Transactions.User_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Coin_Transactions` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`generates`**
* **Natural Reading**:
  * *Forward*: One `Profile` **generates** Zero or Many `Coin_Transactions`.
  * *Reverse*: A `Coin_Transaction` is credited/debited to **Exactly One** `Profile`.

#### 1.5 `Profiles` $\to$ `Notifications`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Notifications.User_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Notifications` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`receives`**
* **Natural Reading**:
  * *Forward*: One `Profile` **receives** Zero or Many `Notifications`.
  * *Reverse*: A `Notification` is addressed to **Exactly One** `Profile`.

---

### Cluster 2: Learning Modules, Topics & Practice Activities

```
Mentor_Profiles (0..1) ----<0..N> Modules
Profiles (0..1) -----------<0..N> Modules (Edit Unlock)
Modules (1) ---------------<0..N> Topics
Topics (0..1) -------------<0..N> Activities
Modules (0..1) ------------<0..N> Activities (Direct Module Scope)
Activities (1) ------------<0..1> Code_Details (IDENTIFYING)
Activities (1) ------------<0..N> Test_Cases
Profiles (0..1) -----------<0..N> Activities (Edit Unlock)
```

#### 2.1 `Mentor_Profiles` $\to$ `Modules`
* **Connection**: `Mentor_Profiles.Ment_Id` (or `Profiles.User_Id`) $\longrightarrow$ `Modules.Ment_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Mentor_Profiles` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`) *(mentor is optional/nullable in DB)*.
* **Child Side**: `Modules` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`authors`**
* **Natural Reading**:
  * *Forward*: A `Mentor_Profile` **authors** Zero or Many `Modules`.
  * *Reverse*: A `Module` is authored by **Zero or One** `Mentor_Profile`.

#### 2.2 `Profiles` $\to$ `Modules` (Edit Unlock)
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Modules.Edit_Unlocked_By`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: nullable audit FK)*.
* **Parent Side**: `Profiles` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Modules` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N Optional Reference**
* **Verb / Center Label**: **`unlocks editing for`**
* **Natural Reading**:
  * *Forward*: An Admin `Profile` optionally **unlocks editing for** Zero or Many `Modules`.
  * *Reverse*: A `Module` is unlocked by **Zero or One** Admin `Profile`.

#### 2.3 `Modules` $\to$ `Topics`
* **Connection**: `Modules.Mod_Id` $\longrightarrow$ `Topics.Mod_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: Topics has its own UUID PK)*.
* **Parent Side**: `Modules` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Topics` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`outlines` / `contains`**
* **Natural Reading**:
  * *Forward*: One `Module` **outlines** Zero or Many `Topics`.
  * *Reverse*: A `Topic` belongs to **Exactly One** `Module`.

#### 2.4 `Topics` $\to$ `Activities`
* **Connection**: `Topics.Topic_Id` $\longrightarrow$ `Activities.Topic_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: topic_id is nullable for standalone activities)*.
* **Parent Side**: `Topics` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Activities` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`organizes`**
* **Natural Reading**:
  * *Forward*: One `Topic` **organizes** Zero or Many `Activities`.
  * *Reverse*: An `Activity` is organized under **Zero or One** `Topic`.

#### 2.5 `Modules` $\to$ `Activities` (Direct Scope)
* **Connection**: `Modules.Mod_Id` $\longrightarrow$ `Activities.Mod_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Modules` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Activities` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`encompasses`**
* **Natural Reading**:
  * *Forward*: One `Module` **encompasses** Zero or Many `Activities`.
  * *Reverse*: An `Activity` belongs to **Zero or One** `Module`.

#### 2.6 `Activities` $\to$ `Code_Details`
* **Connection**: `Activities.Act_Id` $\longrightarrow$ `Code_Details.Cdt_Item_Id`
* **Line Type**: **SOLID LINE (`dashed=0;`)** — **IDENTIFYING RELATIONSHIP**
  * *Reason*: `Cdt_Item_Id` is both the **Primary Key and Foreign Key** referencing `Activities.Act_Id`. `Code_Details` has no surrogate key and cannot exist without an `Activity`.
* **Parent Side**: `Activities` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Code_Details` $\to$ **`O|` Zero or One** (`endArrow=ERzeroToOne;`)
* **Relationship Type**: **1:1 Identifying Extension**
* **Verb / Center Label**: **`specifies parameters for`**
* **Natural Reading**:
  * *Forward*: One `Activity` **specifies parameters for** Zero or One `Code_Details`.
  * *Reverse*: A `Code_Details` record configures execution for **Exactly One** `Activity`.

#### 2.7 `Activities` $\to$ `Test_Cases`
* **Connection**: `Activities.Act_Id` $\longrightarrow$ `Test_Cases.Act_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Activities` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Test_Cases` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`tests with`**
* **Natural Reading**:
  * *Forward*: One `Activity` **tests with** Zero or Many `Test_Cases`.
  * *Reverse*: A `Test_Case` validates execution of **Exactly One** `Activity`.

#### 2.8 `Profiles` $\to$ `Activities` (Edit Unlock)
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Activities.Edit_Unlocked_By`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Profiles` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Activities` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N Optional Reference**
* **Verb / Center Label**: **`unlocks editing for`**

---

### Cluster 3: Practice Engagement, Bookmarks & Reviews

```
Profiles (1) =======<0..N> User_Module_Progress (IDENTIFYING)
Modules (1) ========<0..N> User_Module_Progress (IDENTIFYING)
Profiles (1) =======<0..N> User_Module_Saves (IDENTIFYING)
Modules (1) ========<0..N> User_Module_Saves (IDENTIFYING)
Profiles (1) -------<0..N> Module_Reviews
Modules (1) --------<0..N> Module_Reviews
Modules (1) --------<0..N> Module_Reports
Profiles (0..1) ----<0..N> Module_Reports (Reporter)
Profiles (0..1) ----<0..N> Module_Reports (Resolver)
Activities (0..1) --<0..N> Module_Reports (Target Activity)
```

#### 3.1 & 3.2 `Profiles` & `Modules` $\to$ `User_Module_Progress`
* **Connection 1**: `Profiles.User_Id` $\longrightarrow$ `User_Module_Progress.User_Id`
* **Connection 2**: `Modules.Mod_Id` $\longrightarrow$ `User_Module_Progress.Mod_Id`
* **Line Type**: **SOLID LINES (`dashed=0;`)** — **IDENTIFYING RELATIONSHIP**
  * *Reason*: The table uses a **composite primary key `(user_id, track_id)`**. Both foreign keys comprise the primary key.
* **Parent Sides**: `Profiles` / `Modules` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `User_Module_Progress` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **M:N via Identifying Composite Bridge**
* **Verb / Center Label**:
  * *Profiles $\to$ Progress*: **`tracks practice in`**
  * *Modules $\to$ Progress*: **`records completion of`**
* **Natural Reading**:
  * *Profiles*: One `Profile` **tracks practice in** Zero or Many `User_Module_Progress` records.
  * *Modules*: One `Module` **records completion of** Zero or Many `User_Module_Progress` records.

#### 3.3 & 3.4 `Profiles` & `Modules` $\to$ `User_Module_Saves`
* **Connection 1**: `Profiles.User_Id` $\longrightarrow$ `User_Module_Saves.User_Id`
* **Connection 2**: `Modules.Mod_Id` $\longrightarrow$ `User_Module_Saves.Mod_Id`
* **Line Type**: **SOLID LINES (`dashed=0;`)** — **IDENTIFYING RELATIONSHIP**
  * *Reason*: Composite primary key `(user_id, track_id)`.
* **Parent Sides**: `Profiles` / `Modules` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `User_Module_Saves` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **M:N via Identifying Composite Bridge**
* **Verb / Center Label**:
  * *Profiles $\to$ Saves*: **`bookmarks`**
  * *Modules $\to$ Saves*: **`is bookmarked in`**

#### 3.5 & 3.6 `Profiles` & `Modules` $\to$ `Module_Reviews`
* **Connection 1**: `Profiles.User_Id` $\longrightarrow$ `Module_Reviews.User_Id`
* **Connection 2**: `Modules.Mod_Id` $\longrightarrow$ `Module_Reviews.Mod_Id`
* **Line Type**: **Broken Lines** (`dashed=1;`) *(Non-identifying: has surrogate `Mrv_Id` PK)*.
* **Parent Sides**: `Profiles` / `Modules` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Module_Reviews` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**:
  * *Profiles $\to$ Reviews*: **`writes`**
  * *Modules $\to$ Reviews*: **`receives rating from`**

#### 3.7 to 3.10 `Module_Reports` References
* **`Modules.Mod_Id` $\longrightarrow$ `Module_Reports.Mod_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`is flagged by`**
* **`Profiles.User_Id` $\longrightarrow$ `Module_Reports.User_Id`** (Reporter):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`files`**
* **`Profiles.User_Id` $\longrightarrow$ `Module_Reports.Resolved_By`** (Resolver):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`resolves`**
* **`Activities.Act_Id` $\longrightarrow$ `Module_Reports.Act_Id`** (Target Activity):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`targets issue in`**

---

### Cluster 4: Code Submissions, Automated Audits & Mentor Feedback

```
Profiles (1) -------------<0..N> Submissions
Activities (1) -----------<0..N> Submissions
Submissions (1) ----------<0..1> Ai_Audits
Submissions (1) ----------<0..N> Submission_Feedbacks
Hubs (1) -----------------<0..N> Submission_Feedbacks
Mentor_Profiles (1) ------<0..N> Submission_Feedbacks
```

#### 4.1 `Profiles` $\to$ `Submissions`
* **Connection**: `Profiles.User_Id` $\longrightarrow$ `Submissions.User_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Submissions` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`submits code for`**
* **Natural Reading**:
  * *Forward*: One `Profile` **submits code for** Zero or Many `Submissions`.
  * *Reverse*: A `Submission` is executed by **Exactly One** `Profile`.

#### 4.2 `Activities` $\to$ `Submissions`
* **Connection**: `Activities.Act_Id` $\longrightarrow$ `Submissions.Act_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Activities` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Submissions` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`evaluates solution in`**
* **Natural Reading**:
  * *Forward*: One `Activity` **evaluates solution in** Zero or Many `Submissions`.
  * *Reverse*: A `Submission` attempts **Exactly One** `Activity`.

#### 4.3 `Submissions` $\to$ `Ai_Audits`
* **Connection**: `Submissions.Sub_Id` $\longrightarrow$ `Ai_Audits.Sub_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: Audit_Id is surrogate PK)*.
* **Parent Side**: `Submissions` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Ai_Audits` $\to$ **`O|` Zero or One** (`endArrow=ERzeroToOne;`)
* **Relationship Type**: **1:1 Optional Analysis**
* **Verb / Center Label**: **`is audited by`**
* **Natural Reading**:
  * *Forward*: One `Submission` **is audited by** Zero or One `Ai_Audit`.
  * *Reverse*: An `Ai_Audit` inspects code integrity for **Exactly One** `Submission`.

#### 4.4 to 4.6 `Submission_Feedbacks` Triad
* **`Submissions.Sub_Id` $\longrightarrow$ `Submission_Feedbacks.Sub_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`receives feedback via`**
* **`Hubs.Hub_Id` $\longrightarrow$ `Submission_Feedbacks.Hub_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`scopes review inside`**
* **`Mentor_Profiles.Ment_Id` (or `Profiles.User_Id`) $\longrightarrow$ `Submission_Feedbacks.Mentor_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`provides critique on`**

---

### Cluster 5: Coding Challenges & Benchmark Assessments

```
Mentor_Profiles (0..1) ---<0..N> Assessments
Profiles (0..1) ----------<0..N> Assessments (Edit Unlock)
Assessments (1) ----------<1..N> Assessment_Challenges
Activities (0..1) --------<0..N> Assessment_Challenges (Source Activity)
Profiles (0..1) ----------<0..N> Assessment_Challenges (Edit Unlock)
Profiles (1) -------------<0..N> User_Assessment_Saves
Assessments (1) ----------<0..N> User_Assessment_Saves
Assessments (1) ----------<0..N> Assessment_Reports
Profiles (0..1) ----------<0..N> Assessment_Reports (Reporter)
Profiles (0..1) ----------<0..N> Assessment_Reports (Resolver)
Assessment_Challenges (0..1) -<0..N> Assessment_Reports (Target Challenge)
```

#### 5.1 `Mentor_Profiles` $\to$ `Assessments`
* **Connection**: `Mentor_Profiles.Ment_Id` (or `Profiles.User_Id`) $\longrightarrow$ `Assessments.Ment_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Mentor_Profiles` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Assessments` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`curates`**
* **Natural Reading**:
  * *Forward*: A `Mentor_Profile` **curates** Zero or Many `Assessments`.
  * *Reverse*: An `Assessment` is curated by **Zero or One** `Mentor_Profile`.

#### 5.2 `Assessments` $\to$ `Assessment_Challenges`
* **Connection**: `Assessments.Asmt_Id` $\longrightarrow$ `Assessment_Challenges.Asmt_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: Ach_Id is surrogate PK)*.
* **Parent Side**: `Assessments` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Assessment_Challenges` $\to$ **`|{` One or Many** (`endArrow=ERoneToMany;`)
* **Relationship Type**: **1:N Mandatory Composition**
* **Verb / Center Label**: **`compiles / contains`**
* **Natural Reading**:
  * *Forward*: One `Assessment` **compiles** One or Many `Assessment_Challenges`.
  * *Reverse*: An `Assessment_Challenge` is a benchmark task in **Exactly One** `Assessment`.

#### 5.3 `Activities` $\to$ `Assessment_Challenges` (Source Activity)
* **Connection**: `Activities.Act_Id` $\longrightarrow$ `Assessment_Challenges.Source_Activity_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: source_activity_id is nullable)*.
* **Parent Side**: `Activities` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Assessment_Challenges` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N Optional Adaptation**
* **Verb / Center Label**: **`serves as template for`**
* **Natural Reading**:
  * *Forward*: One practice `Activity` optionally **serves as template for** Zero or Many `Assessment_Challenges`.
  * *Reverse*: An `Assessment_Challenge` is adapted from **Zero or One** practice `Activity`.

#### 5.4 & 5.5 `Profiles` & `Assessments` $\to$ `User_Assessment_Saves`
* **Connection 1**: `Profiles.User_Id` $\longrightarrow$ `User_Assessment_Saves.User_Id`
* **Connection 2**: `Assessments.Asmt_Id` $\longrightarrow$ `User_Assessment_Saves.Asmt_Id`
* **Line Type**: **Broken Lines** (`dashed=1;`) *(Non-identifying: has surrogate `Uas_Id` PK)*.
* **Parent Sides**: `Profiles` / `Assessments` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `User_Assessment_Saves` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**:
  * *Profiles $\to$ Saves*: **`saves to library`**
  * *Assessments $\to$ Saves*: **`is saved in library by`**

#### 5.6 to 5.9 `Assessment_Reports` References
* **`Assessments.Asmt_Id` $\longrightarrow$ `Assessment_Reports.Asmt_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`receives incident report`**
* **`Profiles.User_Id` $\longrightarrow$ `Assessment_Reports.User_Id`** (Reporter):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`flags`**
* **`Profiles.User_Id` $\longrightarrow$ `Assessment_Reports.Resolved_By`** (Resolver):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`resolves`**
* **`Assessment_Challenges.Ach_Id` $\longrightarrow$ `Assessment_Reports.Ach_Id`** (Target Challenge):
  * **Broken Line** (`dashed=1;`) | `O|` Zero or One $\to$ `O{` Zero or Many | **`is targeted in`**

---

### Cluster 6: Collaborative Hubs & Cohort Classrooms

```
Mentor_Profiles (1) -----<0..N> Hubs
Modules (0..1) ----------<0..N> Hubs (Primary Module)
Hubs (1) ----------------<0..N> Hub_Learners
Profiles (1) ------------<0..N> Hub_Learners
Hubs (1) ----------------<0..N> Hub_Invitations
Profiles (1) ------------<0..N> Hub_Invitations (Invited By)
Hubs (1) ----------------<0..N> Hub_Modules
Modules (1) -------------<0..N> Hub_Modules
Hubs (1) ----------------<0..N> Hub_Assessments
Assessments (1) ---------<0..N> Hub_Assessments
```

#### 6.1 `Mentor_Profiles` $\to$ `Hubs`
* **Connection**: `Mentor_Profiles.Ment_Id` (or `Profiles.User_Id`) $\longrightarrow$ `Hubs.Ment_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying)*.
* **Parent Side**: `Mentor_Profiles` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Hubs` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N (One to Many)**
* **Verb / Center Label**: **`manages / hosts`**
* **Natural Reading**:
  * *Forward*: One `Mentor_Profile` **manages** Zero or Many `Hubs`.
  * *Reverse*: A `Hub` is hosted by **Exactly One** `Mentor_Profile`.

#### 6.2 `Modules` $\to$ `Hubs` (Primary Module)
* **Connection**: `Modules.Mod_Id` $\longrightarrow$ `Hubs.Mod_Id`
* **Line Type**: **Broken Line** (`dashed=1;`) *(Non-identifying: primary_module_id is nullable)*.
* **Parent Side**: `Modules` $\to$ **`O|` Zero or One** (`startArrow=ERzeroToOne;`)
* **Child Side**: `Hubs` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **1:N Optional Anchor**
* **Verb / Center Label**: **`anchors as primary track for`**
* **Natural Reading**:
  * *Forward*: One `Module` optionally **anchors as primary track for** Zero or Many `Hubs`.
  * *Reverse*: A `Hub` designates **Zero or One** primary `Module`.

#### 6.3 & 6.4 `Hubs` & `Profiles` $\to$ `Hub_Learners` (`hub_members`)
> [!IMPORTANT]
> **CRITICAL ARCHITECTURAL FIX IN DRAWIO**:
> In your initial diagram, `Hub_Invitations` was connected to `Hub_Learners`.
> * Remove that connection. `Hub_Invitations` stores pending email invitations.
> * `Hub_Learners` records actual enrolled users and connects to **`Hubs`** and **`Profiles`**.

* **Connection 1**: `Hubs.Hub_Id` $\longrightarrow$ `Hub_Learners.Hub_Id`
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`enrolls member in`**
* **Connection 2**: `Profiles.User_Id` $\longrightarrow$ `Hub_Learners.User_Id`
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`participates as learner in`**
* **Relationship Type**: **M:N via Membership Bridge**
* **Natural Reading**:
  * *Hubs*: One `Hub` **enrolls member in** Zero or Many `Hub_Learners`.
  * *Profiles*: One `Profile` **participates as learner in** Zero or Many `Hub_Learners`.

#### 6.5 & 6.6 `Hub_Invitations` References
* **`Hubs.Hub_Id` $\longrightarrow$ `Hub_Invitations.Hub_Id`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`dispatches`**
* **`Profiles.User_Id` $\longrightarrow$ `Hub_Invitations.Invited_By`**:
  * **Broken Line** (`dashed=1;`) | `||` Exactly One $\to$ `O{` Zero or Many | **`sends invitation`**

#### 6.7 & 6.8 `Hubs` & `Modules` $\to$ `Hub_Modules`
* **Connection 1**: `Hubs.Hub_Id` $\longrightarrow$ `Hub_Modules.Hub_Id`
* **Connection 2**: `Modules.Mod_Id` $\longrightarrow$ `Hub_Modules.Mod_Id`
* **Line Type**: **Broken Lines** (`dashed=1;`) *(Non-identifying: has surrogate `Hmd_Id` PK)*.
* **Parent Sides**: `Hubs` / `Modules` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Hub_Modules` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **M:N Multi-Module Hub Assignment**
* **Verb / Center Label**:
  * *Hubs $\to$ Modules*: **`assigns`**
  * *Modules $\to$ Hubs*: **`is assigned to`**

#### 6.9 & 6.10 `Hubs` & `Assessments` $\to$ `Hub_Assessments`
* **Connection 1**: `Hubs.Hub_Id` $\longrightarrow$ `Hub_Assessments.Hub_Id`
* **Connection 2**: `Assessments.Asmt_Id` $\longrightarrow$ `Hub_Assessments.Asmt_Id`
* **Line Type**: **Broken Lines** (`dashed=1;`) *(Non-identifying: has surrogate `Has_Id` PK)*.
* **Parent Sides**: `Hubs` / `Assessments` $\to$ **`||` Exactly One** (`startArrow=ERone;`)
* **Child Side**: `Hub_Assessments` $\to$ **`O{` Zero or Many** (`endArrow=ERzeroToMany;`)
* **Relationship Type**: **M:N Hub Assessment Assignment**
* **Verb / Center Label**:
  * *Hubs $\to$ Assessments*: **`schedules`**
  * *Assessments $\to$ Hubs*: **`is scheduled inside`**

---

## 3. Draw.io Line Styling Copy-Paste Reference

To apply the exact line format in Draw.io / Diagrams.net, click on any connection line and paste the corresponding style into the right-hand **Style** tab:

### 3.1 Standard Non-Identifying 1:N (Broken Line, 1 to 0..N)
```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;startArrow=ERone;startFill=0;endArrow=ERzeroToMany;endFill=0;
```

### 3.2 Identifying Composite Bridge (Solid Line, 1 to 0..N)
*(Used for `User_Module_Progress` and `User_Module_Saves`)*
```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=0;startArrow=ERone;startFill=0;endArrow=ERzeroToMany;endFill=0;
```

### 3.3 Identifying 1:1 Subtype (Solid Line, 1 to 0..1)
*(Used for `Activities` $\to$ `Code_Details`)*
```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=0;startArrow=ERone;startFill=0;endArrow=ERzeroToOne;endFill=0;
```

### 3.4 Optional Parent to Many (Broken Line, 0..1 to 0..N)
*(Used for nullable parent keys like `Topic_Id` in `Activities`, or `Edit_Unlocked_By`)*
```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;startArrow=ERzeroToOne;startFill=0;endArrow=ERzeroToMany;endFill=0;
```
