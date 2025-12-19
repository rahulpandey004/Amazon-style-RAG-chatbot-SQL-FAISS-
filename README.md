🛒 Amazon-Style RAG Chatbot (No Framework)

An Amazon-like intelligent chatbot built from scratch in Python using SQL + FAISS-based RAG, without LangChain or any orchestration framework.
The system supports order tracking, product specification search, and order → product → knowledge chaining.

🚀 Key Features

🔍 Product Specification Search (RAG)

Ask laptop specs, features, battery life, RAM, processor, etc.

Uses FAISS vector search over cleaned product PDFs.

📦 Order Status Lookup (SQL)

Track orders using Order ID.

Fetches order details from a relational database.

🔗 Order → Product → Specs Chaining

Example:
“Give all specifications for the laptop having order id ORD009”

Flow: SQL → Product Name → Vector DB → Answer

🧠 LLM-based Intent Detection

Classifies queries into:

ORDER_STATUS

PRODUCT_SEARCH

GENERAL_RAG

🧭 Custom Routing Logic

Intelligent query routing without frameworks.

Safe fallbacks to prevent crashes.

⚙️ Framework-Free Architecture

No LangChain / LlamaIndex.




# Architecture

User Query
    ↓
Intent Detection (LLM)
    ↓
Router
 ┌───────────────┬───────────────────┐
 │               │                   │
SQL DB        Vector DB (FAISS)    General RAG
 │               │
Order Info     Product Specs
 │               │
 └──────→ Combined Response ←───────┘



amazon_Chatbot/
│
├── backend/
│   ├── intent.py        # Intent classification
│   ├── router.py        # Query routing & orchestration
│   ├── rag.py           # FAISS-based RAG search
│   ├── sql.py           # Order database logic
│   ├── main.py          # Entry point
│
├── data/
│   └── laptops.pdf      # Product specifications (cleaned)
│
├── requirements.txt
├── README.md
└── .gitignore




🧠 Intent Types
Intent	Description
ORDER_STATUS	Order tracking, delivery status
PRODUCT_SEARCH	Laptop specs, comparisons
GENERAL_RAG	General informational queries
🛠️ Tech Stack

Python

FAISS – Vector search

Sentence Transformers – Embeddings

Ollama (Mistral / LLMs) – Intent detection & response

SQL (SQLite / MySQL) – Order database

PDF Processing – Cleaned ingestion pipeline









