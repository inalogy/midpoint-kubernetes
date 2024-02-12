import math
import os

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Define the base URL of your API
API_INGRESS_URL = os.getenv("API_INGRESS_URL", "http://localhost:8000/api")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Render the login page
@app.route('/')
def show_full_list():
    headers = [
        "department", "position", "first_name", "last_name", "display_name", 
        "sex", "birthdate", "id_card", "personal_email", "personal_phone",
        "iban", "home_street", "home_city", "home_postal_code", "home_country",
        "work_street", "work_city", "work_postal_code", "work_country",
        "language", "nationality", "employment_type", "division", "picture"]
    response = requests.get(f"{API_BASE_URL}/employees")
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    data = response.json()
    num_pages = math.ceil(len(data) / per_page)
    show = data[start_index:end_index]
    return render_template(
        'hr.html', people=show, headers=headers, num_pages=num_pages, page=page,
        url=API_INGRESS_URL)

@app.route('/edit/<int:id>')
def edit_employee(id):
    headers = [
        "id", "department", "position", "first_name", "last_name", "display_name", 
        "sex", "birthdate", "id_card", "personal_email", "personal_phone",
        "iban", "home_street", "home_city", "home_postal_code", "home_country",
        "work_street", "work_city", "work_postal_code", "work_country",
        "language", "nationality", "employment_type", "division", "picture"]
    response = requests.get(f"{API_INGRESS_URL}/employees/{id}")
    return render_template('edit.html', headers=headers, data=response.json(),
                           url=API_BASE_URL)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
