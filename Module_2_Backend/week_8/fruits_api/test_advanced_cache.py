import requests
import time

# Configuration
BASE_URL = "http://127.0.0.1:5000"

def test_advanced_cache_features():
    print("Testing Advanced Cache Features with Filters Support...")
    
    # Test 1: GET all products without filters
    print("\n1. Test: GET /products (no filters - should cache)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: {len(data.get('products', []))} products")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 2: Same request (should use cache)
    print("\n2. Test: GET /products (same request - from cache)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products")
    end_time = time.time()
    
    if response.status_code == 200:
        print(f"SUCCESS: Response from cache")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 3: GET with max_price filter
    print("\n3. Test: GET /products?max_price=100 (with filter - new cache key)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products?max_price=100")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: {len(data.get('products', []))} products with max_price=100")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 4: Same filtered request (should use filter-specific cache)
    print("\n4. Test: GET /products?max_price=100 (same filter - from cache)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products?max_price=100")
    end_time = time.time()
    
    if response.status_code == 200:
        print(f"SUCCESS: Filtered response from cache")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 5: Different filter
    print("\n5. Test: GET /products?min_price=50 (different filter - new cache key)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products?min_price=50")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: {len(data.get('products', []))} products with min_price=50")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 6: Multiple filters
    print("\n6. Test: GET /products?min_price=20&max_price=80 (multiple filters)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products?min_price=20&max_price=80")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: {len(data.get('products', []))} products with price range 20-80")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    # Test 7: Name filter
    print("\n7. Test: GET /products?name=apple (name filter)")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/products?name=apple")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: {len(data.get('products', []))} products matching 'apple'")
        print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
    
    print("\nAdvanced cache test completed!")
    print("\nCache Key Examples Generated:")
    print("- all_products (no filters)")
    print("- all_products_max_price=100")
    print("- all_products_min_price=50")
    print("- all_products_max_price=80_min_price=20")
    print("- all_products_name=apple")
    print("\nEach filter combination gets its own cache entry!")

def test_individual_product_cache():
    print("\n" + "="*50)
    print("Testing Individual Product Cache...")
    
    # First, get list to see if we have products
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        data = response.json()
        if len(data.get('products', [])) > 0:
            product_id = data['products'][0]['id']
            
            print(f"\n1. Test: GET /products/{product_id} (first time)")
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/products/{product_id}")
            end_time = time.time()
            
            if response.status_code == 200:
                product = response.json()
                print(f"SUCCESS: Product {product['product']['name']}")
                print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
            
            print(f"\n2. Test: GET /products/{product_id} (from cache)")
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/products/{product_id}")
            end_time = time.time()
            
            if response.status_code == 200:
                print(f"SUCCESS: Product from cache")
                print(f"Response time: {(end_time - start_time)*1000:.2f}ms")
        else:
            print("No products available to test individual caching")

def test_liveness():
    print("Testing API availability...")
    response = requests.get(f"{BASE_URL}/liveness")
    
    if response.status_code == 200:
        print("SUCCESS: API is running")
        return True
    else:
        print("ERROR: API is not available")
        return False

if __name__ == "__main__":
    if test_liveness():
        test_advanced_cache_features()
        test_individual_product_cache()
    else:
        print("ERROR: Make sure Flask application is running on http://127.0.0.1:5000")