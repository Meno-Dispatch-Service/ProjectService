import time
import httpx

URL = "http://localhost:8082/project-service/api/v1/get-project/5/"

start = time.time()
response = httpx.get(URL)
end = time.time()

print("Response time:", end - start, "seconds")
print("Status code:", response.status_code)
print("Response JSON:", response.json())
