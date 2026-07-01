import urllib.request

req = urllib.request.Request("https://pchoelsfgzorcbidhbtk.supabase.co/auth/v1/.well-known/jwks.json")
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(e)
