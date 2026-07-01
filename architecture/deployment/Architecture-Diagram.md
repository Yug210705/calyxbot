# Calyx Production Architecture

```mermaid
graph TD
    Client[Web Browser / Client]
    
    subgraph Vercel [Frontend (Vercel)]
        NextJS[Next.js App]
    end
    
    subgraph Render [Backend (Render)]
        FastAPI[FastAPI Modular Monolith]
    end
    
    subgraph Supabase [Database & Auth (Supabase)]
        Postgres[(PostgreSQL)]
        GoTrue[Supabase Auth / GoTrue]
    end
    
    Client -->|HTTPS / UI| NextJS
    Client -->|JWT Authentication| GoTrue
    NextJS -->|REST API + Bearer JWT| FastAPI
    FastAPI -->|JWT Verification| GoTrue
    FastAPI -->|SQLAlchemy Async| Postgres
```
