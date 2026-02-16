import urllib.request
import json
import http.cookiejar

def test_dashboard():
    # Setup cookie jar to handle session
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # Login first
    login_url = 'http://localhost:5000/api/auth/login'
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    print("1. Logging in...")
    try:
        req = urllib.request.Request(
            login_url, 
            data=json.dumps(login_data).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'Origin': 'http://localhost:5174'},
            method='POST'
        )
        with opener.open(req) as response:
            print(f"Login Status: {response.getcode()}")
            print(response.read().decode())
    except Exception as e:
        print(f"Login Failed: {e}")
        return

    # Check Dashboard Stats
    endpoints = [
        '/api/dashboard/stats',
        '/api/dashboard/sales-chart',
        '/api/dashboard/category-chart',
        '/api/dashboard/top-products',
        '/api/dashboard/recent-transactions'
    ]

    print("\n2. Checking Dashboard Endpoints...")
    for endpoint in endpoints:
        url = f'http://localhost:5000{endpoint}'
        print(f"\nTesting {endpoint}...")
        try:
            req = urllib.request.Request(
                url,
                headers={'Content-Type': 'application/json', 'Origin': 'http://localhost:5174'},
                method='GET'
            )
            with opener.open(req) as response:
                print(f"Status: {response.getcode()}")
                data = json.loads(response.read().decode())
                # Print summary only
                if 'data' in data:
                    print(f"Success. Data items: {len(data['data']) if isinstance(data['data'], list) else 'Dict'}")
                else:
                    print("Success but unexpected structure.")
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
            print(e.read().decode())
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_dashboard()
