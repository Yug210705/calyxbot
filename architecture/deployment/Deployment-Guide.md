# Calyx Deployment Guide

This guide covers the deployment of the Backend to Render, the Frontend to Vercel, and the Database to Supabase.

## 1. Database (Supabase)
1. Log into Supabase and create a new project.
2. Under Database Settings, note the **Connection string** (URI).
3. Under API Settings, note the **Project URL**, **anon public key**, and **service_role secret**.
4. Retrieve the **JWT Secret** from the API settings.
5. Run Alembic migrations against the Supabase database:
   ```bash
   DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres" alembic upgrade head
   ```

## 2. Backend (Render)
The backend is defined in `backend/render.yaml`.
1. Connect your GitHub repository to Render using the "Blueprint" deployment method, or manually create a new Web Service.
2. Select the `backend` directory.
3. Configure the following **Production Environment Variables** in Render:
   - `ENVIRONMENT`: `production`
   - `SUPABASE_URL`: (From Step 1)
   - `SUPABASE_SERVICE_ROLE_KEY`: (From Step 1)
   - `SUPABASE_JWT_SECRET`: (From Step 1)
   - `DATABASE_URL`: The Supabase connection string. Use `pool_mode=transaction` and the IPv4 string if required by Render.
   - `ALLOWED_ORIGINS`: The URL of your Vercel frontend (e.g., `https://calyx.vercel.app`)

### Verification (Health Check)
After deployment completes, verify the health check endpoint:
```bash
curl -I https://<your-render-app>.onrender.com/api/v1/health
```
Expect HTTP 200 OK.

## 3. Frontend (Vercel)
The frontend configuration is in `frontend/vercel.json`.
1. Import the repository in Vercel.
2. Set the Root Directory to `frontend`.
3. Configure the following **Production Environment Variables** in Vercel:
   - `NEXT_PUBLIC_SUPABASE_URL`: (From Step 1)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: (From Step 1)
   - `NEXT_PUBLIC_API_URL`: The Render URL from Step 2 (e.g., `https://calyx-api.onrender.com/api/v1`)

### Verification (Build Checklist)
- Verify `npm run build` succeeds without TS errors.
- Visit the deployment URL.
- Test the Signup -> Create Organization -> Invite flow.
