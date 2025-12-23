# E-commerce Order Management System

## Project Overview
This is a comprehensive backend system for an E-commerce Order Management platform. The project is designed with a focus on performance, data integrity, and scalability using modern Python technologies. It features a fully containerized environment and asynchronous background task processing.

## Technology Stack

* **Core Framework:** Python 3.11, FastAPI
* **Database:** PostgreSQL
* **ORM:** Tortoise ORM
* **Asynchronous Processing:** Celery, Redis
* **Infrastructure:** Docker, Docker Compose
* **Testing:** Pytest, Pytest-asyncio
* **Authentication:** JWT (JSON Web Token)

## Key Features

### 1. User Management
* User registration and secure login (JWT).
* **Asynchronous Email Verification:** Utilizes Celery workers to handle email sending in the background, ensuring immediate API response times.

### 2. Product & Inventory Management
* CRUD operations for products.
* Inventory tracking with optimistic locking to prevent race conditions.
* Media upload support (Local storage).

### 3. Order Processing (High Performance)
* Transactional order creation ensuring ACID properties.
* Real-time inventory deduction using `select_for_update`.

### 4. Payment Integration
* Mock payment gateway integration.
* Webhook implementation to handle payment status updates from external systems.

### 5. Infrastructure & DevOps
* **Dockerized Environment:** The entire stack (Web, Worker, DB, Redis) is orchestrated via Docker Compose.
* **Clean Architecture:** Separation of concerns between Routes, Business Logic, and Data Access layers.

## System Architecture

The system consists of four main containers:
1.  **Web Service:** FastAPI application handling HTTP requests.
2.  **Worker Service:** Celery worker processing background tasks (e.g., emails).
3.  **Database:** PostgreSQL 15.
4.  **Message Broker:** Redis (handling task queues).

## Setup & Installation

### Prerequisites
* Docker Desktop installed.
* Docker Compose installed.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Mock_E-commerce-Order-Management-System
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory. Ensure the database and broker URLs match the Docker service names:
    ```env
    DATABASE_URL=postgres://postgres:password123@db:5432/oms_db
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    SECRET_KEY=your_secret_key
    MAIL_USERNAME=your_email
    MAIL_PASSWORD=your_password
    MAIL_FROM=your_email
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    ```

3.  **Build and Start Services:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Apply Database Migrations:**
    Initialize the database schema inside the container:
    ```bash
    docker-compose exec web aerich upgrade
    ```

5.  **Access the Application:**
    * **Swagger UI:** http://localhost:8000/docs
    * **ReDoc:** http://localhost:8000/redoc

## Testing

The project includes a comprehensive test suite using Pytest.

To run tests inside the Docker container:
```bash
docker-compose exec web pytest
```
Coverage: The current test suite covers approximately 80% of the codebase, including unit tests for Models/Schemas and integration tests for API Routes.