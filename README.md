# 🩺 **MedQuizPro: Medical Education Reimagined**

### An Interactive Learning Platform for Healthcare Professionals

---

## 🚀 **Project Overview**

**MedQuizPro** is an interactive and comprehensive medical education platform designed to help healthcare professionals enhance their knowledge through specialized quizzes. The platform supports role-based learning paths, automated scoring, and progress tracking, ensuring a tailored educational experience for different medical disciplines.

---

## 🌟 **Core Features**

- **🔒 Role-Based Authentication**: Secure login for nurses, doctors, pharmacists, clinical officers, and medical licentiates.
- **📝 Course-Specific Quizzes**: Organized by profession and discipline (e.g., anatomy, pharmacology, medicine).
- **⏱️ Time-Limited Assessments**: Quizzes with configurable time limits to simulate real exam conditions.
- **📊 Progress Tracking**: Monitor quiz results and track professional development.
- **🗂️ Question Bank Management**: Add and manage quiz questions easily.
- **👨‍⚕️ Professional Dashboards**: Customized dashboards for different medical roles.
- **🛠️ Error Handling**: Comprehensive error management for a seamless user experience.

---

## 💻 **Technology Stack**

### **Backend**
- **Flask** (Python)
- **SQLAlchemy ORM**
- **MySQL** Database

### **Frontend**
- **HTML5**
- **CSS3**
- **JavaScript**

### **Security**
- **Bcrypt** for Password Encryption
- **Flask-Login** for Authentication
- **Secure Session Management**

---

## 🛠️ **Installation Instructions**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/medquest.git
   cd medquest
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

## 📂 **Project Structure**

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
│   │   │   ├── components/
│   │   │   │   ├── cards.css
│   │   │   │   ├── forms.css
│   │   │   │   ├── buttons.css
│   │   │   ├── style.css
│   │   ├── uploads/
│   │   ├── js/
│   │   │   ├── components/
│   │   │   │   ├── quiz.js
│   │   │   │   ├── timer.js
│   │   │   │   ├── validation.js
│   │   │   ├── main.js
│   │   ├── images/
│   │   │   ├── avatars/
├── initialize-database.py
├── .idea/
├── instance/
├── run.py
├── init_db.py


```

---

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

## 🧪 **Testing**

To run tests:

```bash
pytest
```

---

## 🔍 **Future Enhancements**

- 📱 **Mobile App Development**
- 🤖 **AI-Powered Learning Recommendations**
- 🌐 **Integration with Medical Institutions**
- 🧑‍🤝‍🧑 **Community Learning Features**

---

## 🤝 **Contributing**

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Create a pull request.

---

## 📜 **License**

This project is licensed under the **MIT License**.

---

## 📬 **Contact**

- **Author**: Martin Nyemba  
- **Email**: [your.email@example.com](mailto:martinnyemba@gmail.com)  
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/martinchongochikaya)  
- **GitHub**: [Your GitHub Profile](https://github.com/martinnyemba)  

---

### 🩺 **Empowering Healthcare Professionals Through Education**
