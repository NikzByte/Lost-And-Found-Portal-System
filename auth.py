"""
======================================
auth.py - User Authentication Module
======================================
This file handles user registration, login, and credential storage
for the lost and found system using a JSON-based local database.
Handles account registration and login for the BatStateU Student Portal.
User credentials are stored in users.json, with passwords hashed via SHA-256.

Functions:
    read_logins() -- Loads and returns all users from users.json.
    register()    -- Creates a new account with a validated BatStateU GSuite email.
    login()       -- Authenticates a user by username, email, and password.

Note:
    Users may type 'exit' at any prompt to return to the main menu.

Purpose of the File:
This module provides basic authentication services for the Lost and Found
system. It ensures that only registered users with valid credentials can
access and manage listings within the application.

Author:  Onikka Mae Buela
Date:    April 20, 2026
"""

import hashlib
import json
import os

# ===================
# READ USERS.JSON - 
# ===================
def read_logins():
    # Ensure the file exists and isn't empty so json.load doesn't crash
    if not os.path.exists('users.json') or os.stat('users.json').st_size == 0:
        with open('users.json', 'w') as f:
            json.dump([], f)
        return []
    
    with open('users.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# ===================
# USER REGISTRATION
# ===================
def register():
    print("\nCreate New Account")
    new_username = input("Enter a Username: ").lower()
    
    while True:
        new_gsuiteEmail = input("Enter Your Gsuite Email: ")
        if new_gsuiteEmail == "exit":
            print("\nReturning to Main Menu...")
            return None
        
        if new_gsuiteEmail.endswith("@g.batstate-u.edu.ph"):
            break
        else:
            print("Invalid email. Please use your BatStateU Gsuite email only.")
            
    new_password = input("Enter a Password: ") 
    if new_password == "exit":
        print("\nReturning to Main Menu...")
        return None
        
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    
# Load existing data, append new user dictionary, and rewrite file
    users = read_logins()
    users.append({
        "username": new_username,
        "email": new_gsuiteEmail,
        "password": hashed_password
    })
    
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
         
    print("Registration Successful! You can now log in.")
    return new_username

# ===================
# USER LOGIN
# ===================
def login():
    while True:
        print("\nLog Into Your Account")
        
        userName = input("Enter username: ").lower()
        if userName == 'exit': return None
        
        gsuiteEmail = input("Enter your Gsuite Email: ")
        if gsuiteEmail == 'exit': return None
        
        password = input("Enter password: ")
        if password == 'exit': return None
        
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        
        # Search through the list of dictionaries
        for user in read_logins():
            if (user['username'] == userName and 
                user['email'] == gsuiteEmail and 
                user['password'] == hashed_input):
                print("\nSuccessfully Logged In!")
                return userName
                    
        print("Username/Gsuite/Password Is Incorrect. Try again.")