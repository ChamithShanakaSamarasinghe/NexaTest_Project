# AI Text Data Preprocessing Pipeline

## Overview
This project implements an industry-style AI text preprocessing pipeline that ingests raw text, cleans and tokenizes it, generates word embeddings, computes semantic similarity, applies rule-based semantic mapping, and stores all outputs in PostgreSQL.

The system is fully containerized using Docker and provides a Streamlit-based UI for file upload and result visualization.

## Features
- Text ingestion with encoding detection
- Cleaning and normalization
- Tokenization and frequency analysis
- Word2Vec-based embeddings
- Semantic similarity computation
- Rule-based semantic categorization
- PostgreSQL persistence
- Streamlit UI
- Dockerized environment

## Technology Stack
- Python
- Streamlit
- PostgreSQL
- Docker & Docker Compose
- Gensim, Scikit-learn
- psycopg2

## How to Run (Docker)

```bash
docker compose up --build
Then open: http://localhost:8501

## Notes

Database credentials are for local development only.
pgAdmin configuration is optional and not required to run the pipeline.

## Status
Core backend pipeline and UI are complete. Minor UI enhancements and database administration tooling are future work.