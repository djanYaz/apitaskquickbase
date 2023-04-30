import base64

import requests
import argparse
import os


# Define command line arguments
parser = argparse.ArgumentParser(description='Map GitHub user data to Freshdesk contact fields')
parser.add_argument('github_username', type=str, help='GitHub username')
parser.add_argument('freshdesk_subdomain', type=str, help='Freshdesk subdomain')

args = parser.parse_args()

github_username = args.github_username
freshdesk_subdomain = args.freshdesk_subdomain

#github_username = input("Enter GitHub username: ")
#freshdesk_subdomain = input("Enter Freshdesk subdomain: ")

# Retrieve GitHub user info
github_token = os.environ['GITHUB_TOKEN']
headers = {'Authorization': f'token {github_token}'}
response = requests.get(f'https://api.github.com/users/{github_username}', headers=headers)
if response.status_code == 200:
    github_user = response.json()

    # Retrieve GitHub user email
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get('https://api.github.com/user/emails', headers=headers)
    if response.status_code == 200:
        emails = response.json()
        primary_email = [email['email'] for email in emails if email['primary']][0]
    else:
        print(f'Failed to retrieve GitHub user emails with status code {response.status_code}')
        print(response.json())

    # Map GitHub user fields to Freshdesk contact fields
    freshdesk_contact = {
        'name': github_user['name'],
        'email': primary_email,
        'job_title': github_user['bio'],
    }

    # Create or update Freshdesk contact
    freshdesk_token = os.environ['FRESHDESK_TOKEN']
    encoded_api_key = base64.b64encode(freshdesk_token.encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": "Basic " + encoded_api_key,
        "content-type": "application/json",
    }

    response = requests.get(f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts', headers=headers)

    if response.status_code == 200:
        contacts = response.json()
        for contact in contacts:
            if contact['email'] == primary_email:
                contact_id = contact['id']
                # Update existing contact
                response = requests.put(f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts/{contact_id}',
                                        headers=headers, json=freshdesk_contact)
                if response.status_code == 200:
                    print('Contact updated successfully')
                else:
                    print(f'Failed to update contact with status code {response.status_code}')
                    print(response.json())
                break
        else:
            # Create new contact
            response = requests.post(f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts', headers=headers,
                                     json=freshdesk_contact)
            if response.status_code == 201:
                print('Contact created successfully')
            else:
                print(f'Failed to create contact with status code {response.status_code}')
                print(response.json())
    else:
        print(f'Failed to retrieve contacts with status code {response.status_code}')
        print(response.json())
