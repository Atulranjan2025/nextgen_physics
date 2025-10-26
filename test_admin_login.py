import requests

# Your live site admin login URL
LOGIN_URL = "https://www.nextgenphysics.in/admin/login/"

# Credentials
data = {
    "username": "admin",
    "password": "NextGen@123",
    "next": "/admin/"
}

# Start a session (so cookies can persist)
session = requests.Session()

# Send POST request to login
response = session.post(LOGIN_URL, data=data, allow_redirects=False)

print("🔍 Status Code:", response.status_code)
print("🔍 Headers:", response.headers)

# Check cookies
cookies = session.cookies.get_dict()
print("🍪 Cookies stored:", cookies)

# Step 2: Try accessing the admin dashboard
dashboard = session.get("https://www.nextgenphysics.in/admin/")
print("📄 Admin Dashboard Status:", dashboard.status_code)
print("📄 Dashboard Title (first 200 chars):")
print(dashboard.text[:200])
