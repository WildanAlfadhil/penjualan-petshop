import urllib.request
import json
import http.cookiejar

BASE_URL = 'http://localhost:5000/api'

def cleanup():
    # Setup cookie jar
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # Login again
    login_data = json.dumps({
        'username': 'staff1',
        'password': 'staff123'
    }).encode('utf-8')
    
    req = urllib.request.Request(f'{BASE_URL}/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
    opener.open(req)
    
    # Delete transaction 11
    print("Deleting test transaction 11...")
    req = urllib.request.Request(f'{BASE_URL}/transactions/11', method='DELETE')
    try:
        with opener.open(req) as response:
            print(f"Delete Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"Delete failed: {e.code} {e.reason}")

if __name__ == "__main__":
    cleanup()
