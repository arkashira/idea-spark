## dataflow.md  

### System Dataflow Architecture for **idea‑spark**  

---  

#### 1. External Data Sources  
| Source | Type | Purpose | Access |
|--------|------|---------|--------|
| **OpenAI / Anthropic / Llama‑2 API** | LLM inference | Core idea‑generation & validation prompts | API‑Key (OAuth2‑Client‑Credentials) |
| **Product Hunt / Indie Hackers RSS & API** | Market trend feed | Real‑time hot‑topic extraction | Public API (rate‑limited) + API‑Key |
| **Google Trends / YouTube Trends API** | Trend analytics | Signal weighting for idea relevance | OAuth2 (service account) |
| **Domain‑specific knowledge bases** (e.g., Crunchbase, AngelList) | Structured data | Funding & competitor context | API‑Key |
| **User‑provided context** (CSV, JSON, URLs) | Upload | Seed data for niche‑specific brainstorming | JWT‑protected upload endpoint |
| **Web‑scraped public pages** (via Scrapy workers) | Unstructured text | Enrich idea corpus with niche blogs/articles | Internal service, obey robots.txt |

---

#### 2. Ingestion Layer  
- **API Gateway (Kong / AWS API GW)** – entry point, validates JWT/OAuth tokens, rate‑limits per‑user.  
- **Ingress Workers (Python/FastAPI)** – thin adapters for each external source:  
  - `llm_ingest.py` → forwards prompt payloads to LLM provider.  
  - `trend_ingest.py` → polls Google Trends, stores raw JSON.  
  - `ph_ingest.py` → pulls latest Product Hunt posts via webhook.  
- **Message Bus (Kafka topic: `raw_events`)** – decouples ingestion from downstream processing; retains ordering per source.  

**Auth Boundary:**  
All inbound calls must present a signed JWT issued by the **Auth Service** (see below). Invalid tokens are rejected at the API Gateway.

---

#### 3. Processing / Transform Layer  
| Component | Tech | Function |
|-----------|------|----------|
| **Stream Processor (Kafka Streams / Flink)** | Java/Scala | Normalises raw events, extracts fields, enriches with taxonomy (e.g., “AI‑tools”, “No‑code”). |
| **LLM Prompt Orchestrator (Celery + Redis)** | Python | Constructs multi‑turn prompts, calls LLM API, receives idea candidates. |
| **Idea Scoring Engine** | Python (NumPy, scikit‑learn) | Applies heuristic + ML model (XGBoost) on: trend score, market size, competition density, novelty. |
| **Validation Microservice** | FastAPI | Runs quick “fit‑check” simulations (e.g., TAM calculator, SEO difficulty). |
| **Audit Logger** | ElasticSearch | Immutable log of every prompt, response, and scoring decision for compliance. |

All processing services run inside a **Kubernetes namespace `idea-spark-prod`** with **NetworkPolicy** that only allows inbound traffic from the `raw_events` Kafka topic and outbound to the LLM providers.

**Auth Boundary:**  
Inter‑service calls use **mutual TLS (mTLS)**; service identities are managed by Istio’s SPIFFE IDs.

---

#### 4. Storage Tier  
| Store | Type | Data | Access Pattern |
|-------|------|------|----------------|
| **PostgreSQL (cloud‑native, read‑replicas)** | Relational | User profiles, saved idea sets, feedback scores | OLTP, strong consistency |
| **Redis (clustered)** | In‑memory KV | Session cache, short‑lived LLM responses (TTL 5 min) | Fast lookup |
| **S3‑compatible Object Store** | Blob | Raw PDFs, CSV uploads, exported idea decks | Bulk read/write |
| **Vector DB (Pinecone / Milvus)** | Approximate nearest‑neighbor | Embeddings of all generated ideas for similarity search | ANN queries |
| **ElasticSearch** | Full‑text | Audit logs, searchable idea metadata | Text search, analytics |

**Auth Boundary:**  
- DB credentials stored in **HashiCorp Vault**; pods retrieve via Vault Agent Injector.  
- S3 bucket policies restrict to the `idea-spark-prod` IAM role.  

---

#### 5. Query / Serving Layer  
- **GraphQL API (Apollo Server)** – single endpoint for UI; resolves: `listIdeas`, `searchSimilar`, `getIdeaDetail`. Enforces field‑level RBAC based on JWT claims.  
- **REST Endpoints (FastAPI)** – for legacy integrations (e.g., Zapier).  
- **Cache Layer (Redis)** – caches top‑10 ideas per user for 2 min.  
- **Rate Limiter (Envoy)** – per‑user QPS caps (default 5 req/s).  

**Auth Boundary:**  
All requests must present a valid JWT; token introspection performed by **Auth Service** (Keycloak). Refresh tokens rotate every 12 h.

---

#### 6. Egress to User  
| Channel | Tech | Flow |
|---------|------|------|
| **Web UI (React + Vite)** | HTTPS (TLS 1.3) | Calls GraphQL → receives JSON, renders idea cards, allows “save” / “export”. |
| **Email Digest (SendGrid)** | SMTP API | Nightly summary of top‑ranked ideas, includes PDF attachment from S3. |
| **Slack Bot** | Bolt SDK | `/ideas generate <topic>` → triggers backend via webhook, returns formatted message. |
| **API Webhooks** | POST JSON | Users can register a webhook URL; system POSTs new idea payloads (signed with HMAC secret). |

**Auth Boundary:**  
- UI uses **OAuth2 Authorization Code Flow** with PKCE; tokens stored in HttpOnly Secure cookies.  
- Outbound webhooks are signed (HMAC‑SHA256) and include a timestamp to prevent replay.  

---  

### ASCII Block Diagram  

```
+-------------------+        +-------------------+        +-------------------+
|  External Sources |        |   Ingestion Layer|        | Processing Layer |
| (LLM, Trends, PH) |  -->   |  API GW + Workers|  -->   |  Stream Proc      |
+-------------------+        +-------------------+        +-------------------+
          |                           |                           |
          v                           v                           v
   +----------------+          +----------------+          +----------------+
   |  Kafka Topic   |<-------->|  Kafka Streams |<--------|  Celery Workers|
   | raw_events     |          | (norm/ enrich) |          | (prompt orch) |
   +----------------+          +----------------+          +----------------+
          |                           |                           |
          v                           v                           v
   +----------------+          +----------------+          +----------------+
   |  Storage Tier  |<-------->|  Vector DB     |<--------|  Scoring Engine|
   | (Postgres, S3,|          | (embeddings)   |          | (XGBoost)      |
   |  Redis, ES)   |          +----------------+          +----------------+
   +----------------+                  |                           |
          |                           |                           |
          v                           v                           v
   +----------------+          +----------------+          +----------------+
   | Query/Serving  |<-------->|  GraphQL API   |<--------|  Auth Service   |
   | (Apollo, Fast) |          | (RBAC)         |          | (Keycloak)      |
   +----------------+          +----------------+          +----------------+
          |                           |                           |
          v                           v                           v
   +----------------+          +----------------+          +----------------+
   |   Egress UI    |<-------->|  Web UI (React)|<--------|  User JWT       |
   | (Email, Slack) |          +----------------+          +----------------+
   +----------------+                                           
```

---  

**Key Security Controls**  

1. **Perimeter** – API GW enforces JWT + rate limits.  
2. **Zero‑Trust Internal** – mTLS + Istio NetworkPolicies.  
3. **Secret Management** – Vault‑driven DB/LLM credentials.  
4. **Data Privacy** – User‑uploaded files encrypted at rest (S3 SSE‑AES256).  
5. **Auditability** – Immutable logs in ElasticSearch, retained 90 days.  

---  

*End of `dataflow.md`*