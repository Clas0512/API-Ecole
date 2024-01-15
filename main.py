#!/usr/bin/env python3

from IPython.display import display, Image

import time
import requests
import json

UID = "Your-UID"
SECRET = "Your-secret"

def post42(url, payload):
    url = "https://api.intra.42.fr" + url
    payload = payload
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get42(url, payload):
    url = "https://api.intra.42.fr" + url
    payload = payload
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

wtoken = post42("/oauth/token", {"grant_type": "client_credentials", \
                                "client_id": UID, "client_secret": SECRET})
campus_users = []
temp = []

campus_users_general = '/v2/campus/49'
campus_users_total = get42(campus_users_general, {"access_token": wtoken["access_token"]})
total_users = campus_users_total["users_count"]

total_pages = ( total_users // 100 + 1 ) + 1

print(f"Total users: {total_users} Total pages: {total_pages}")
print("Please wait while data from API is retrieved...")

for i in range(1, total_pages):
    campus_users += get42("/v2/campus/49/users?page[number]=" + str(i) + "&page[size]=100", \
                                                   {"access_token": wtoken["access_token"]})

for user in campus_users:
    temp.append({
        "full_name": user.get("usual_full_name"),
        "login": user.get("login"),  
        "correction_point": user.get("correction_point"),
        "pool_month": user.get("pool_month"),
        "pool_year": user.get("pool_year"),
        "location": user.get("location"),  
        "updated_at": user.get("updated_at").split("T")[1].split(".")[0],
        "wallet": user.get("wallet"),
        "image": user.get("image")
    })

while (1):
    search = input("Search Name: ")
    for entry in temp:
        if (search.lower() in entry['login'].lower() or
                search.lower() in entry['full_name'].lower()):
            print(f"\033[92m{entry['login']:<10}\033[0m Evo Points: {str(entry['correction_point']):<5} Wallet: {str(entry['wallet']):<10} Pool_Date: {str(entry['pool_month'])} - {str(entry['pool_year'])}")
            image_url = entry['image']
            display(Image(url=image_url['link']))