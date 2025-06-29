import requests

# Primeiro fazer login para obter um token válido
login_url = "http://localhost:8000/login"
login_data = {
    "nickname": "johnatas1",
    "password": "123456"
}

try:
    response = requests.post(login_url, json=login_data)
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.text}")
    
    if response.status_code == 200:
        login_result = response.json()
        token = login_result.get("access_token")
        
        if token:
            # Testar leaderboard com token válido
            leaderboard_url = "http://localhost:8000/api/usuarios/leaderboard"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            leaderboard_response = requests.get(leaderboard_url, headers=headers)
            print(f"\nLeaderboard Status: {leaderboard_response.status_code}")
            print(f"Leaderboard Response: {leaderboard_response.text}")
        else:
            print("Nenhum token retornado no login")
    
except Exception as e:
    print(f"Erro: {e}")
