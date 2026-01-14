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

* [ ] Choose LLM provider (OpenAI / Azure / local / others)
* [ ] Configure LLM API credentials
* [ ] LLM client wrapper (service layer)
* [ ] Define base system prompt
* [ ] Implement single-turn LLM response
* [ ] Handle model parameters (temperature, max tokens)
* [ ] Error handling & retry logic
* [ ] Replace stub `/chat` with real LLM call

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


## Pending List

* [ ] Add Fallback - Retry strategy
* [ ] Add CircutBreaker (PyBreaker)
* [ ] Add reasons why pick frameworks
* [ ] Add Load Testing
* [ ] Add Stress Testing
* [ ] Learn about FastAPI's lifespan arg
