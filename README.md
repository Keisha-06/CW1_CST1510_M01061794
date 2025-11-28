Student Name: [Keisha]
Student ID: [M01061794]
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

# Project Description

A command-line authentication system implenenting secure password hashing. 
This system allows users to register accounts and log in with proper password.

## Features

- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implimentation

- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain file ('users.txt')
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters) , Password (6-50 characters)