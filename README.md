
# 🛍️ Shop API (Django REST Framework)

Onlayn do‘kon uchun API — mahsulotlar, buyurtmalar, savat va foydalanuvchilarni boshqarish imkoniyatiga ega.  
**JWT autentifikatsiya**, **Swagger hujjatlari** va **RESTful arxitektura** asosida qurilgan.  

---

## 🚀 Texnologik stek
- **Python** 3.10+
- **Django** 4.x
- **Django REST Framework** 3.x
- **PostgreSQL** yoki **SQLite3**
- **Simple JWT** — autentifikatsiya
- **drf-yasg** — Swagger hujjatlari
- **django-filter** — filtrlash

---

## 📂 Loyiha tuzilmasi
```
shop_api/
│
├── shop_api/                 # Asosiy sozlamalar va URL mapping
├── users/                    # Foydalanuvchilar (register, login, admin boshqaruv)
├── products/                 # Mahsulotlar, toifalar va teglar
├── cart/                     # Savat (qo‘shish, ko‘rish, o‘chirish)
├── orders/                   # Buyurtmalar (foydalanuvchi va admin boshqaruvi)
└── requirements.txt
```

---

## ⚙️ O‘rnatish va ishga tushirish

### 1. Repozitoriyani yuklab oling
```bash
git clone https://github.com/username/shop_api.git
cd shop_api
```

### 2. Virtual muhit yaratish va faollashtirish
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Kerakli paketlarni o‘rnatish
```bash
pip install -r requirements.txt
```

### 4. Migratsiyalarni bajarish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

---

## 🔑 Autentifikatsiya

**Simple JWT** orqali ishlaydi.  

- **Token olish:** `POST /api/token/`  
- **Tokenni yangilash:** `POST /api/token/refresh/`

---

## 📌 Asosiy Endpointlar

### **Auth (JWT)**
- `POST /api/users/register/` – Ro‘yxatdan o‘tish  
- `POST /api/token/` – Login (access & refresh token olish)  
- `POST /api/token/refresh/` – Token yangilash  

### **Products & Categories**
- `GET /api/products/` – Mahsulotlar (filter, qidiruv, sort, sahifalash bilan)  
- `GET /api/products/<id>/` – Bitta mahsulot detali  
- `GET /api/products/categories/` – Toifalar ro‘yxati  
- **Admin:** CRUD (mahsulot, toifa, teglar)

### **Cart**
- `GET /api/cart/` – Savatni ko‘rish  
- `POST /api/cart/` – Mahsulot qo‘shish  
- `PUT /api/cart/item/<id>/` – Miqdorni yangilash  
- `DELETE /api/cart/item/<id>/` – Mahsulotni o‘chirish  

### **Orders**
- `GET /api/orders/` – Foydalanuvchi buyurtmalari (filter + sahifalash)  
- `POST /api/orders/` – Buyurtma yaratish  
- **Admin:** Barcha buyurtmalarni ko‘rish va holatini yangilash

### **Users (Admin)**
- `GET /api/users/admin/` – Foydalanuvchilar ro‘yxati  
- `GET /api/users/admin/<id>/` – Foydalanuvchi profili  
- `PUT /api/users/admin/<id>/` – Yangilash  
- `DELETE /api/users/admin/<id>/` – O‘chirish  

---

## 📖 Swagger hujjatlari
Hamma endpointlar uchun **Swagger UI** mavjud:  
```
GET /api/docs/
```

---

## 🛡️ Xavfsizlik
- **JWT tokenlar** orqali autentifikatsiya.  
- **Permissions**:  
  - `IsAuthenticated` – foydalanuvchilar uchun.  
  - `IsAdminUser` – admin uchun.  
- **Serializer validatsiyasi** – kiritilgan ma’lumotlarni tekshiradi.  

