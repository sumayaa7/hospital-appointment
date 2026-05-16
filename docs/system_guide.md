# Hospital Appointment System Guide
## System purpose
This platform allows patients to book doctor appointments in available time slots.
## Main features
- View available doctors and specializations
- View available slots for upcoming days
- Book a free slot with patient name and phone
- Cancel appointment via unique cancel token link
- Admin page to see all appointments
## Routes
- GET / : Main booking page
- GET /slots/<slot_id>/book : Booking form page for slot
- POST /slots/<slot_id>/book : Create appointment for slot
- GET /cancel/<token> : Cancel appointment by token
- GET /admin/appointments : List all appointments for admin view
## Booking rules
- One slot can have only one active appointment
- If slot is already booked, booking is rejected
- Patient name must be at least 2 characters
- Phone must be at least 5 characters
## Data model
- Doctor: full_name, specialty
- Slot: doctor_id, start_at, duration_min
- Appointment: slot_id, patient_name, phone, status, cancel_token, created_at
## Tech stack
- Backend: Flask
- Database: SQLite via Flask-SQLAlchemy
- Templates: Jinja2
- Styling: static CSS
## Authentication
No user login is implemented in current version.
Admin page is open in this demo setup.
## Deployment note
Development server uses Flask debug mode and is not for production.
