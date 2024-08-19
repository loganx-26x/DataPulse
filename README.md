# Catalyst Count (Data Pulse)

## Overview
Catalyst Count is a web application built using Django 3.x/4.x, SQLite, and Bootstrap 4/5. The application allows users to log in and upload large CSV data files (up to 1GB) with visual progress indicators. Once the file is uploaded, the application updates the database with the contents of the file and provides a form for users to filter the data and view the count of records based on the applied filters.

### Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/catalyst-count.git
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables:
        ```
        SECRET_KEY=your_secret_key
        ```

5. **Run the initial migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```


7. **Run the development server**
    ```bash
    python manage.py runserver
    ```
