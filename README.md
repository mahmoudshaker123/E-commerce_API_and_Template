# E-commerce API & Template

## Overview
This project is a full-featured **E-commerce platform** built using **Django**, **Django REST Framework (DRF)**, and **Django Templates**. It provides a **RESTful API** for backend operations and also supports template-based rendering for frontend pages.

## Technologies Used
- **Django** – Web framework for backend logic.
- **Django REST Framework (DRF)** – For building the API.
- **Docker** – For containerization and easy deployment.
- **Celery** – For handling asynchronous tasks.
- **Redis** – As a message broker for Celery and caching.
- **API & Templates** – Supports both API-based and template-based interactions.

## Features
### **1. User Authentication & Authorization**
- User registration and login.
- Token-based authentication.
- Role-based access control (Admin, Seller, Customer).

### **2. Product Management**
- CRUD operations for products.
- Categories and filtering options.
- Product images and descriptions.

### **3. Cart & Checkout System**
- Add/remove products from cart.
- Secure checkout process.
- Order history tracking.

### **4. Payment Integration**
- Support for multiple payment gateways.
- Secure transaction handling.

### **5. Order Management**
- Track order status (Pending, Shipped, Delivered, etc.).
- Order cancellation and refunds.

### **6. Celery & Redis for Background Tasks**
- Email notifications.
- Order processing automation.
- Caching for improved performance.

### **7. API & Templates**
- RESTful API for frontend integration.
- HTML templates for server-side rendering.

## Installation & Setup
### **1. Clone the Repository**
```sh
git clone https://github.com/mahmoudshaker123/E-commerce_API_and_Template.git
cd E-commerce_API_and_Template
```

### **2. Set Up Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Run Migrations**
```sh
python manage.py migrate
```

### **5. Run the Development Server**
```sh
python manage.py runserver
```

## Docker Setup
```sh
docker-compose up --build
```

## Future Enhancements
- Implementing GraphQL support.
- Adding AI-based recommendations.
- Multi-language support.

---
📌 **Feel free to contribute or suggest improvements!** 🚀

