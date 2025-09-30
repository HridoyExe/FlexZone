🏋️ Gym Management System API Documentation

The Gym Management System API is a complete RESTful API built with Django and Django REST Framework. It allows management of memberships, subscriptions, fitness classes, class bookings, attendance, payments, and feedback.
Authentication is handled via JWT using Djoser.

🌐 Base URLs
Service	URL
API	/api/
Authentication	/auth/
Swagger UI	/swagger/
Redoc UI	/redoc/

All endpoints require authentication unless otherwise noted. Permissions are role-based (Admin, Staff, Member).

🔐 Authentication Endpoints
Method	Endpoint	Description
POST	/auth/jwt/create/	Obtain JWT token
POST	/auth/jwt/refresh/	Refresh JWT token
POST	/auth/jwt/verify/	Verify JWT token
GET	/auth/users/me/	Retrieve current user profile
PUT	/auth/users/me/	Update current user profile
PATCH	/auth/users/me/	Partial update of current user profile
DELETE	/auth/users/me/	Delete current user
GET	/auth/users/	List all users
POST	/auth/users/	Create a new user
POST	/auth/users/activation/	Activate a user
POST	/auth/users/resend_activation/	Resend activation email
POST	/auth/users/reset_email/	Request email reset
POST	/auth/users/reset_email_confirm/	Confirm email reset
POST	/auth/users/reset_password/	Request password reset
POST	/auth/users/reset_password_confirm/	Confirm password reset
POST	/auth/users/set_email/	Set email
POST	/auth/users/set_password/	Set password
GET	/auth/users/{id}/	Retrieve user by ID
PUT	/auth/users/{id}/	Update user by ID
PATCH	/auth/users/{id}/	Partial update user by ID
DELETE	/auth/users/{id}/	Delete user by ID
🏷 Membership Endpoints
Method	Endpoint	Description
GET	/api/memberships/	List all memberships
POST	/api/memberships/	Create a new membership
GET	/api/memberships/{id}/	Retrieve a membership
PUT	/api/memberships/{id}/	Update a membership
PATCH	/api/memberships/{id}/	Partial update a membership
DELETE	/api/memberships/{id}/	Delete a membership
💳 Subscription Endpoints
Method	Endpoint	Description
GET	/api/subscriptions/	List all subscriptions
POST	/api/subscriptions/	Create a new subscription
GET	/api/subscriptions/{id}/	Retrieve a subscription
PUT	/api/subscriptions/{id}/	Update a subscription
PATCH	/api/subscriptions/{id}/	Partial update a subscription
DELETE	/api/subscriptions/{id}/	Delete a subscription
🏋️ Fitness Classes Endpoints
Method	Endpoint	Description
GET	/api/fitness-classes/	List all fitness classes
POST	/api/fitness-classes/	Create a new fitness class
GET	/api/fitness-classes/{id}/	Retrieve a fitness class
PUT	/api/fitness-classes/{id}/	Update a fitness class
PATCH	/api/fitness-classes/{id}/	Partial update a fitness class
DELETE	/api/fitness-classes/{id}/	Delete a fitness class
🔹 Nested Endpoints for Fitness Classes
Attendance
Method	Endpoint	Description
GET	/api/fitness-classes/{fitness_class_pk}/attendance/	List attendance for a class
POST	/api/fitness-classes/{fitness_class_pk}/attendance/	Create attendance for a class
GET	/api/fitness-classes/{fitness_class_pk}/attendance/{id}/	Retrieve an attendance record
PUT	/api/fitness-classes/{fitness_class_pk}/attendance/{id}/	Update an attendance record
PATCH	/api/fitness-classes/{fitness_class_pk}/attendance/{id}/	Partial update an attendance record
DELETE	/api/fitness-classes/{fitness_class_pk}/attendance/{id}/	Delete an attendance record
Bookings
Method	Endpoint	Description
GET	/api/fitness-classes/{fitness_class_pk}/bookings/	List class bookings
POST	/api/fitness-classes/{fitness_class_pk}/bookings/	Create a class booking
GET	/api/fitness-classes/{fitness_class_pk}/bookings/{id}/	Retrieve a booking
PUT	/api/fitness-classes/{fitness_class_pk}/bookings/{id}/	Update a booking
PATCH	/api/fitness-classes/{fitness_class_pk}/bookings/{id}/	Partial update a booking
DELETE	/api/fitness-classes/{fitness_class_pk}/bookings/{id}/	Delete a booking
Feedbacks
Method	Endpoint	Description
GET	/api/fitness-classes/{fitness_class_pk}/feedbacks/	List feedbacks for a class
POST	/api/fitness-classes/{fitness_class_pk}/feedbacks/	Create feedback for a class
GET	/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/	Retrieve feedback
PUT	/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/	Update feedback
PATCH	/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/	Partial update feedback
DELETE	/api/fitness-classes/{fitness_class_pk}/feedbacks/{id}/	Delete feedback
📅 Class Bookings Endpoints
Method	Endpoint	Description
GET	/api/class-bookings/	List all class bookings
POST	/api/class-bookings/	Create a new class booking
GET	/api/class-bookings/{id}/	Retrieve a booking
PUT	/api/class-bookings/{id}/	Update a booking
PATCH	/api/class-bookings/{id}/	Partial update a booking
DELETE	/api/class-bookings/{id}/	Delete a booking
📝 Attendance Endpoints
Method	Endpoint	Description
GET	/api/attendance/	List all attendance records
POST	/api/attendance/	Create a new attendance record
GET	/api/attendance/{id}/	Retrieve an attendance record
PUT	/api/attendance/{id}/	Update attendance record
PATCH	/api/attendance/{id}/	Partial update attendance
DELETE	/api/attendance/{id}/	Delete attendance record
💵 Payments Endpoints
Method	Endpoint	Description
GET	/api/payments/	List all payments
POST	/api/payments/	Create a new payment
GET	/api/payments/{id}/	Retrieve a payment
PUT	/api/payments/{id}/	Update a payment
PATCH	/api/payments/{id}/	Partial update payment
DELETE	/api/payments/{id}/	Delete a payment
📝 Feedback Endpoints
Method	Endpoint	Description
GET	/api/feedbacks/	List all feedbacks
POST	/api/feedbacks/	Create feedback
GET	/api/feedbacks/{id}/	Retrieve feedback
PUT	/api/feedbacks/{id}/	Update feedback
PATCH	/api/feedbacks/{id}/	Partial update feedback
DELETE	/api/feedbacks/{id}/	Delete feedback
📊 Reports Endpoints
Method	Endpoint	Description
GET	/api/reports/attendance/	Attendance report
GET	/api/reports/feedback/	Feedback report
GET	/api/reports/membership/	Membership report

✅ Note: All endpoints require authentication unless explicitly stated. Role-based permissions are applied for Admin, Staff, and Member.