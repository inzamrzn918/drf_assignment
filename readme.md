# Django Authentication Project

This project is a Django-based authentication system that includes user registration, login, OTP verification, and profile management. It also includes a simple HTML and JavaScript UI for handling these operations.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [License](#license)

## Features

- User registration with email and password
- OTP verification for user registration
- User login with email and password
- User profile management
- CSRF protection
- Swagger documentation for API endpoints

## Requirements

- Python 3.8+
- Django 5.1.6
- SQLite (default database)
- SMTP server for sending emails (e.g., Gmail)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/inzamrzn918/drf_assignment.git
    cd drf_assignment
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    NB: used pip freeze to collect packages, it looks like a lots

4. **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```


## Configuration

1. **Create a .env file in the project root directory and add the following configuration:**

    ```env
    SECRET_KEY='your-secret-key'
    DEBUG=True

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD='your-email-password'
    ```


## Running the Project

1. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

2. **Open your browser and navigate to:**

    ```
    http://localhost:8000
    ```

## API Endpoints

- **CSRF Token:** `GET /api/csrf-token/`
- **User Registration:** `POST /api/register/`
- **OTP Verification:** `POST /api/verify-otp/`
- **User Login:** `POST /api/login/`
- **User Logout:** `POST /api/logout/`
- **User Details:** `GET /api/me/`
- **UI:** `GET /`

## Usage

1. **User Registration:**

    - Fill in the registration form with your email, password, first name, and last name.
    - Submit the form to receive an OTP via email.

2. **OTP Verification:**

    - Enter the OTP received in your email to verify your account.
    - On successful verification, you will be redirected to the login page.

3. **User Login:**

    - Enter your email and password to log in.
    - On successful login, you will see a welcome message with your profile details and a logout button.

4. **User Profile:**

    - Click on the "My Profile" button to view your profile details.

5. **User Logout:**

    - Click on the "Logout" button to log out of your account.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.