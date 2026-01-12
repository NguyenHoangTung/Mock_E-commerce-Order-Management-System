# E-commerce Order Management System

## Project Overview
This is a comprehensive backend system for an E-commerce Order Management platform. The project is designed with a focus on performance, data integrity, and scalability using modern Python technologies. It features a fully containerized environment and asynchronous background task processing.

## Technology Stack

* **Core Framework:** Python 3.11, FastAPI
* **Database:** PostgreSQL
* **ORM:** Tortoise ORM
* **Asynchronous Processing:** Celery, Redis
* **Monitoring & Logging:** Prometheus, Grafana, Loki, Promtail
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

### 5. Production Monitoring
* **Real-time Metrics:** Tracking RPS, Latency, and Error Rates via Prometheus.
* **Centralized Logging:** Aggregating logs from all services using Loki & Promtail.
* **Visualization:** Interactive dashboards via Grafana.

### 6. Infrastructure & DevOps
* **Dockerized Environment:** The entire stack (Web, Worker, DB, Redis) is orchestrated via Docker Compose.
* **Clean Architecture:** Separation of concerns between Routes, Business Logic, and Data Access layers.

## System Architecture

The system consists of five main containers:
1.  **Web Service:** FastAPI application handling HTTP requests.
2.  **Worker Service:** Celery worker processing background tasks (e.g., emails).
3.  **Database:** PostgreSQL 15.
4.  **Message Broker:** Redis (handling task queues).
5.  **Observability Stack:**
    * **Prometheus:** Scrapes metrics from FastAPI applications.
    * **Loki:** Aggregates logs via Promtail.
    * **Grafana:** Visualizes metrics and logs.

## System Monitoring & Observability

The project comes with a pre-configured monitoring stack (PLG Stack: Prometheus, Loki, Grafana).

### 1. Metrics Dashboard
Visualizes system performance including Requests Per Second (RPS), P99 Latency, and Status Codes.

![Grafana Metrics Dashboard](/static/images/grafanadb.jpeg)
<br>

### 2. Centralized Logging
Real-time log aggregation allowing deep diving into specific requests and error traces using Loki.

![Grafana Logs View](/static/images/lokilog.png)
<br>

**Access Monitoring:**
* **Grafana:** http://localhost:3000 (Default creds: admin/admin)
* **Prometheus:** http://localhost:9090

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
    * **Grafana:** http://localhost:3000

## Testing

The project includes a comprehensive test suite using Pytest.

To run tests inside the Docker container:
```bash
docker-compose exec web pytest
```
Coverage: The current test suite covers approximately 80% of the codebase, including unit tests for Models/Schemas and integration tests for API Routes.