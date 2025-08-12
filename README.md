# **EcoSale API**

EcoSale API is the backend service for the EcoSale E-commerce Platform, built with Django REST Framework (DRF).
It provides APIs for authentication, products, orders, carts, and wishlists — complete with Swagger and Redoc documentation.
**Note: No 3RD PARTY API INTEGRATED**
---

## **Features**

* 🔐 **JWT Authentication** (with `djangorestframework-simplejwt`)
* 🛍 **Product & Order Management**
* 🛒 **Shopping Cart & Wishlist**
* 📝 **API Documentation** (Swagger & Redoc via `drf-yasg`)
* 🎨 **Modern Admin Interface** (via `django-jazzmin`)
* 🌐 **CORS Enabled** (for frontend integration)
* 📦 **Static & Media Files Handling**
* 🚀 **Production Ready** (with `gunicorn` & `whitenoise`)

---

## **Tech Stack**

* **Backend Framework:** Django 5+ & Django REST Framework
* **Database:** SQLite (development), PostgreSQL (production-ready)
* **Authentication:** JWT
* **Documentation:** Swagger & Redoc
* **Deployment:** Render (Gunicorn + Whitenoise)

---

## **Installation & Setup**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jamesadewara/EcoSale_backend_demo.git
cd EcoSale-api
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost,https://EcoSale-backend-demo.onrender.com

# Database
DATABASE_URL=postgresurl

# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=30
REFRESH_TOKEN_LIFETIME_DAYS=1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://EcoSale-backend-demo.onrender.com
```

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 6️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Start the Development Server

```bash
python manage.py runserver
```

---

## **API Documentation**

Once the server is running:

* **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **Redoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## **Production (Render) Deployment**

Gunicorn is used as the WSGI HTTP server.

**Procfile:**

```bash
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Static files** are served via Whitenoise. Make sure `DEBUG=False` in production and run:

```bash
python manage.py collectstatic --noinput
```

---

## **Endpoints Overview**

| Method | Endpoint                     | Description             |
| ------ | ---------------------------- | ----------------------- |
| POST   | `/api/auth/login/`           | User login              |
| POST   | `/api/auth/register/`        | User registration       |
| GET    | `/api/products/`             | List products           |
| POST   | `/api/cart/add_item/`        | Add item to cart        |
| POST   | `/api/wishlist/add_product/` | Add product to wishlist |
| POST   | `/api/orders/checkout/`      | Checkout order          |

---

## **License**

This project is licensed under the BSD License.