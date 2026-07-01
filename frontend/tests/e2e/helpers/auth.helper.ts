import { config } from '../config';

export async function autoConfirmUser(email: string) {
  if (!config.serviceRoleKey) {
    console.log(`[auth.helper] No SERVICE_ROLE_KEY provided. Skipping auto-confirm for ${email}.`);
    return;
  }
  
  let user = null;
  let page = 1;
  while (!user) {
    const response = await fetch(`${config.supabaseUrl}/auth/v1/admin/users?page=${page}&per_page=50`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${config.serviceRoleKey}`,
        'apikey': config.serviceRoleKey
      }
    });

    if (!response.ok) {
      console.error(`[auth.helper] Failed to fetch users for auto-confirm: ${response.status}`);
      return;
    }

    const data = await response.json();
    if (!data.users || data.users.length === 0) break;
    
    user = data.users.find((u: Record<string, unknown>) => u.email === email);
    if (user) break;
    page++;
  }

  if (user) {
    await fetch(`${config.supabaseUrl}/auth/v1/admin/users/${user.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${config.serviceRoleKey}`,
        'apikey': config.serviceRoleKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email_confirm: true })
    });
    console.log(`[auth.helper] Auto-confirmed user ${email}`);
  }
}

export async function cleanupTestUser(email: string) {
  if (!config.serviceRoleKey) return;
  
  let user = null;
  let page = 1;
  while (!user) {
    const response = await fetch(`${config.supabaseUrl}/auth/v1/admin/users?page=${page}&per_page=50`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${config.serviceRoleKey}`,
        'apikey': config.serviceRoleKey
      }
    });

    if (!response.ok) return;

    const data = await response.json();
    if (!data.users || data.users.length === 0) break;
    
    user = data.users.find((u: Record<string, unknown>) => u.email === email);
    if (user) break;
    page++;
  }

  if (user) {
    await fetch(`${config.supabaseUrl}/auth/v1/admin/users/${user.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${config.serviceRoleKey}`,
        'apikey': config.serviceRoleKey
      }
    });
    console.log(`[auth.helper] Cleaned up user ${email}`);
  }
}

export async function createTestUser(email: string, password: string = 'TestPassword123!') {
  if (!config.serviceRoleKey) {
    console.log(`[auth.helper] No SERVICE_ROLE_KEY provided. Skipping admin user creation for ${email}.`);
    return;
  }
  
  const response = await fetch(`${config.supabaseUrl}/auth/v1/admin/users`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${config.serviceRoleKey}`,
      'apikey': config.serviceRoleKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email,
      password,
      email_confirm: true,
      user_metadata: { full_name: 'Admin Created Test User' }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    console.error(`[auth.helper] Failed to create user via admin API: ${response.status} ${errorBody}`);
  } else {
    console.log(`[auth.helper] Admin created test user ${email}`);
    
    // Authenticate to get JWT token
    const authRes = await fetch(`${config.supabaseUrl}/auth/v1/token?grant_type=password`, {
      method: 'POST',
      headers: { 'apikey': config.supabaseAnonKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (authRes.ok) {
      const { access_token } = await authRes.json();
      
      // Call complete-signup to sync the user to the FastAPI backend DB
      const syncRes = await fetch(`${config.apiUrl}/api/v1/auth/complete-signup`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${access_token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: 'Admin Created Test User' })
      });
      
      if (!syncRes.ok) {
        console.error(`[auth.helper] Failed to sync user to backend: ${syncRes.status} ${await syncRes.text()}`);
      } else {
        console.log(`[auth.helper] Synced test user ${email} to backend`);
      }
    } else {
      console.error(`[auth.helper] Failed to authenticate newly created user for sync`);
    }
  }
}
