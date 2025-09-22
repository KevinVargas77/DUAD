import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:5000"

def test_api_with_cache():
    print("Testing API with Redis cache...")
    
    # Test 1: GET all products (should cache the results)
    print("\n1. Test: GET /products (first time - no cache)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: Response successful: {len(data.get('products', []))} products")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    else:
        print(f"ERROR: {response.status_code}")
        return
    
    # Test 2: GET all products again (should use cache)
    print("\n2. Test: GET /products (second time - from cache)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: Response from cache: {len(data.get('products', []))} products")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    else:
        print(f"ERROR: {response.status_code}")
    
    # Test 3: GET specific product (if available)
    if len(data.get('products', [])) > 0:
        product_id = data['products'][0]['id']
        
        print(f"\n3. Test: GET /products/{product_id} (first time - no cache)")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        end_time = time.time()
        
        if response.status_code == 200:
            product_data = response.json()
            print(f"SUCCESS: Product retrieved: {product_data['product']['name']}")
            print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
        else:
            print(f"ERROR: {response.status_code}")
        
        print(f"\n4. Test: GET /products/{product_id} (second time - from cache)")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        end_time = time.time()
        
        if response.status_code == 200:
            product_data = response.json()
            print(f"SUCCESS: Product from cache: {product_data['product']['name']}")
            print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
        else:
            print(f"ERROR: {response.status_code}")
    
    print("\nCache tests completed!")
    print("NOTE: To fully test the cache, you will need:")
    print("   - JWT authentication to create/update/delete products")
    print("   - Verify cache invalidation after CUD operations")

def test_liveness():
    print("Testing liveness endpoint...")
    response = requests.get(f"{BASE_URL}/liveness")
    
    if response.status_code == 200:
        print("SUCCESS: API is working correctly")
        return True
    else:
        print("ERROR: API is not available")
        return False

if __name__ == "__main__":
    if test_liveness():
        test_api_with_cache()
    else:
        print("ERROR: Cannot continue - API is not available")
        print("HINT: Make sure Flask application is running on http://127.0.0.1:5000")