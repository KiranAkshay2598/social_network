# Social Network API

A high-performance social networking REST API built with Django REST Framework, featuring secure user authentication, paginated user search, automated friend request workflows with custom rate-limiting (max 3 requests/min), and bidirectional friendship management. Built for a technical interview round for a company in 2024, showcasing robust service-layer architecture and containerized Docker deployment.

---

## Key Features

* **User Authentication**: Secure signup and login endpoints returning DRF token authentication headers.
* **User Search**: Search users by exact email match or paginated name search (first name / last name).
* **Friend Request Workflow**: Send friend requests with rate-limiting (maximum 3 requests per minute), accept or reject pending requests.
* **Friend & Pending Lists**: Retrieve bidirectional friend lists and pending incoming friend requests.
* **Docker Support**: Containerized configuration with `Dockerfile` and `docker-compose.yml` for instant setup.
* **Modern Standards**: Django 4.2 & Python 3.11 compatibility, clean service-layer architecture, and PEP8-compliant imports.

---

## Tech Stack

* **Framework**: Django 4.2 & Django REST Framework 3.18
* **Language**: Python 3.11
* **Database**: SQLite (Development)
* **Authentication**: DRF Token Authentication
* **Containerization**: Docker & Docker Compose

---

## Repository Structure

```
social_network/
├── social_network/          # Django inner settings & configuration package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── socialnetworkapp/        # Primary Django application
│   ├── models.py            # Database models (FriendRequest)
│   ├── serializers.py       # DRF Serializers
│   ├── services.py          # Business logic layer (Auth, Search, Friend Requests)
│   ├── views.py             # API View controllers with IsAuthenticated rules
│   └── urls.py              # Endpoint routing
├── postman/                 # Postman collection for API testing
│   └── Social_Network.postman_collection.json
├── .gitignore               # Excludes virtual environments, db, and media files
├── Dockerfile               # Container build configuration
├── docker-compose.yml       # Multi-container orchestration
├── manage.py                # Django command-line utility
└── requirements.txt         # Project dependencies
```

---

## Getting Started

### Prerequisites
* Python 3.11+
* Git
* Docker & Docker Compose

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:KiranAkshay2598/social_network.git
   cd social_network
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

The API will be available at `http://127.0.0.1:8000/`.

---

### Running with Docker

```bash
docker compose up --build
```

---

## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/signup/` | Register a new user account | No |
| `POST` | `/api/v1/login/` | Log in and receive DRF auth token | No |
| `GET` | `/api/v1/search/` | Search users by email or name (paginated) | Yes |
| `POST` | `/api/v1/send-request/` | Send friend request (max 3/min) | Yes |
| `POST` | `/api/v1/respond-request/<id>/` | Accept or reject a friend request | Yes |
| `GET` | `/api/v1/friends/` | View list of accepted friends | Yes |
| `GET` | `/api/v1/pending-requests/` | View list of pending friend requests | Yes |

---

## Postman Collection

A pre-configured Postman collection is included in the `postman/` directory:
* File: `postman/Social_Network.postman_collection.json`

**To use**:
1. Open Postman.
2. Click **Import** and select `Social_Network.postman_collection.json`.
3. Set your `Authorization` header to `Token <your_token>` after logging in.