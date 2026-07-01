import jwt

url = "https://pchoelsfgzorcbidhbtk.supabase.co/auth/v1/.well-known/jwks.json"
jwks_client = jwt.PyJWKClient(url)

token = "eyJhbGciOiJFUzI1NiIsImtpZCI6Ijc3MTdjOWE1LWVhMmEtNGYxOC1iYWM2LTE0ZDhkYWJiMWY3MyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3BjaG9lbHNmZ3pvcmNiaWRoYnRrLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJlN2Q5ZjZlNS1kMmZiLTRiM2ItYjcyZi03OTVhZWU4OTI3MjgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzgyOTAzMjA0LCJpYXQiOjE3ODI4OTk2MDQsImVtYWlsIjoiYXBpLTE3ODI4OTk2MDA3OTVAZXhhbXBsZS5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJBZG1pbiBDcmVhdGVkIFRlc3QgVXNlciJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzgyODk5NjA0fV0sInNlc3Npb25faWQiOiI1ZTMyMWY0Yi1jYTgyLTQ0MTEtYWNlZC04YzU3MGMzOTY0NTgiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.KYCPj9805ZhvH7DE3zAU6JX207tVX7VeYK8md1FHaHIeKE3AvGx5-q0-178EbRBrxXuc3ifkW1oyNq_IH-aiCQ"

try:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256", "RS256", "HS256"],
        audience="authenticated"
    )
    print("Success")
except Exception as e:
    print(type(e).__name__, str(e))
