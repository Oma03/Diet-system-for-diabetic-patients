# Diet System for Diabetic Patients

A backend system built with Django and Django REST Framework to support diet planning and tracking for diabetic patients. The API enables patients and caregivers to manage meal plans, monitor food intake, and make informed nutritional decisions based on diabetic health needs.

---

## 🚀 Features

- 🥗 Create and manage user-specific diet plans
- 📅 Schedule meals and assign food types
- 📊 Track and review daily/weekly dietary records
- 🔐 Token-based user authentication (JWT)
- 🔄 API endpoints for seamless frontend integration

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite (default), configurable to PostgreSQL
- **Authentication:** JWT (via `djangorestframework-simplejwt`)
- **Environment:** Django environment config using `.env` file

---

## 📁 Project Structure

```bash
diet-system/
├── diet/                  # Core diet app (models, views, serializers)
├── users/                 # User authentication and profile logic
├── config/                # Django settings and URLs
├── manage.py
├── requirements.txt
