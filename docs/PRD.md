# Product Requirements Document (PRD) – Idea Spark

**Project:** Idea Spark  
**Repository:** `idea-spark`  
**Owner:** Axentx OS Product Team  
**Last Updated:** 2026‑06‑24  

---

## 1. Problem Statement

Axentx OS relies on a tightly‑coordinated pipeline to turn market signals into revenue‑validated products.  
However:

1. **Idea Visibility** – Validated ideas are scattered across email, Slack, and ad‑hoc spreadsheets, making it hard to see the entire pipeline.
2. **Conversion Tracking** – There is no automated way to measure how many ideas convert into shipped products within the 90‑day window that the company uses to gauge product viability.
3. **Performance Analysis** – Team members lack a single source of truth for North‑Star‑Metric (NSM) reporting, leading to ad‑hoc analyses and delayed decision‑making.

Without a unified tracker, the company risks duplicating effort, missing high‑impact ideas, and losing the ability to prove ROI on its product development process.

---

## 2. Target Users

| Persona | Role | Pain Points | How Idea Spark Helps |
|---------|------|-------------|----------------------|
| **Product Manager (PM)** | Owns the product backlog | Needs a clear view of idea status and conversion metrics | Provides a single view of ideas, validation status, and 90‑day conversion rates |
| **Reviewers / QA Leads** | Gatekeepers of quality | Must verify that ideas meet quality gates before moving forward | Automatic status updates and alerts when an idea fails a gate |
| **Data Analysts** | Build performance dashboards | Requires clean, aggregated data for NSM reports | Generates ready‑made NSM reports and exportable datasets |
| **Engineering Leads** | Manage implementation | Needs to see which ideas are in the pipeline to allocate resources | Links ideas to pipeline stages and tracks progress automatically |
| **Executive Leadership** | Makes strategic decisions | Needs high‑level metrics on pipeline health | Provides NSM dashboards and trend analyses |

---

## 3. Goals & Objectives

| Goal | Success Metric | Target |
|------|----------------|--------|
| **Centralize Idea Visibility** | % of ideas tracked in Idea Spark | 100% of validated ideas |
| **Automate 90‑Day Conversion Tracking** | % of ideas that convert within 90 days | ≥ 70% |
| **Enable Data‑Driven Decisions** | Frequency of NSM report usage | ≥ 5 reports per month |
| **Reduce Duplicate Effort** | % of duplicated ideas identified | ≤ 5% |
| **Improve Time‑to‑Validation** | Average days from idea submission to validation | ≤ 14 days |

---

## 4. Key Features (Prioritized)

| # | Feature | Description | Priority | Dependencies |
|---|---------|-------------|----------|--------------|
| 1 | **Idea Ingestion & Validation Status** | Users can submit ideas via a web form or API. Each idea is tagged with validation status (Pending, Validated, Rejected). | P1 | Axentx OS BRAIN (pgvector) |
| 2 | **Pipeline Stage Linking** | Each idea is automatically linked to the corresponding stage in the Axentx OS pipeline (HR/BD, PM/PRD, Architect, Dev, QA, Reviewer). | P1 | Existing pipeline data models |
| 3 | **Automated 90‑Day Conversion Tracker** | The system calculates the time from validation to shipping, flags ideas that exceed 90 days, and sends alerts. | P1 | Timestamp fields in pipeline stages |
| 4 | **NSM Dashboard & Report Generator** | Generates North‑Star‑Metric reports (e.g., conversion rate, time‑to‑validation, revenue impact) with visualizations and export options (CSV, PDF). | P2 | Data aggregation layer |
| 5 | **Role‑Based Access Control** | Only authorized users can view or edit ideas based on their role. | P2 | Authentication & RBAC |
| 6 | **Notification System** | Email/SMS alerts for status changes, 90‑day thresholds, and NSM report availability. | P3 | Email/SMS service |
| 7 | **Audit Trail & Versioning** | Keeps a history of changes to each idea for compliance and analysis. | P3 | Database logging |
| 8 | **Integration with Axentx OS BRAIN** | Pulls and pushes data to the shared BRAIN for cross‑product insights. | P4 | pgvector API |

---

## 5. Success Metrics

| Metric | Definition | Target | Measurement Tool |
|--------|------------|--------|------------------|
| **Idea Coverage** | % of validated ideas present in Idea Spark | 100% | Database query |
| **Conversion Rate** | % of ideas that ship within 90 days | ≥ 70% | Dashboard KPI |
| **Time‑to‑Validation** | Avg. days from idea submission to validation | ≤ 14 days | Analytics |
| **NSM Report Utilization** | Number of reports generated per month | ≥ 5 | Logging |
| **Duplicate Detection** | % of ideas flagged as duplicates | ≤ 5% | Duplicate detection algorithm |
| **User Adoption** | % of target users actively using the system | ≥ 80% | User analytics |

---

## 6. Scope

### In Scope
- Web UI for idea submission, status tracking, and NSM dashboards.
- REST API for programmatic ingestion and status updates.
-
