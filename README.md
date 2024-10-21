# MINI-TWITTER-PROJECT
Repository made to store my code for the b2bit selection process.

## Overview

This project is a mini Twitter clone, created as part of the selection process for b2bit. It includes basic functionality such as user registration, tweet creation, and more, providing a simplified version of the well-known social media platform.

## Getting Started

To run the application, please follow the steps below. The API documentation is automatically generated and can be accessed at the endpoint /swagger/ once the API is running.

### Prerequisites
 - Python 3.12
 - django and djangorestframework
 - PostgreSQL
 - Docker 

 ### Installation
1. Clone this repository:

2. Have Docker and Python installing in your computer:

3. Open terminal in your IDE:
- Execute this commands: `docker-compose up --build`
- The database may not be migrating, just use the `docker-compose exec web python manage.py migrate` command

4. Access the API documentation:
- Open your browser and navigate to http://127.0.0.1:8000/swagger/ to view the interactive API documentation.

## Features
- User authentication (JWT-based).

- Tweet creation and listing.

- Follow and unfollow users.

- Basic timeline functionality.

## API Documentation
The API documentation is automatically generated and available at /swagger/. This includes all the endpoints, input parameters, and response formats to help developers interact with the API.

## Developer Notes

- Tests are located in the tests/ directory and can be run using pytest.