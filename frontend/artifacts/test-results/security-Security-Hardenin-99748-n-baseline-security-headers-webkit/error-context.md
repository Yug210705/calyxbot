# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: security.spec.ts >> Security & Hardening >> Backend responses contain baseline security headers
- Location: tests\e2e\specs\security.spec.ts:36:7

# Error details

```
TypeError: fetch failed
```

# Test source

```ts
  21  |       console.error(`[auth.helper] Failed to fetch users for auto-confirm: ${response.status}`);
  22  |       return;
  23  |     }
  24  | 
  25  |     const data = await response.json();
  26  |     if (!data.users || data.users.length === 0) break;
  27  |     
  28  |     user = data.users.find((u: Record<string, unknown>) => u.email === email);
  29  |     if (user) break;
  30  |     page++;
  31  |   }
  32  | 
  33  |   if (user) {
  34  |     await fetch(`${config.supabaseUrl}/auth/v1/admin/users/${user.id}`, {
  35  |       method: 'PUT',
  36  |       headers: {
  37  |         'Authorization': `Bearer ${config.serviceRoleKey}`,
  38  |         'apikey': config.serviceRoleKey,
  39  |         'Content-Type': 'application/json'
  40  |       },
  41  |       body: JSON.stringify({ email_confirm: true })
  42  |     });
  43  |     console.log(`[auth.helper] Auto-confirmed user ${email}`);
  44  |   }
  45  | }
  46  | 
  47  | export async function cleanupTestUser(email: string) {
  48  |   if (!config.serviceRoleKey) return;
  49  |   
  50  |   let user = null;
  51  |   let page = 1;
  52  |   while (!user) {
  53  |     const response = await fetch(`${config.supabaseUrl}/auth/v1/admin/users?page=${page}&per_page=50`, {
  54  |       method: 'GET',
  55  |       headers: {
  56  |         'Authorization': `Bearer ${config.serviceRoleKey}`,
  57  |         'apikey': config.serviceRoleKey
  58  |       }
  59  |     });
  60  | 
  61  |     if (!response.ok) return;
  62  | 
  63  |     const data = await response.json();
  64  |     if (!data.users || data.users.length === 0) break;
  65  |     
  66  |     user = data.users.find((u: Record<string, unknown>) => u.email === email);
  67  |     if (user) break;
  68  |     page++;
  69  |   }
  70  | 
  71  |   if (user) {
  72  |     await fetch(`${config.supabaseUrl}/auth/v1/admin/users/${user.id}`, {
  73  |       method: 'DELETE',
  74  |       headers: {
  75  |         'Authorization': `Bearer ${config.serviceRoleKey}`,
  76  |         'apikey': config.serviceRoleKey
  77  |       }
  78  |     });
  79  |     console.log(`[auth.helper] Cleaned up user ${email}`);
  80  |   }
  81  | }
  82  | 
  83  | export async function createTestUser(email: string, password: string = 'TestPassword123!') {
  84  |   if (!config.serviceRoleKey) {
  85  |     console.log(`[auth.helper] No SERVICE_ROLE_KEY provided. Skipping admin user creation for ${email}.`);
  86  |     return;
  87  |   }
  88  |   
  89  |   const response = await fetch(`${config.supabaseUrl}/auth/v1/admin/users`, {
  90  |     method: 'POST',
  91  |     headers: {
  92  |       'Authorization': `Bearer ${config.serviceRoleKey}`,
  93  |       'apikey': config.serviceRoleKey,
  94  |       'Content-Type': 'application/json'
  95  |     },
  96  |     body: JSON.stringify({
  97  |       email,
  98  |       password,
  99  |       email_confirm: true,
  100 |       user_metadata: { full_name: 'Admin Created Test User' }
  101 |     })
  102 |   });
  103 | 
  104 |   if (!response.ok) {
  105 |     const errorBody = await response.text();
  106 |     console.error(`[auth.helper] Failed to create user via admin API: ${response.status} ${errorBody}`);
  107 |   } else {
  108 |     console.log(`[auth.helper] Admin created test user ${email}`);
  109 |     
  110 |     // Authenticate to get JWT token
  111 |     const authRes = await fetch(`${config.supabaseUrl}/auth/v1/token?grant_type=password`, {
  112 |       method: 'POST',
  113 |       headers: { 'apikey': config.supabaseAnonKey, 'Content-Type': 'application/json' },
  114 |       body: JSON.stringify({ email, password })
  115 |     });
  116 |     
  117 |     if (authRes.ok) {
  118 |       const { access_token } = await authRes.json();
  119 |       
  120 |       // Call complete-signup to sync the user to the FastAPI backend DB
> 121 |       const syncRes = await fetch(`${config.apiUrl}/api/v1/auth/complete-signup`, {
      |                       ^ TypeError: fetch failed
  122 |         method: 'POST',
  123 |         headers: { 'Authorization': `Bearer ${access_token}`, 'Content-Type': 'application/json' },
  124 |         body: JSON.stringify({ full_name: 'Admin Created Test User' })
  125 |       });
  126 |       
  127 |       if (!syncRes.ok) {
  128 |         console.error(`[auth.helper] Failed to sync user to backend: ${syncRes.status} ${await syncRes.text()}`);
  129 |       } else {
  130 |         console.log(`[auth.helper] Synced test user ${email} to backend`);
  131 |       }
  132 |     } else {
  133 |       console.error(`[auth.helper] Failed to authenticate newly created user for sync`);
  134 |     }
  135 |   }
  136 | }
  137 | 
```