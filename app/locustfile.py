import random

from locust import HttpUser, between, task


class EcommerceUser(HttpUser):
    wait_time = between(1, 3)
    token = None 
    
    def on_start(self):
        email = f"loadtest_{random.randint(1, 1000000)}@example.com"
        password = "password123"
        username = f"user_{random.randint(1, 1000000)}"

        with self.client.post("api/v1/users/register", json={
            "username": username,
            "email": email,
            "password": password,
        }, catch_response=True) as response:
            
            if response.status_code != 200:
                print(f"Register failed: {response.text}")
                response.failure("Register failed")
                return 

            user_data = response.json()
            verification_token = user_data.get("verification_token")
            
            if not verification_token:
                print("Error: No verification_token returned. Check Backend Schema!")
                return

        verify_url = f"api/v1/users/verify?token={verification_token}"
        with self.client.get(verify_url, catch_response=True) as v_res:
            if v_res.status_code != 200:
                print(f"Verify failed: {v_res.text}")
                v_res.failure("Verify failed")
                return

        login_res = self.client.post("/users/login", json={
            "identifier": email, 
            "password": password
        })
        
        if login_res.status_code == 200:
            self.token = login_res.json().get("access_token")
        else:
            print(f"Login failed for {email}: {login_res.text}")

    
    @task(3)
    def view_products(self):
        self.client.get("/api/v1/products", headers=self._get_headers())

    @task(1) 
    def create_order(self):
        if not self.token:
            return

        payload = {
            "items": [
                {"product_id": "75983652-8c70-41d9-b1c5-939c4d4c83c9", "quantity": 1} 
            ],
            "shipping_address": "Hanoi, Vietnam"
        }
    
        with self.client.post("/api/v1/orders/", json=payload, headers=self._get_headers(), catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            elif response.status_code == 400 and "Insufficient stock" in response.text:
                response.success() 
            else:
                response.failure(f"Got status {response.status_code}: {response.text}")

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}