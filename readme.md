# 🧑‍💼 Django Job Portal

A full-featured Job Portal built with Django where Employers can post jobs and Job Seekers can apply.

---

## 🔧 Features

### 👤 User Roles:
- **Employers**:
  - Register & complete company profile
  - Post, edit, and manage job listings
  - View applications for posted jobs
  - Change application statuses

- **Job Seekers**:
  - Register & complete personal profile
  - Upload resume & apply for jobs
  - Track application status

### 🧩 Modules:
- **User Registration/Login** (with separate employer/jobseeker roles)
- **Job Posting & Management**
- **Job Applications**
- **Profile Completion**
- **Role-Based Navigation**
- **Responsive UI with Bootstrap 5**

---

## 🚀 Getting Started

### 🔑 Prerequisites

- Python 3.11+
- pip (Python package installer)
- virtualenv *(recommended)*

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/ishwaryasree2320/jobportal.git
cd jobportal

# Set up virtual environment
python -m venv venv
venv\Scripts\activate   # on Windows
# or
source venv/bin/activate  # on macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
