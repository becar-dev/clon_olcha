# 🛍️ Olcha.uz Clone - RESTful API

This is a RESTful API built using **Django Rest Framework** that replicates core functionalities of the e-commerce platform [Olcha.uz](https://olcha.uz). The API provides endpoints for products, categories, reviews, and user accounts with full CRUD capabilities, JWT authentication, custom permissions, caching, filtering, and more.

---

## 📎 Project Links

- 🔗 **Live API**: [https://clon-olcha.onrender.com/](https://clon-olcha.onrender.com/)
- 📘 **Swagger Documentation**: [https://clon-olcha.onrender.com/swagger/](https://clon-olcha.onrender.com/swagger/)
- 🧑‍💻 **GitHub Repository**: [https://github.com/becar-dev/clon_olcha.git](https://github.com/becar-dev/clon_olcha.git)

---

## ✅ Features Overview

### 1. ViewSets with Django REST Framework
All views are implemented using `ModelViewSet` to provide built-in CRUD operations in a clean and consistent structure for:
- Products
- Categories
- Reviews
- User Accounts

### 2. 🔐 Authentication (JWT)
Authentication is handled via `djangorestframework-simplejwt`, providing:
- `/api/v1/login/` – for obtaining `access` and `refresh` tokens
- Token-based secured access for user-related endpoints

### 3. 🛡️ Custom Permissions
Implemented `IsOwnerOrReadOnly` permission class for the **reviews** app:
- Users can **only update or delete** their own reviews
- All users can **read** others' reviews

### 4. ⚡ Caching (Performance Boost)
To improve speed and reduce database load:
- Frequently accessed endpoints (like product list and details) are cached using `@cache_page`
- Cache timeout: **5 minutes**

### 5. 🧠 Optimization
Improved query performance using:
- `select_related` and `prefetch_related` to solve **N+1 problem**
- `django-mptt` for efficient hierarchical category queries
- Entire category tree fetched in one DB query and assembled in-memory

### 6. 🔎 Search & Filter
Powered by `django-filter`:
- Filter by **category**, including **sub-categories**
- Filter by **price range**
- Search by **product name** and **description**
- Sort by **price** or **date added**

### 7. 🔔 Signals
Improved automation via Django signals:
- `post_save` creates a **UserProfile** when a new `CustomUser` registers
- `post_save` and `post_delete` on reviews auto-update the **product's average rating**

### 8. 🧭 Middleware
Custom `RequestTimeLoggingMiddleware` logs how long each request takes:
- Helps identify and optimize slow endpoints in production

### 9. ☁️ Deployment
Deployed on [Render.com](https://render.com) with:
- **PostgreSQL** as the production database
- **Gunicorn** as WSGI HTTP server
- **WhiteNoise** for serving static files
- Production-ready configurations applied

---

## 📦 Tech Stack

| Category        | Technology                    |
|----------------|-------------------------------|
| Framework      | Django, Django REST Framework |
| Auth           | JWT (`djangorestframework-simplejwt`) |
| Caching        | Django Cache Framework        |
| ORM Optimization | select_related, prefetch_related |
| Tree Models    | django-mptt                   |
| Filtering      | django-filter                 |
| Deployment     | Render.com, Gunicorn          |
| Documentation  | drf-yasg (Swagger UI)         |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip / poetry

### Installation

```bash
git clone https://github.com/becar-dev/clon_olcha.git
cd clon_olcha
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file and configure your environment variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Apply Migrations & Run Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🧪 API Usage (Quick Example)

### 🔑 Get Token

```http
POST /api/v1/login/
{
  "username": "your_user",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "....",
  "refresh": "...."
}
```

Use the `access` token in Authorization headers:

```http
Authorization: Bearer <access_token>
```

---

## 🧰 Developer Notes

- Run tests: `python manage.py test`
- Swagger available at `/swagger/`
- Admin panel: `/admin/`

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome!  
Feel free to check [issues page](https://github.com/becar-dev/clon_olcha/issues).

---

## 🧑‍💼 Author

**Bekzod (becar-dev)**  
🔗 GitHub: [@becar-dev](https://github.com/becar-dev)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
