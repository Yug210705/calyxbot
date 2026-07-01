# Environment Variable Matrix

| Variable | Development | Staging (Render/Vercel Preview) | Production (Render/Vercel Main) |
|---|---|---|---|
| **Backend** | | | |
| `ENVIRONMENT` | `development` | `staging` | `production` |
| `DATABASE_URL` | `postgresql://...` (Local/Dev DB) | `postgresql://...` (Staging DB) | `postgresql://...` (Prod DB, IPv4/Transaction pool) |
| `SUPABASE_URL` | `http://localhost:54321` | Supabase Staging URL | Supabase Prod URL |
| `SUPABASE_SERVICE_ROLE_KEY`| Local mock key | Staging key | Prod key |
| `SUPABASE_JWT_SECRET` | Local mock secret | Staging secret | Prod secret |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | `https://staging-calyx.vercel.app` | `https://calyx.vercel.app` |
| | | | |
| **Frontend** | | | |
| `NEXT_PUBLIC_SUPABASE_URL` | `http://localhost:54321` | Supabase Staging URL | Supabase Prod URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Local mock anon key | Staging anon key | Prod anon key |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api/v1` | `https://staging-api.onrender.com/api/v1` | `https://calyx-api.onrender.com/api/v1` |
