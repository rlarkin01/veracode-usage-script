import sys
import os
from os.path import expanduser
import re
import requests
import json
import csv
from datetime import datetime
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC


admin_base = "https://api.veracode.com/api/authn/v2"
appsec_base = "https://api.veracode.com/appsec/v1"
headers = {"User-Agent": "Python HMAC Example"}


def main():
    creds = get_credentials()

    filename = 'accountDetails_'+datetime.now().strftime("%m.%d.%Y_%H.%M.%S")+'.csv'
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Agency_name","App_total","Static_SCA","Dynamic","Users","Greenlight","eLearning","Admin_count","Admin_usernames","Creator_count","Creator_usernames"])

        for agency in creds:
            if agency[0] != 'default':
                os.environ["VERACODE_API_PROFILE"] = agency[0]
                app_counts = get_app_counts()
                user_counts = get_user_counts()
                writer.writerow([agency[0],app_counts[0],app_counts[1],app_counts[2],user_counts[0],user_counts[1],user_counts[2],user_counts[3],user_counts[4],user_counts[5],user_counts[6]])

    with open(filename, 'r') as f:
        print("results from: " + filename + "\n")
        print(f.read())


def get_credentials():
    pattern = re.compile("\[(.*)\]\s*\nveracode_api_key_id = (.*)\s*\nveracode_api_key_secret = (.*)\s*\n")

    f = open(expanduser("~") + "/.veracode/credentials", "r")
    filetext = f.read()
    f.close()

    return re.findall(pattern, filetext)


def get_app_counts():
    response = make_api_call(appsec_base + "/applications")

    if response.ok:
        data = response.json()
        total, static_sca, dynamic = 0, 0, 0
        for app in data["_embedded"]["applications"]:
            total+=1
            for scan in app["scans"]:
                if scan["scan_type"] == "STATIC":
                    static_sca+=1
                elif scan["scan_type"] == "DYNAMIC":
                    dynamic+=1

        return (total, static_sca, dynamic)
    else:
        print(response.status_code)


def get_user_counts():
    response = make_api_call(admin_base + "/users")

    if response.ok:
        data = response.json()
        total, greenlight, elearn, admins, creators = 0,0,0,0,0
        admin_names, creator_names = [], []
        for user in data["_embedded"]["users"]:
            total+=1
            details = make_api_call(user["_links"]["self"]["href"])
            if details.ok:
                user = details.json()
                creator_already_added = False
                for role in user["roles"]:
                    description = role["role_description"]
                    if description == "Administrator":
                        admins+=1
                        admin_names.append(user["user_name"])
                    elif not creator_already_added and (description == "Security Lead" or description == "Creator"):
                        creators+=1
                        creator_names.append(user["user_name"])
                        creator_already_added = True
                    elif description == "Greenlight IDE User":
                        greenlight+=1
                    elif description == "eLearning":
                        elearn+=1

        return (total, greenlight, elearn, admins, ' AND '.join(admin_names), creators, ' AND '.join(creator_names))
    else:
        print(response.status_code)


def make_api_call(url):
    try:
        return requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
