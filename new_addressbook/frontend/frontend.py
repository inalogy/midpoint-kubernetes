import os

import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Define the base URL of your API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Render the login page
@app.route('/')
def login():
    error = request.args.get('error', '')
    return render_template('login.html', error=error)

# Handle login form submission
@app.route('/login', methods=['POST'])
def do_login():
    # Get username and password from the form
    username = request.form['username']
    password = request.form['password']

    # Make a POST request to /api/login to authenticate and obtain the token
    response = requests.post(
        f'{API_BASE_URL}/login',
        json={'username': username, 'password': password})

    if response.status_code == 200:
        # If authentication is successful, get the token from the response
        access_token = response.json()['access_token']
        # Store the token in session or somewhere secure (for simplicity, using a global variable here)
        global ACCESS_TOKEN
        ACCESS_TOKEN = access_token
        # Redirect to the people route
        return redirect(url_for('people'))
    else:
        # If authentication fails, redirect back to the login page with an error message
        return redirect(
            url_for('login', error='Login failed. Please try again.'))



# Render the people page
@app.route('/people')
def people():
    # Make a GET request to /api/people using the token
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(f'{API_BASE_URL}/people', headers=headers)

    if response.status_code == 200:
        # If the request is successful, render the people page with the data
        people_data = response.json()
        print(people_data)
        return render_template('people.html', people=people_data)
    else:
        # If the request fails, display an error message
        return 'Failed to fetch people data.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
