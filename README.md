# Memocha

**RAG-based Chatbot with Long-Term Memory**

## Todo List

---

## **Day 1 — Backend & Infrastructure**

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

* [x] Session creation API
* [x] Fetch sessions API
* [x] Store user & assistant messages in DB
* [x] Message history API
* [x] Load full history per session

---

## **Day 4 — Frontend Core**

**Goal:** Usable chat interface

* [x] Initialize Next.js project
* [x] Basic layout and routing
* [x] Chat UI (message list, input box, send button)
* [x] Role-based message styling
* [x] Connect frontend to `/chat`
* [x] Display streaming or full responses
* [x] Basic error handling
* [x] Implement Server-Sent Events (SSE) for chat responses

---

## **Day 5 — LLM & System Performance Evaluation**

**Goal:** Benchmark and evaluate LLM responses and system performance

* [ ] LLM Response Latency Metrics
  * [ ] Measure time to first token (TTFT)
  * [ ] Measure time to completion (TTC)
  * [ ] Track latency distribution (p50, p95, p99)
  * [ ] Compare streaming vs non-streaming latency
* [ ] Streaming Performance Benchmarks
  * [ ] Measure chunks per second
  * [ ] Calculate total streaming time
  * [ ] Evaluate chunk size distribution
  * [ ] Test streaming with different message lengths
* [ ] Response Quality Evaluation
  * [ ] Test response relevance to user queries
  * [ ] Measure response coherence and fluency
  * [ ] Evaluate response accuracy for factual questions
  * [ ] Test response consistency across similar queries
  * [ ] Evaluate response completeness
  * [ ] **Technologies/Methods:** Custom evaluation scripts, LLM-as-a-judge, human evaluation
* [ ] System Performance Benchmarks
  * [ ] Measure end-to-end request latency (p50, p95, p99)
  * [ ] Test concurrent request handling capacity
  * [ ] Evaluate database query performance
  * [ ] Monitor memory usage during streaming
  * [ ] Track CPU utilization under load
  * [ ] Measure database connection pool efficiency
  * [ ] **Technologies/Methods:** pytest-benchmark, APM tools (Datadog, New Relic), custom profiling
* [ ] Streaming UX Evaluation
  * [ ] Measure time to first token (TTFT) - user perception of responsiveness
  * [ ] Evaluate chunk size impact on perceived performance
  * [ ] Test streaming behavior with slow network conditions
  * [ ] Measure user satisfaction with streaming vs non-streaming
  * [ ] A/B test different streaming configurations
* [ ] Error Rate and Reliability Metrics
  * [ ] Track LLM API error rates
  * [ ] Measure circuit breaker activation frequency
  * [ ] Evaluate retry success rates
  * [ ] Monitor connection timeout occurrences
  * [ ] Track error recovery time
  * [ ] Measure system uptime and availability
* [ ] Cost and Efficiency Analysis
  * [ ] Track token usage per conversation
  * [ ] Calculate cost per message/response
  * [ ] Measure tokens per second throughput
  * [ ] Evaluate cost-effectiveness of streaming vs batch
  * [ ] Track API cost trends over time
  * [ ] **Technologies/Methods:** Token counting libraries, cost tracking scripts, usage analytics
* [ ] Load Testing
  * [ ] Test system under various load conditions
  * [ ] Measure performance degradation with increased load
  * [ ] Identify system bottlenecks
  * [ ] Test rate limiting effectiveness
  * [ ] **Technologies/Methods:** Locust, k6, custom load testing scripts

---

## **Day 6 — Vector Store & Embeddings (RAG Storage)**

**Goal:** Store chat history as vectorized memory

* [ ] Deploy Milvus via Docker Compose
* [ ] Create collections and indexes
* [ ] Connect FastAPI to Milvus
* [ ] Choose embedding model
* [ ] Generate embeddings for chat messages
* [ ] Store embeddings with metadata (user, session, date)
* [ ] Test vector insert & similarity search
* [ ] Vector Search Performance Evaluation
  * [ ] Measure retrieval latency
  * [ ] Benchmark embedding generation speed
  * [ ] Test vector search query time with different index types
  * [ ] **Technologies/Methods:** Custom timing scripts, pytest-benchmark, vector similarity benchmarks

---

## **Day 7 — RAG Retrieval & Memory Injection**

**Goal:** Retrieval-Augmented Generation

* [ ] Implement top-K vector search
* [ ] Filter by user / session / time
* [ ] Rank and clean retrieved memories
* [ ] Design RAG prompt template
* [ ] Inject retrieved memories into LLM context
* [ ] Inject recent conversation window
* [ ] Token & context length control
* [ ] Define "daily memory" or chunking strategy
* [ ] Normalize messages for embedding storage
* [ ] RAG Retrieval Evaluation
  * [ ] Measure retrieval accuracy (precision, recall)
  * [ ] Evaluate Mean Reciprocal Rank (MRR)
  * [ ] Calculate Normalized Discounted Cumulative Gain (NDCG)
  * [ ] Test retrieval relevance with ground truth
  * [ ] **Technologies/Methods:** Custom evaluation scripts, scikit-learn metrics, vector similarity benchmarks, retrieval hit rate
* [ ] End-to-End RAG System Evaluation
  * [ ] Evaluate answer faithfulness (grounded in retrieved context)
  * [ ] Measure answer relevance to user query
  * [ ] Test context precision and recall
  * [ ] Evaluate answer semantic similarity
  * [ ] **Technologies/Methods:** RAGAS framework, custom evaluation pipeline, semantic similarity metrics
* [ ] Memory Retrieval Quality
  * [ ] Test memory recall accuracy across sessions
  * [ ] Evaluate temporal relevance (recent vs old memories)
  * [ ] Measure memory injection effectiveness
  * [ ] Test memory chunking and retrieval strategies
  * [ ] **Technologies/Methods:** Custom evaluation suite, A/B testing different retrieval strategies, relevance scoring

---

## **Day 8 — Streaming, UX & Reliability**

**Goal:** Production-ready interaction

* [ ] Typing indicator
* [ ] Loading & error states
* [ ] Session reset / clear memory
* [ ] Long conversation stress testing
* [ ] Memory relevance evaluation
* [ ] Stress Testing & Edge Cases
  * [ ] Test with very long conversations (1000+ messages)
  * [ ] Evaluate performance with large memory stores
  * [ ] Test retrieval with sparse/no relevant memories
  * [ ] Measure degradation with context window limits
  * [ ] **Technologies/Methods:** Locust, k6, custom stress test scripts, memory profiling

---

## **Day 9 — Optimization & Deployment**

**Goal:** Stability and scale

* [ ] Tune Milvus index parameters
* [ ] Memory size & retention policies
* [ ] Rate limiting & cost control
* [ ] Dockerize backend cleanly
* [ ] Environment variable hardening
* [ ] Deployment preparation (prod vs dev configs)
* [ ] Performance Benchmarking
  * [ ] Measure LLM API latency (p50, p95, p99)
  * [ ] Track end-to-end response time
  * [ ] Monitor token usage and cost per request
  * [ ] **Technologies/Methods:** pytest-benchmark, custom timing scripts, APM tools (Datadog, New Relic)
* [ ] Cost Analysis
  * [ ] Track LLM API costs per conversation
  * [ ] Measure embedding generation costs
  * [ ] Calculate storage costs (vector DB)
  * [ ] Optimize cost vs quality trade-offs
  * [ ] **Technologies/Methods:** Cost tracking scripts, usage analytics, cost optimization strategies

---


## **Day 10 — Multi-User Concurrency & Scalability**

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
* [ ] Continuous Evaluation Setup
  * [ ] Set up automated evaluation pipeline
  * [ ] Create evaluation dashboard
  * [ ] Implement regression testing for quality metrics
  * [ ] Track metrics over time
  * [ ] **Technologies/Methods:** CI/CD integration, evaluation databases, monitoring dashboards (Grafana, custom)

---

## Pending List

* [x] Add Fallback - Retry strategy
* [x] Add CircutBreaker (PyBreaker)
* [ ] Add reasons why pick frameworks
* [ ] Add Load Testing
* [ ] Add Stress Testing
* [ ] Learn about FastAPI's lifespan arg
* [ ] Allow other API, or self-hosted LLM models
* [ ] Find an LLM Serving Engine
* [ ] Add non-root user for security in frontend Dockerfile (production)
