---
doc_id: R-13
doc_name: Glossary
phase: Cross-cutting
required_when: Required for all scales and methodologies
depends_on: []
mode: Both
---

# {{Project Name}} - Glossary

## 1. Purpose
Unify the meaning of terms used across the project and prevent ambiguity and inconsistent notation.
Other documents must first register any business / domain term in this glossary before using it (CLAUDE.md rule #4).
When DDD is adopted, this glossary serves as the **Ubiquitous Language** and must align with DM-1 (Domain Model).

## 2. Scope
- In scope: {{Business terms, domain terms, abbreviations, synonym disambiguation}}
- Out of scope: {{General technical terms like programming language grammar terms (register only when truly needed)}}

## 3. Prerequisites & Dependencies
- Reference documents: None (cross-cutting / topmost)
- Already-issued IDs: None (terms themselves serve as the primary key, no separate ID)

## 4. Body

### 4.1 Terms
| Term | Pronunciation | Meaning | Synonym / Variant | Forbidden Words | Translation (ja) | First Appearance |
|---|---|---|---|---|---|---|
| {{term}} | {{pronunciation}} | {{business meaning}} | {{synonym}} | {{forbidden similar terms}} | {{Japanese translation}} | {{originating doc ID}} |
| Order | order | A request from a customer that has been registered but not yet confirmed. | — | "request" (use "order" in this project) | 受注 | R-1 |
| Confirmed Order | — | An order whose inventory has been allocated and payment completed; ready for shipment. | — | — | 受注確定 | R-8 |

### 4.2 Abbreviations
| Abbreviation | Full Form | Meaning |
|---|---|---|
| {{abbreviation}} | {{full spelling}} | {{meaning}} |
| MFA | Multi-Factor Authentication | — |
| RTM | Requirements Traceability Matrix | — |

### 4.3 Notation Rules
- One canonical spelling per concept; do not mix variants (e.g., do not use "customer" and "client" interchangeably).
- The first occurrence of an abbreviation must include the full spelling in parentheses.
- Industry regulations and laws: write the formal name first, then the abbreviation is allowed (e.g., "General Data Protection Regulation (GDPR)").

## 5. Traceability
- Upstream: None (cross-cutting / topmost)
- Downstream (documents that reference this glossary): **All documents** / especially B-12 Logical ER / DM-1 Domain Model (entity names must match the glossary).

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

> | Term | Pronunciation | Meaning | Translation (ja) |
> |---|---|---|---|
> | Order | order | A request from a customer that has been registered but not yet confirmed. | 受注 |
> | Confirmed Order | — | An order whose inventory has been allocated and payment completed; ready for shipment. | 受注確定 |
