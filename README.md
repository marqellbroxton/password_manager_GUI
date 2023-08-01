# Password Manager Web Application

This is a simple password manager web application built with Flask. The application securely stores and manages your passwords for different websites and services.

## Features

- User account creation and login: Users can create an account with a unique username and password. Existing users can log in to access their saved passwords.
- Password Management: Users can add, retrieve, edit, and delete passwords associated with different websites.
- Session Management: The application uses Flask's session management to maintain user login status across different pages.

## Installation

1. Make sure you have Python installed on your system.

2. Install the required libraries by running:

```
pip install Flask
```

## How to Use

1. Run the application:

```
python app.py
```

2. Access the application in your web browser at `http://localhost:5000/`.

3. **Create an Account**: If you are a new user, click on the "Create Account" link to create a new account. Enter a unique username and password to sign up.

4. **Log In**: Once you have created an account, use your username and password to log in.

5. **Add Passwords**: After logging in, you can add passwords for different websites or services. Click on the "Add Password" link and enter the website name and the password you want to save.

6. **Retrieve Passwords**: To retrieve a saved password, click on the "Retrieve Password" link, enter the website name, and the corresponding password will be displayed.

7. **Edit Passwords**: If you want to update a password, click on the "Edit Password" link, enter the website name, and provide the new password.

8. **Delete Passwords**: To delete a saved password, click on the "Delete Password" link, enter the website name, and the password will be removed from the database.

9. **Log Out**: You can log out by clicking on the "Log Out" link, which will clear your session and redirect you to the login page.

## Security Note

- The passwords are stored in an SQLite database, and they are not stored in plaintext. The passwords are encrypted using the Fernet encryption algorithm provided by the `cryptography` library.
- The application uses Flask's session management to store the user's login status, which helps maintain user authentication during their interaction with the web application.
- It is recommended to use a strong and unique master password for your account. The password manager will help you securely manage other passwords, but the security of your account largely depends on the strength of the master password.

**Disclaimer**: While efforts have been made to implement security best practices, it is important to understand that no system is completely immune to security risks. Use this password manager at your own risk, and always follow best security practices for managing your passwords.

## Acknowledgments

This password manager web application is built with Flask, a lightweight and efficient web framework in Python. It uses SQLite as the database for storing password information. Thank you to the Flask community and the developers of the required libraries for their contributions.
