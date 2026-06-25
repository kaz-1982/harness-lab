---
doc_id: R-9
doc_name: Non-Functional Requirements Definition
phase: Requirements
required_when: Required for all scales and methodologies
depends_on: [R-1]
mode: Both
---

# {{Project Name}} - Non-Functional Requirements Definition

## 1. Purpose
Define quality characteristics (performance, availability, security, etc.) in **measurable / verifiable form** (no fuzzy adjectives).
This document references ISO/IEC 25010 (product quality model) or IPA's non-functional requirement grade.
Each requirement is realized in B-1 (System Architecture) / B-19 (Security Design).

## 2. Scope
- In scope: {{Quality characteristics across the eight ISO/IEC 25010 categories for this system}}
- Out of scope: {{Quality of external systems; organizational operations not owned by this project}}

## 3. Prerequisites & Dependencies
- Reference documents: R-1 Business Requirements; R-12 Constraints (if available)
- Already-issued IDs: R-NF-* assigned in this document
- Referenced standards: ISO/IEC 25010, IPA Non-Functional Requirement Grade

## 4. Body

> Each characteristic must include a **numeric target** (vague adjectives like "fast" or "high" are not acceptable).

### 4.1 Functional Suitability
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-001 | Functional completeness | {{e.g., 100% of acceptance tests for all F-* pass}} | {{e.g., TS-1 AT-* all green}} |

### 4.2 Performance Efficiency
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-010 | Response time | {{e.g., 95%tile of screen response within 2 seconds}} | {{e.g., APM tool in production}} |
| R-NF-011 | Throughput | {{e.g., 500 concurrent users at peak}} | {{e.g., load test}} |
| R-NF-012 | Resource efficiency | {{e.g., average CPU usage <= 60%}} | {{monitoring metrics}} |

### 4.3 Compatibility
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-020 | Co-existence | {{e.g., can run on the same server as existing ERP}} | {{}} |
| R-NF-021 | Interoperability | {{e.g., external APIs conform to OpenAPI 3.0}} | {{}} |

### 4.4 Usability
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-030 | Learnability | {{e.g., new users complete order operation within 30 minutes}} | {{UX testing}} |
| R-NF-031 | Accessibility | {{e.g., WCAG 2.1 AA conformance}} | {{}} |

### 4.5 Reliability
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-040 | Availability | {{e.g., 99.9% uptime on weekdays 9-18}} | {{monitoring log aggregation}} |
| R-NF-041 | Fault tolerance | {{e.g., MTTR <= 1 hour, RPO 15 min, RTO 4 hours}} | {{}} |
| R-NF-042 | Recoverability | {{e.g., restore from backup within 2 hours}} | {{}} |

### 4.6 Security
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-050 | Confidentiality | {{e.g., all communications TLS 1.3+, PII encrypted at rest with AES-256}} | {{}} |
| R-NF-051 | Integrity | {{e.g., audit log retained 7 years, tamper detection via hash chain}} | {{}} |
| R-NF-052 | Authentication | {{e.g., password bcrypt(cost=12), MFA required}} | {{}} |

### 4.7 Maintainability
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-060 | Testability | {{e.g., unit test coverage C0 80%+}} | {{}} |
| R-NF-061 | Modularity | {{e.g., public API changes do not cascade across modules}} | {{}} |

### 4.8 Portability
| ID | Aspect | Target | Measurement |
|---|---|---|---|
| R-NF-070 | Adaptability | {{e.g., can migrate cloud provider X→Y within 1 month}} | {{}} |

## 5. Traceability
- Upstream (basis of this document): R-1 Business Requirements; R-12 Constraints (if available)
- Downstream (designs / tests that reference this document):
  - B-1 System Architecture (realization of each R-NF-*)
  - B-2 Software Architecture
  - B-17 Operations Design (availability / reliability runtime concerns)
  - B-19 Security Design (realization of R-NF-050~052)
  - R-14 RTM

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

> - Reliability: 99.9% uptime on weekdays 9-18, MTTR within 1 hour, RPO 15 min, RTO 4 hours
> - Performance: 500 concurrent users at peak, 95%tile screen response within 2 seconds
> - Security: All communications TLS 1.3+, password bcrypt(cost=12), audit log retained 7 years
