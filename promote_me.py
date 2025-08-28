import requests
import os

SUPABASE_URL = "https://blqtfxldzdxzsfmtafzi.supabase.co"
SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

user_id = "8341df1c-f9ea-4ef1-ae22-94c25351b57e"

response = requests.patch(
    f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "app_metadata": {"roles": ["admin"]}
    }
)

print(response.json())
