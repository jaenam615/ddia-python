# ddia-python

This repository contains Python-based implementations of key concepts from the book **"Designing Data-Intensive Applications" (DDIA)** by Martin Kleppmann.

The goal of this project is to solidify understanding of distributed systems, databases, and scalable architecture by translating theoretical ideas into runnable, testable code.

---

## 📁 Project Structure
ddia-python/
├── src/                 # Source code organized by chapter
│   ├── chapter_1/
│   └── chapter_2/
│
├── tests/               # Corresponding unit tests per chapter
│   ├── chapter_1/
│   └── chapter_2/
│
├── pyproject.toml       # Dependency and project configuration
├── uv.lock              # Lock file 
└── docker-compose.yml   # Optional container setup for services 

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ddia-python.git
cd ddia-python
```

### 2. Set up environment

Make sure you have Python 3.12+ installed.

Use uv to install dependencies:

```bash
uv venv
uv pip install -r pyproject.toml
(Optional) docker-compose up -d
```