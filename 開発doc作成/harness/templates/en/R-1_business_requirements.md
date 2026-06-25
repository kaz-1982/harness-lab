---
doc_id: R-1
doc_name: Business Requirements Definition
phase: Requirements
required_when: Required for all scales and methodologies
depends_on: [PR-1]
mode: Both
---

# {{Project Name}} - Business Requirements Definition

## 1. Purpose
Define the business requirements (i.e., what the requesting business unit wants) without introducing system-level concerns.
This document is the first agreement point between the requester and the development team, and serves as the basis for all downstream functional / non-functional requirements and design decisions.

## 2. Scope
- In scope: {{Target business scope. e.g., Monthly AR aggregation for domestic corporate customers in the accounting department}}
- Out of scope: {{e.g., Overseas customers, individual customers, accounts payable, payroll}}

## 3. Prerequisites & Dependencies
- Reference documents:
  - PR-1 Pre-study Summary (if available; source of "problem → cause → countermeasure → candidate requirements")
  - R-13 Glossary (register business terms used in this document)
- Already-issued IDs: {{Business requirement IDs R-B-* assigned in this document. See §4.5}}

## 4. Body

### 4.1 Business Purpose & Background
{{Why is the business systemized? Describe the underlying management challenge / KPI miss / regulatory change in 1-3 paragraphs.}}

### 4.2 Target Business Scope
{{Specify the boundary of the target business using 4W1H (who / when / where / what / how much). Make "in scope" and "out of scope" explicit.}}

### 4.3 Business Process Overview
{{List the current (As-Is) business process as numbered steps. If BPR is involved, visualize in R-2 (business flow diagram).}}

### 4.4 Business Rules
{{Rules for business judgments and exceptions. Write them in IF-THEN form so that conditions and outcomes are explicit.}}

### 4.5 Business KPIs & Success Criteria (Business Requirement IDs R-B-*)
| ID | Business Requirement | Current Value | Target Value | Measurement |
|---|---|---|---|---|
| R-B-001 | {{the requirement sentence}} | {{current}} | {{target}} | {{how to measure}} |

### 4.6 Stakeholders
{{List the primary stakeholders. If R-15 (Stakeholder Register) is being authored, keep this section concise and reference it.}}

## 5. Traceability
- Upstream (basis of this document):
  - PR-1 Pre-study Summary (if available)
  - Management policy / business plan (reference)
- Downstream (designs / tests that reference this document):
  - R-7 User Stories (Agile) or R-8 Functional Requirements Specification (WF)
  - R-9 Non-Functional Requirements
  - R-14 RTM (track from each R-B-* downstream)

## 6. Revision History
| Rev | Date | Author | Changes |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | | Initial draft |

## 7. Review Status
- Single-document quality check: Not done / Done (YYYY-MM-DD)
- Consistency check: Not done / Done (YYYY-MM-DD)
- TBD / Open items:
  - (none, or bullet list)
- Approval: Not approved / Approved (approver, date)

---

### Appendix: Example (for reference)

> "In the monthly closing process of the accounting department, the AR aggregation, which currently takes 5 business days, shall be completed within 1 business day by the new system. The scope is limited to AR management for domestic corporate customers; overseas corporations and individual customers are out of scope."
