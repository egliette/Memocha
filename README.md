# Memocha

**RAG-based Chatbot with Long-Term Memory**

## Todo List

---

## **Day 1 — Backend & Infrastructure (Completed)**

* [x] Repo setup, folders, Git
* [x] FastAPI project initialization
* [x] Health check endpoint
* [x] Environment configuration
* [x] Logging setup
* [x] PostgreSQL via Docker
* [x] SQLAlchemy models (Session, Message)
* [x] Alembic migrations
* [x] CRUD tests for core models
* [x] Basic `/chat` endpoint (echo / stub, no LLM)

---

## **Day 2 — LLM API Integration (Core Chatbot)**

**Goal:** Turn `/chat` into a real LLM-powered chatbot

* [x] Choose LLM provider (OpenAI / Azure / local / others)
* [x] Configure LLM API credentials
* [x] LLM client wrapper (service layer)
* [x] Define base system prompt
* [x] Implement single-turn LLM response
* [x] Handle model parameters (temperature, max tokens)
* [x] Error handling & retry logic
* [x] Add Circuit Breaker (PyBreaker)
* [x] Replace stub `/chat` with real LLM call

---

## **Day 3 — Sessions & Persistent Chat History**

**Goal:** Persist conversations as retrievable documents

* [ ] Session creation API
* [ ] Fetch sessions API
* [ ] Store user & assistant messages in DB
* [ ] Message history API
* [ ] Load full history per session
* [ ] Define “daily memory” or chunking strategy
* [ ] Normalize messages for embedding storage

---

## **Day 4 — Frontend Core**

**Goal:** Usable chat interface

* [ ] Initialize Next.js project
* [ ] Basic layout and routing
* [ ] Chat UI (message list, input box, send button)
* [ ] Role-based message styling
* [ ] Connect frontend to `/chat`
* [ ] Display streaming or full responses
* [ ] Basic error handling

---

## **Day 5 — Vector Store & Embeddings (RAG Storage)**

**Goal:** Store chat history as vectorized memory

* [ ] Deploy Milvus via Docker Compose
* [ ] Create collections and indexes
* [ ] Connect FastAPI to Milvus
* [ ] Choose embedding model
* [ ] Generate embeddings for chat messages
* [ ] Store embeddings with metadata (user, session, date)
* [ ] Test vector insert & similarity search

---

## **Day 6 — RAG Retrieval & Memory Injection**

**Goal:** Retrieval-Augmented Generation

* [ ] Implement top-K vector search
* [ ] Filter by user / session / time
* [ ] Rank and clean retrieved memories
* [ ] Design RAG prompt template
* [ ] Inject retrieved memories into LLM context
* [ ] Inject recent conversation window
* [ ] Token & context length control

---

## **Day 7 — Streaming, UX & Reliability**

**Goal:** Production-ready interaction

* [ ] Enable streaming responses (backend)
* [ ] Implement Server-Sent Events (SSE) for chat responses
* [ ] Stream tokens to frontend
* [ ] Typing indicator
* [ ] Loading & error states
* [ ] Session reset / clear memory
* [ ] Long conversation stress testing
* [ ] Memory relevance evaluation

---

## **Day 8 — Optimization & Deployment**

**Goal:** Stability and scale

* [ ] Tune Milvus index parameters
* [ ] Memory size & retention policies
* [ ] Rate limiting & cost control
* [ ] Dockerize backend cleanly
* [ ] Environment variable hardening
* [ ] Deployment preparation (prod vs dev configs)

---


## **Day 9 — Multi-User Concurrency & Scalability**

**Goal:** Handle many concurrent users efficiently

* [ ] Database connection pooling optimization
  * [ ] Configure SQLAlchemy pool size (min/max connections)
  * [ ] Set appropriate pool timeout and recycle settings
  * [ ] Monitor connection pool usage
* [ ] Async/await optimization
  * [ ] Ensure all I/O operations are async (DB, LLM API calls)
  * [ ] Use async database sessions (asyncpg)
  * [ ] Verify LLM client supports async operations
* [ ] Session isolation & security
  * [ ] Verify session isolation (each user's data is separate)
  * [ ] Add user authentication/authorization
  * [ ] Implement user ID tracking per session
* [ ] Rate limiting per user
  * [ ] Implement rate limiting middleware (slowapi or similar)
  * [ ] Set limits per user/IP (requests per minute)
  * [ ] Return proper 429 responses with retry-after headers
* [ ] LLM API rate limit handling
  * [ ] Implement request queuing for LLM API calls
  * [ ] Add exponential backoff for rate limit errors
  * [ ] Consider request batching if supported
* [ ] Caching strategies
  * [ ] Cache frequently accessed session data
  * [ ] Cache system prompts and templates
  * [ ] Implement Redis for distributed caching (if multi-instance)
* [ ] Connection pooling for external services
  * [ ] Verify LLM client uses HTTP connection pooling
  * [ ] Configure HTTP client timeouts appropriately
  * [ ] Monitor external API connection health
* [ ] Monitoring & observability
  * [ ] Add request metrics (response time, error rate)
  * [ ] Track concurrent user count
  * [ ] Monitor database connection pool usage
  * [ ] Set up alerts for high error rates or latency
* [ ] Load testing
  * [ ] Use locust or k6 for load testing
  * [ ] Test with 100+ concurrent users
  * [ ] Identify bottlenecks (DB, LLM API, memory)
  * [ ] Measure p95/p99 response times
* [ ] Horizontal scaling preparation
  * [ ] Ensure stateless API design (no in-memory state)
  * [ ] Use shared session storage (database, not memory)
  * [ ] Configure load balancer sticky sessions (if needed)
  * [ ] Test multi-instance deployment

---

## Pending List

* [x] Add Fallback - Retry strategy
* [x] Add CircutBreaker (PyBreaker)
* [ ] Add reasons why pick frameworks
* [ ] Add Load Testing
* [ ] Add Stress Testing
* [ ] Learn about FastAPI's lifespan arg
