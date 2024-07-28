import time
import requests
from datetime import datetime
import json
import random

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '0',
    "referer": "https://mini.playvaliants.com/",
}

def load_credentials():
    try:
        with open('token.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        # print("Token berhasil dimuat.")
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat query:", str(e))
        return 

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'


def login(query):
    url = f'https://mini.playvaliants.com/api/login?{query}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code >= 500:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 400:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def getdata(token):
    url = 'https://mini.playvaliants.com/api/user/data'
    headers['authorization'] = f'Bearer {token}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code >= 500:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 400:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def get_mission(token):
    url = 'https://mini.playvaliants.com/api/user/missions'
    headers['authorization'] = f'Bearer {token}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code >= 500:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 400:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def claim_mission(token, payload):
    url = 'https://mini.playvaliants.com/api/missions/claim'
    headers['authorization'] = f'Bearer {token}'
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 500:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 400:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def taptap(token, payload):
    url = 'https://mini.playvaliants.com/api/gameplay/click'
    headers['authorization'] = f'Bearer {token}'
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 500:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 400:
            print(f"Status Code : {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def main():
    queries = load_credentials()
    mission = 'n'
    auto_battle = 'n'
    auto_combo = 'n'
    for index, token in enumerate(queries):
        useragent = getuseragent(index)
        headers['user-agent'] = useragent
        data_login = getdata(token)
        if data_login is not None:
            print(data_login)
            print(f'======== User {index+1} =========')
            energy = data_login.get('energy')
            print(f"Energy : {data_login.get('energy')}/{data_login.get('energy_cap')}")
            if mission == 'y':
                data_mission = get_mission(token)
                if data_mission is not None:
                    list_mission = data_mission.get('missions')
                    for miss in list_mission:
                        claimed = miss.get('claimed')
                        id = miss.get('id')
                        if claimed == False:
                            time.sleep(2)
                            payload = {"id":id}
                            data_claim = claim_mission(token, payload)
                            if data_claim is not None:
                                reward = data_claim.get('reward')
                                print(f"Mission {id} claimed successfully | Reward : {reward}")

            while True:
                time.sleep(2)
                tap = random.randint(50, 60)

                if energy < tap:
                    tap = energy

                payload = {"count":tap}
                data_tap = taptap(token, payload)
                if data_tap is not None:
                    user_energy = data_tap.get('user_energy')
                    reward = data_tap.get('reward')
                    print(f" Tapping {reward} Energy : {user_energy}")
                    energy = user_energy
                
                if energy < 50:
                    break
        #print(data_login)

if __name__ == "__main__":
    main()