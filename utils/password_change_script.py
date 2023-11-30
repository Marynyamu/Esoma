import requests
import json

def change_password(username, old_password, new_password):
    # Replace these with your actual credentials and endpoint URL
    api_url = 'http://your_api_url/api/password_change'
    login_url = 'http://your_login_url'  # Replace with your login URL

    # Step 1: Login to get the JWT token
    login_data = {
        'username': username,
        'password': old_password
    }

    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        token = response.json().get('access_token')  # Assuming the token is returned in a field named 'access_token'

        # Step 2: Change password request with JWT token
        change_password_data = {
            'username': username,
            'old_password': old_password,
            'new_password': new_password
        }

        headers = {
            'Authorization': f'Bearer {token}',  # Include the JWT token in the Authorization header
            'Content-Type': 'application/json'
        }

        change_response = requests.post(api_url, json=change_password_data, headers=headers)
        return change_response.json()  # Return the response from the password change endpoint
    else:
        return {"message": "Login failed. Couldn't retrieve JWT token."}

