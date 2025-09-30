# 🏋️ Gym Management System API Documentation

The **Gym Management System API** is a complete RESTful API built with **Django** and **Django REST Framework**.  
It allows management of **memberships, subscriptions, fitness classes, class bookings, attendance, payments, and feedback**.  
Authentication is handled via **JWT** using **Djoser**.

---

## 🌐 Base URLs

| Service         | URL        |
|-----------------|------------|
| **API**         | `/api/`    |
| **Authentication** | `/auth/`   |
| **Swagger UI**  | `/swagger/` |
| **Redoc UI**    | `/redoc/`   |

> ✅ All endpoints require authentication unless otherwise noted.  
> 🔑 Permissions are **role-based**: `Admin`, `Staff`, `Member`.

---

## 🔐 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/auth/jwt/create/` | Obtain JWT token |
| POST   | `/auth/jwt/refresh/` | Refresh JWT token |
| POST   | `/auth/jwt/verify/` | Verify JWT token |
| GET    | `/auth/users/me/` | Retrieve current user profile |
| PUT    | `/auth/users/me/` | Update current user profile |
| PATCH  | `/auth/users/me/` | Partial update user profile |
| DELETE | `/auth/users/me/` | Delete current user |
| GET    | `/auth/users/` | List all users |
| POST   | `/auth/users/` | Create a new user |
| POST   | `/auth/users/activation/` | Activate a user |
| POST   | `/auth/users/resend_activation/` | Resend activation email |
| POST   | `/auth/users/reset_email/` | Request email reset |
| POST   | `/auth/users/reset_email_confirm/` | Confirm email reset |
| POST   | `/auth/users/reset_password/` | Request password reset |
| POST   | `/auth/users/reset_password_confirm/` | Confirm password reset |
| POST   | `/auth/users/set_email/` | Set email |
| POST   | `/auth/users/set_password/` | Set password |
| GET    | `/auth/users/{id}/` | Retrieve user by ID |
| PUT    | `/auth/users/{id}/` | Update user by ID |
| PATCH  | `/auth/users/{id}/` | Partial update user by ID |
| DELETE | `/auth/users/{id}/` | Delete user by ID |

---

## 🏷 Membership Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/memberships/` | List all memberships |
| POST   | `/api/memberships/` | Create a new membership |
| GET    | `/api/memberships/{id}/` | Retrieve a membership |
| PUT    | `/api/memberships/{id}/` | Update a membership |
| PATCH  | `/api/memberships/{id}/` | Partial update membership |
| DELETE | `/api/memberships/{id}/` | Delete a membership |

---

## 💳 Subscription Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/subscriptions/` | List all subscriptions |
| POST   | `/api/subscriptions/` | Create a subscription |
| GET    | `/api/subscriptions/{id}/` | Retrieve a subscription |
| PUT    | `/api/subscriptions/{id}/` | Update a subscription |
| PATCH  | `/api/subscriptions/{id}/` | Partial update subscription |
| DELETE | `/api/subscriptions/{id}/` | Delete a subscription |

---

## 🏋️ Fitness Classes Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/fitness-classes/` | List all fitness classes |
| POST   | `/api/fitness-classes/` | Create a fitness class |
| GET    | `/api/fitness-classes/{id}/` | Retrieve a fitness class |
| PUT    | `/api/fitness-classes/{id}/` | Update a fitness class |
| PATCH  | `/api/fitness-classes/{id}/` | Partial update fitness class |
| DELETE | `/api/fitness-classes/{id}/` | Delete a fitness class |

---

### 🔹 Nested Endpoints (Fitness Classes)

#### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/fitness-classes/{fitness_class_pk}/attendance/` | List attendance |
| POST   | `/api/fitness-classes/{fitness_class_pk}/attendance/` | Create attendance |
| GET    | `/api/fitness-classes/{fitness_class_pk}/attendance/{id}/` | Retrieve record |
| PUT    | `/api/fitness-classes/{fitness_class_pk}/attendance/{id}/` | Update record |
| PATCH  | `/api/fitness-classes/{fitness_class_pk}/attendance/{id}/` | Partial update |
| DELETE | `/api/fitness-classes/{fitness_class_pk}/attendance/{id}/` | Delete record |

#### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/fitness-classes/{fitness_class_pk}/bookings/` | List bookings |
| POST   | `/api/fitness-classes/{fitness_class_pk}/bookings/` | Create booking |
| GET    | `/api/fitness-classes/{fitness_class_pk}/bookings/{id}/` | Retrieve booking |
| PUT    | `/api/fitness-classes/{fitness_class_pk}/bookings/{id}/` | Update booking |
| PATCH  | `/api/fitness-classes/{fitness_class_pk}/bookings/{id}/` | Partial update |
| DELETE | `/api/fitness-classes/{fitness_class_pk}/bookings/{id}/` | Delete booking |

#### Feedbacks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/fitness-classes/{fitness_class_pk}/feedbacks/` | List feedbacks |
| POST   | `/api/fitness-classes/{fitness_class_pk}/feedbacks/` | Create feedback |
| GET    | `/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/` | Retrieve feedback |
| PUT    | `/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/` | Update feedback |
| PATCH  | `/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/` | Partial update |
| DELETE | `/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/` | Delete feedback |

---

## 📅 Class Bookings Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/class-bookings/` | List all bookings |
| POST   | `/api/class-bookings/` | Create booking |
| GET    | `/api/class-bookings/{id}/` | Retrieve booking |
| PUT    | `/api/class-bookings/{id}/` | Update booking |
| PATCH  | `/api/class-bookings/{id}/` | Partial update |
| DELETE | `/api/class-bookings/{id}/` | Delete booking |

---

## 📝 Attendance Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/attendance/` | List records |
| POST   | `/api/attendance/` | Create record |
| GET    | `/api/attendance/{id}/` | Retrieve record |
| PUT    | `/api/attendance/{id}/` | Update record |
| PATCH  | `/api/attendance/{id}/` | Partial update |
| DELETE | `/api/attendance/{id}/` | Delete record |

---

## 💵 Payments Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/payments/` | List payments |
| POST   | `/api/payments/` | Create payment |
| GET    | `/api/payments/{id}/` | Retrieve payment |
| PUT    | `/api/payments/{id}/` | Update payment |
| PATCH  | `/api/payments/{id}/` | Partial update |
| DELETE | `/api/payments/{id}/` | Delete payment |

---

## 📝 Feedback Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/feedbacks/` | List feedbacks |
| POST   | `/api/feedbacks/` | Create feedback |
| GET    | `/api/feedbacks/{id}/` | Retrieve feedback |
| PUT    | `/api/feedbacks/{id}/` | Update feedback |
| PATCH  | `/api/feedbacks/{id}/` | Partial update |
| DELETE | `/api/feedbacks/{id}/` | Delete feedback |

---

## 📊 Reports Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/reports/attendance/` | Attendance report |
| GET    | `/api/reports/feedback/` | Feedback report |
| GET    | `/api/reports/membership/` | Membership report |

---

✅ **Note:** All endpoints require authentication unless explicitly stated.  
🔑 **Role-based permissions**: `Admin`, `Staff`, `Member`.  
