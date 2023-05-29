"""
Script: User Data Import Script
Description: This script retrieves user data from an external API and inserts it into a MySQL database.
Dependencies: Python requests library, mysql-connector-python library
Pre-requisites: API credentials, MySQL database configuration
"""

import requests
import mysql.connector

data = []
base_url = "https://dummyapi.io/data/v1" # Base URL for the external API
params = {
    "limit": "20",
    "page": "0"
}
headers = {
    "Content-Type": "application/json",
    "app-id": '<app-id>', # API credentials for authentication
}

"""
Fetches user data from the external API.

Parameters:
- None

Returns:
- List of user objects in JSON format
"""
users_response = requests.get(
    base_url+'/user', params=params, headers=headers
)
users_response = requests.get(
    base_url+'/user', params=params, headers=headers
)
if users_response.status_code == 200:
    users = users_response.json()["data"]
    for user in users:
		"""
		Fetches a single user's data from the external API.

		Parameters:
		- Query: user_id (string)

		Returns:
		- A user object in JSON format
		"""
        single_user_response = requests.get(
            base_url+'/user/'+user["id"],
            params=params,
            headers=headers,
        )
        if single_user_response.status_code == 200:
            single_user = single_user_response.json()
            if single_user["gender"] == "male":
                print(f"The name {single_user['firstName']} contains "
                    f"{len(single_user['firstName'])} characters")
                data.append((
                    single_user["firstName"],
                    single_user["lastName"],
                    single_user["dateOfBirth"],
                    single_user["gender"],
                    len(single_user['firstName'])
                ))
        else:
            print(f"Request to {base_url+'/user/'+user['id']} "
                f"failed with status code: {response.status_code}")
else:
    print(f"Request to {base_url+'/user'} failed with "
        f"status code: {response.status_code}")

"""
Connects to the MySQL database and inserts user data.

Parameters:
- data: List of user data tuples to be inserted into the database
"""
try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='<password>',
        database='dummyapi'
    )
    print('Connected to MySQL database')
except mysql.connector.Error as error:
    print('Failed to connect to MySQL database:', error)
    exit()

cursor = connection.cursor()
insert_query = '''INSERT INTO users (
    first_name,
    last_name,
    dob,
    gender,
    name_character_count
) VALUES (%s, %s, %s, %s, %s)'''

try:
    cursor.executemany(insert_query, data)
    connection.commit()
    print('Data inserted successfully')
except mysql.connector.Error as error:
    print('Failed to insert data:', error)
    connection.rollback()

cursor.close()
connection.close()
print('MySQL connection closed')
