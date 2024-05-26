# Alog_BACKEND


## Introduction
Alog_BACKEND is a dairy farm monitoring system that provides a comprehensive API for managing cows and their sensor data. The project aims to help farmers track the health and activity of their cows using sensor data.

## Features
- User authentication with JWT
- CRUD operations for cows and sensor data
- Health status monitoring of cows
- Data parsing and health status determination

## Getting Started
These instructions will help you set up the project on your local machine for development and testing purposes.

## Prerequisites
- Python 3.x
- Docker
- Docker Compose

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Djaam/Alog_BACKEND.git
   cd Alog_BACKEND
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application using Docker:
   ```sh
   docker-compose up
   ```

## Usage
1. Create a superuser to access the admin panel:
   ```sh
   python manage.py createsuperuser
   ```

2. Start the development server:
   ```sh
   python manage.py runserver
     ```

## API Endpoints
- `POST /signup/`: Create a new user account
- `POST /login/`: Obtain a JWT token
- `GET /cows/`: List all cows for the authenticated user
- `POST /cows/`: Add a new cow
- `GET /cows/{id}/`: Retrieve details of a specific cow
- `PUT /cows/{id}/`: Update details of a specific cow
- `DELETE /cows/{id}/`: Delete a specific cow
- `GET /sensor_data/`: List all sensor data for cows belonging to the authenticated user
- `POST /sensor_data/`: Add new sensor data
- `GET /sensor_data/{cow_id}/`: Retrieve sensor data for a specific cow
