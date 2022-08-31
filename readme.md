# My Tube Backend

## Django Setup

### .ENV

> Create .env file in root directory
>> Add Following env variables

1. DJANGO_SECRET_KEY
2. DB_USERNAME
3. DB_PASSWORD
4. DB_PORT
5. DOMAIN
6. FRONT_END_DOMAIN
7. OAUTH_CALLBACK

> All the Domain should end with / forward slash

### Database

You need Postgres installed into your system

### Virtual Environment

Create a Virtual environment and install python packages from requirements.txt. use this command to install all packages

> pip install -r requirements.txt

#### Google Credential

Create an account on Google developer console
> Enable YouTube Data Api

> Enable Oauth2 and YouTube Public API KEYS
> Add Redirect URI in Oauth2 For Example
> http://localhost:3000/redirecting/

*Go back to .env file and add OAUTH_CALLBACK=redirecting/*

**Download Oauth2 Credentials and rename it as <client_secret.json>**

Place client_secret.json in root directory

You are good to Go

Run
> python3 manage.py runserver 8000




