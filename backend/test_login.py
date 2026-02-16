import urllib.request
import json

def test_login():
    url = 'http://localhost:5000/api/auth/login'
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    print(f"Testing login at {url}...")
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'Origin': 'http://localhost:5174'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            json_response = json.loads(response_body)
            
            print(f"Status Code: {status_code}")
            print(f"Response: {json_response}")
            
            if status_code == 200 and json_response.get('success'):
                print("✅ LOGIN SUCCESS!")
            else:
                print("❌ LOGIN FAILED!")
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
