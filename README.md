# 🏥 MedQuizPro: Advanced Medical Education Platform

### An Interactive Learning Platform for Healthcare Professionals

Medical quiz and assessment platform designed specifically for healthcare professionals, 
featuring role-based learning paths, real-time analytics, and comprehensive progress tracking.

## 🚀 **Project Overview**
---
The app can be found at 🚀 **https://creativedigitalzambia.tech**
--

**MedQuizPro** is an interactive and comprehensive medical education platform designed to help healthcare professionals enhance their knowledge through specialized quizzes. The platform supports role-based learning paths, automated scoring, and progress tracking, ensuring a tailored educational experience for different medical disciplines.

---

## 🌟 Key Features

### For Healthcare Professionals
- **🔐 Role-Based Access**: Tailored content for different medical roles (doctors, nurses, pharmacists, etc.)
- **📊 Personalized Dashboard**: Track your progress, achievements, and performance metrics
- **⏱️ Timed Assessments**: Realistic exam conditions with configurable time limits
- **📱 Multi-Device Support**: Seamless experience across desktop and mobile devices
- **🏆 Achievement System**: Earn badges and track professional development

### For Administrators
- **👥 User Management**: Comprehensive tools for managing healthcare professionals
- **📝 Quiz Creation**: Rich question editor with support for images and explanations
- **📈 Analytics Dashboard**: Detailed insights into user performance and engagement
- **🔍 Content Review**: Moderation system for community-submitted questions
- **🔄 Session Management**: Advanced user session handling and security

## 🛠️ Technical Stack

### Backend
- **Framework**: Flask 3.1.0
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Authentication**: Flask-Login with advanced session management
- **Task Queue**: Redis + RQ for background processing
- **Email**: Custom Python SMTP email for notifications
- **Caching**: Flask-Caching with Redis

### Frontend
- **Template Engine**: Jinja2
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Form Handling**: Flask-WTF with CSRF protection

### Security
- **Authentication**: Multi-session support with device tracking
- **Password Security**: Bcrypt hashing
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Session Management**: Secure cookie handling
- **Input Validation**: WTForms validators

## 📋 Prerequisites

- Python 3.8+
- Redis Server
- PostgreSQL (production) or SQLite (development)
- Heroku (for deployment)

## 🛠️ **Installation Instructions** and 🚀 Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/medquizpro.git
   cd medquizpro
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory:

   ```bash
   SECRET_KEY='your_secret_key'
   SQLALCHEMY_DATABASE_URI='mysql://username:password@localhost/medquiz_db'
   ```

5. **Set Up the Database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the Application**

   ```bash
   flask run
   ```

7. **Access the App**

   Visit `http://127.0.0.1:5000` in your browser.

---

## 🏗️ Project Structure

```
medquizpro/
├── Procfile
├── README.md
├── MedQuizPro.db
├── LICENSE
├── worker.py
├── venv/
├── .gitignore
├── requirements.txt
├── .env
├── migrations/
├── logs/
├── tests/
│   ├── __init__.py
├── config.py
├── app/
│   ├── errors.py
│   ├── __init__.py
│   ├── models/
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── submission.py
│   │   ├── user.py
│   │   ├── study_group.py
│   │   ├── result.py
│   │   ├── question.py
│   │   ├── report.py
│   │   ├── quiz.py
│   ├── search.py
│   ├── templates/
│   │   ├── reports/
│   │   │   ├── report_form.html
│   │   ├── emails/
│   │   │   ├── base.html
│   │   │   ├── welcome.html
│   │   │   ├── achievement.html
│   │   │   ├── reset_password.html
│   │   │   ├── quiz_completion.html
│   │   │   ├── issue_report.html
│   │   │   ├── contact_form.html
│   │   ├── base.html
│   │   ├── quiz/
│   │   │   ├── analytics.html
│   │   │   ├── components/
│   │   │   ├── take_quiz.html
│   │   │   ├── result.html
│   │   │   ├── list.html
│   │   │   ├── modals/
│   │   ├── admin/
│   │   │   ├── reports/
│   │   │   │   ├── review.html
│   │   │   │   ├── list.html
│   │   │   ├── submissions/
│   │   │   │   ├── review.html
│   │   │   │   ├── review_single.html
│   │   │   ├── dashboard.html
│   │   │   ├── base.html
│   │   │   ├── quiz/
│   │   │   │   ├── create.html
│   │   │   │   ├── edit_questions.html
│   │   │   │   ├── edit.html
│   │   │   │   ├── manage.html
│   │   │   ├── users.html
│   │   │   ├── reports.html
│   │   ├── errors/
│   │   │   ├── 401.html
│   │   │   ├── 500.html
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   ├── 400.html
│   │   ├── main/
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   ├── index.html
│   │   ├── search/
│   │   │   ├── _pagination.html
│   │   │   ├── _results.html
│   │   │   ├── search.html
│   │   ├── submission/
│   │   │   ├── submit.html
│   │   │   ├── my_submissions.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── reset_password.html
│   │   │   ├── achievements.html
│   │   │   ├── register.html
│   │   │   ├── reset_password_request.html
│   │   │   ├── profile.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── email.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── quiz/
│   │   │   ├── __init__.py
│   │   │   ├── submission.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   ├── reports.py
│   │   ├── main/
│   │   │   ├── __init__.py
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   ├── uploads/
│   │   ├── js/
│   │   ├── images/
│   │   │   ├── avatars/
├── initialize-database.py
├── .idea/
├── instance/
├── run.py
```

## 🔧 Configuration

The application uses a hierarchical configuration system:

- `config.py`: Base configuration
- `.env`: Environment-specific settings
- Instance folder: Local overrides

Key configuration options:
- Database URLs
- Redis settings
- Mail server settings
- Security keys
- File upload limits

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Generate coverage report:
```bash
coverage run -m pytest
coverage report
```

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Create a pull request.


## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For support:
- 📧 Email: martinnyemba@gmail.com
- 📝 Issues: GitHub Issue Tracker

## 🙏 Acknowledgments

Special thanks to:
- ALX Software Engineering Program
- Medical professionals who provided content expertise
- Open source community contributors
- Early adopters and testers


## 🗓️ **Development Roadmap**

### **Week 1: Project Setup & Authentication**
- Project structure and database schema
- User authentication and role-based access

### **Week 2: Backend Development**
- Quiz management system
- Automated scoring and progress tracking

### **Week 3: Advanced Features & Deployment**
- Error handling and testing
- Final deployment and documentation

---

## 🔄 Latest Updates

- Added professional dashboard analytics
- Enhanced quiz submission system
- Improved session security
- Added support for community-contributed questions
- Implemented comprehensive achievement system

## 📬 **Contact**

- **Author**: Martin Nyemba  
- **Email**: [martinnyemba@gmail.com](mailto:martinnyemba@gmail.com)  
- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/martinchongochikaya)  
- **GitHub**: [GitHub Profile](https://github.com/martinnyemba)  

---

### 🩺 **Empowering Healthcare Professionals Through Education**
