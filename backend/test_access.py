import urllib.request
import urllib.parse
import json
import http.cookiejar

BASE_URL = 'http://localhost:5000/api'

def test_staff_access():
    # Setup cookie jar
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # 1. Login
    print("Testing Login...")
    login_data = json.dumps({
        'username': 'staff1',
        'password': 'staff123'
    }).encode('utf-8')
    
    req = urllib.request.Request(f'{BASE_URL}/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
    
    try:
        with opener.open(req) as response:
            print(f"Login Status: {response.status}")
            print(f"Login Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"Login failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
        return

    # 2. Get Transactions
    print("\nTesting GET /transactions...")
    try:
        with opener.open(f'{BASE_URL}/transactions') as response:
            print(f"GET Transactions Status: {response.status}")
            data = json.loads(response.read().decode('utf-8'))
            print(f"GET Transactions Success: {data.get('success')}")
            print(f"Transaction Count: {len(data.get('data', [])) if data.get('success') else 'N/A'}")
    except urllib.error.HTTPError as e:
        print(f"GET Transactions failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))

    # 3. Create Transaction (Simulation)
    print("\nTesting POST /transactions (Dry Run)...")
    transaction_data = json.dumps({
        'customer_id': 1,
        'total_amount': 10000, 
        'payment_method': 'cash',
        'notes': 'Test transaction from script',
        'details': [] 
    }).encode('utf-8')
    
    req = urllib.request.Request(f'{BASE_URL}/transactions', data=transaction_data, headers={'Content-Type': 'application/json'})
    
    try:
        with opener.open(req) as response:
            print(f"POST Transaction Status: {response.status}")
            print(f"POST Transaction Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"POST Transaction failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))

if __name__ == "__main__":
    try:
        test_staff_access()
    except Exception as e:
        print(f"An error occurred: {e}")
