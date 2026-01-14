# Memocha
Chatbot with Memory

## Todo List

### **Day 1 — Project & Backend Setup**

* [x] Repo setup, folders, Git
* [x] FastAPI project initialization
* [x] Health check endpoint
* [x] Environment configuration
* [x] Logging setup
* [x] PostgreSQL via Docker
* [ ] SQLAlchemy models
* [ ] Migrations
* [ ] CRUD test
* [ ] Basic `/chat` endpoint (no memory)

---

### **Day 2 — Frontend Core**

* [ ] Initialize Next.js project
* [ ] Basic layout and routing
* [ ] Chat UI (message list, input box, send button)
* [ ] Role-based message styling
* [ ] Connect frontend to `/chat` endpoint
* [ ] Display responses
* [ ] Basic error handling

---

### **Day 3 — Sessions & History**

* [ ] Session model (backend)
* [ ] Create session API
* [ ] Fetch sessions API
* [ ] Message history API
* [ ] Load messages per session
* [ ] Session sidebar UI
* [ ] Switch between chat sessions

---

### **Day 4 — Milvus & Embeddings**

* [ ] Deploy Milvus with Docker Compose
* [ ] Create collection and index
* [ ] Connect FastAPI to Milvus
* [ ] Test vector insert
* [ ] Test vector search
* [ ] Choose embedding model
* [ ] Generate embeddings for messages
* [ ] Store embeddings with metadata

---

### **Day 5 — Memory Retrieval & Agent Logic**

* [ ] Implement top-K vector search
* [ ] Filter by user/session
* [ ] Clean and rank retrieved memories
* [ ] Define system prompt
* [ ] Inject retrieved memories
* [ ] Inject recent chat history
* [ ] Token and context size control

---

### **Day 6 — Streaming & UX**

* [ ] Enable streaming responses in backend
* [ ] Stream tokens to frontend
* [ ] Live token rendering in UI
* [ ] Typing indicator
* [ ] Loading states
* [ ] Clear conversation / session reset

---

### **Day 7 — Testing, Tuning & Deployment**

* [ ] Long conversation testing
* [ ] Memory relevance testing
* [ ] Concurrent usage testing
* [ ] Tune Milvus index parameters
* [ ] Limit memory size
* [ ] Dockerize backend
* [ ] Environment variable setup
* [ ] Deployment preparation

## Pending List

* [ ] Add Fallback - Retry strategy
* [ ] Add CircutBreaker (PyBreaker)
* [ ] Add reasons why pick frameworks
* [ ] Add Load Testing
* [ ] Add Stress Testing
* [ ] Learn about FastAPI's lifespan arg
