from flask_wtf import FlaskForm
from werkzeug.datastructures import FileStorage
from wtforms import (StringField, PasswordField, BooleanField, SelectField,
                     TextAreaField, IntegerField, FileField, SelectMultipleField,
                     RadioField, DecimalField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, \
    NumberRange, Regexp
from app.models import User
from flask_wtf.file import FileAllowed
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={
            "placeholder": "Enter your email",
            "autocomplete": "email",
            "spellcheck": "false",
            "autocapitalize": "none",
            "inputmode": "email"
        }
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters long")
        ],
        render_kw={
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        }
    )

    remember_me = BooleanField(
        'Keep me logged in',
        description="Warning: Only select this option on your personal devices"
    )


class RegistrationForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired()]
    )
    lastname = StringField(
        label='Last Name',
        validators=[DataRequired()]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4, max=25),
            Regexp(r'^[\w.]+$', message="Username can only contain letters, numbers, and dots.")
        ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Medical Doctor'),
        ('medical_licentiate', 'Medical Licentiate'),
        ('clinical_officer', 'Clinical Officer'),
        ('dentist', 'Dentist'),
        ('pharmacist', 'Pharmacist'),
        ('laboratory_technologist', 'Laboratory Technologist/Technician'),
        ('nurse', 'Registered Nurse (General Nurse)'),
        ('midwife', 'Midwife'),
        ('physiotherapist', 'Physiotherapist'),
        ('radiographer', 'Radiographer (Diagnostic and Therapeutic)'),
        ('nutritionist', 'Nutritionist/Dietitian'),
        ('biomedical_scientist', 'Biomedical Scientist'),
        ('public_health_specialist', 'Public Health Specialist'),
        ('paramedic', 'Paramedic/Emergency Medical'),
        ('optometrist', 'Optometrist/Ophthalmic Technologist'),
        ('anaesthetist', 'Anaesthetist'),
        ('anesthetic_technologist', 'Anesthetic Technologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('environmental_technologist', 'Environmental Health Technologist')
    ])

    specialization = StringField('Specialization', validators=[Optional()])
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
    institution = StringField('Institution/Hospital', validators=[Optional()])


class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    course = SelectField('Course', choices=[
        ('anatomy', 'Anatomy'),
        ('pharmacology', 'Pharmacology'),
        ('medicine', 'Medicine'),
        ('microbiology', 'Microbiology'),
        ('surgery', 'Surgery'),
        ('pediatrics', 'Pediatrics'),
        ('obstetrics', 'Obstetrics & Gynecology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('hiv_aids_medicine', 'HIV/AIDS Medicine'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('neonatology', 'Neonatology'),
        ('pathology', 'Pathology'),
        ('preventive_medicine', 'Preventive Medicine'),
        ('leadership_and_management', 'Leadership & Management')
    ], validators=[DataRequired(message="Please select a Course Type")]
                         )
    profession = SelectField('Target Profession', choices=[
        ('all', 'All Professions'),
        ('doctor', 'Medical Doctor'),
        ('medical_licentiate', 'Medical Licentiate'),
        ('clinical_officer', 'Clinical Officer'),
        ('dentist', 'Dentist'),
        ('pharmacist', 'Pharmacist'),
        ('laboratory_technologist', 'Laboratory Technologist/Technician'),
        ('nurse', 'Registered Nurse (General Nurse)'),
        ('midwife', 'Midwife'),
        ('physiotherapist', 'Physiotherapist'),
        ('radiographer', 'Radiographer (Diagnostic and Therapeutic)'),
        ('nutritionist', 'Nutritionist/Dietitian'),
        ('biomedical_scientist', 'Biomedical Scientist'),
        ('public_health_specialist', 'Public Health Specialist'),
        ('paramedic', 'Paramedic/Emergency Medical'),
        ('optometrist', 'Optometrist/Ophthalmic Technologist'),
        ('anaesthetist', 'Anaesthetist'),
        ('anesthetic_technologist', 'Anesthetic Technologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('environmental_technologist', 'Environmental Health Technologist')
    ])
    difficulty_level = SelectField('Difficulty Level', choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    passing_score = IntegerField('Passing Score (%)',
                                 validators=[DataRequired(), NumberRange(min=0, max=100)],
                                 default=60)
    time_limit = IntegerField('Time Limit (minutes)',
                              validators=[DataRequired(), NumberRange(min=5, max=180)])
    max_attempts = IntegerField('Maximum Attempts',
                                validators=[DataRequired(), NumberRange(min=1, max=10)],
                                default=5)
    tags = StringField('Tags (comma separated)', validators=[Optional()])
    instructions = TextAreaField('Instructions', validators=[Optional()])


class QuestionForm(FlaskForm):
    """Enhanced form for creating and editing questions"""
    content = TextAreaField(
        'Question Content',
        validators=[
            DataRequired(message="Question content is required"),
            Length(min=10, max=2000,
                   message="Question content must be between 10 and 2000 characters")
        ],
        render_kw={"placeholder": "Enter your question here...", "rows": 3}
    )

    question_type = SelectField(
        'Question Type',
        choices=[
            ('multiple_choice', 'Multiple Choice'),
            ('true_false', 'True/False')
        ],
        default='multiple_choice',
        validators=[DataRequired(message="Please select a question type")]
    )

    difficulty_level = SelectField(
        'Difficulty Level',
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='intermediate',
        validators=[DataRequired(message="Please select a difficulty level")]
    )

    points = IntegerField(
        'Points',
        validators=[
            DataRequired(message="Points value is required"),
            NumberRange(min=1, max=100, message="Points must be between 1 and 100")
        ],
        default=1,
        render_kw={"placeholder": "Points (1-100)"}
    )

    # Option fields with enhanced validation
    option1 = TextAreaField(
        'Option 1',
        validators=[
            DataRequired(message="Option 1 is required"),
            Length(min=1, max=500,
                   message="Option must be between 1 and 500 characters")
        ],
        render_kw={"placeholder": "Enter first option..."}
    )

    option2 = TextAreaField(
        'Option 2',
        validators=[
            DataRequired(message="Option 2 is required"),
            Length(min=1, max=500,
                   message="Option must be between 1 and 500 characters")
        ],
        render_kw={"placeholder": "Enter second option..."}
    )

    option3 = TextAreaField(
        'Option 3',
        validators=[
            DataRequired(message="Option 3 is required"),
            Length(min=1, max=500,
                   message="Option must be between 1 and 500 characters")
        ],
        render_kw={"placeholder": "Enter third option..."}
    )

    option4 = TextAreaField(
        'Option 4',
        validators=[
            DataRequired(message="Option 4 is required"),
            Length(min=1, max=500,
                   message="Option must be between 1 and 500 characters")
        ],
        render_kw={"placeholder": "Enter fourth option..."}
    )

    correct_answer = RadioField(
        'Correct Answer',
        choices=[
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
            ('4', 'Option 4')
        ],
        validators=[DataRequired(message="Please select the correct answer")]
    )

    explanation = TextAreaField(
        'Explanation',
        validators=[
            Optional(),
            Length(max=2000,
                   message="Explanation cannot exceed 2000 characters")
        ],
        render_kw={
            "placeholder": "Explain why the correct answer is right...",
            "rows": 3
        }
    )

    image = FileField(
        'Question Image (Optional)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'png', 'jpeg', 'gif'],
                        'Only image files (jpg, png, jpeg, gif) are allowed!')
        ]
    )

    def validate_image(self, field):
        """Validate image file size and type"""
        if field.data:
            if not isinstance(field.data, FileStorage):
                return

            # Check file size (limit to 5MB)
            max_size = 5 * 1024 * 1024
            field.data.seek(0, 2)
            size = field.data.tell()
            field.data.seek(0)

            if size > max_size:
                raise ValidationError('File size must be less than 5MB')

    def validate_question_type(self, field):
        """Handle validation for different question types"""
        if field.data == 'true_false':
            # For true/false questions, modify validators for options 3 and 4
            self.option3.validators = [Optional()]
            self.option4.validators = [Optional()]

            # Set default values for unused options
            if not self.option3.data:
                self.option3.data = ''
            if not self.option4.data:
                self.option4.data = ''

            # Update correct answer choices for true/false
            self.correct_answer.choices = [
                ('1', 'True'),
                ('2', 'False')
            ]

    def validate_correct_answer(self, field):
        """Ensure correct answer selection is valid for question type"""
        if self.question_type.data == 'true_false' and int(field.data) > 2:
            raise ValidationError('Invalid correct answer selection for true/false question')

    def validate_options(self):
        """Custom validation to ensure options are unique"""
        options = [
            self.option1.data,
            self.option2.data,
            self.option3.data,
            self.option4.data
        ]

        # Filter out empty options for true/false questions
        options = [opt for opt in options if opt]

        # Instead of raising ValidationError, return False
        if len(set(options)) != len(options):
            self.option1.errors.append('All options must be unique')
            return False
        return True

    def validate(self):
        """Override validate method to include options validation"""
        if not super().validate():
            return False
        if not self.validate_options():
            return False
        return True


class ProfileForm(FlaskForm):
    firstname = StringField(
        label='First Name', validators=[DataRequired()]
    )
    lastname = StringField(
        label='Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password', message='Passwords must match')])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Medical Doctor'),
        ('medical_licentiate', 'Medical Licentiate'),
        ('clinical_officer', 'Clinical Officer'),
        ('dentist', 'Dentist'),
        ('pharmacist', 'Pharmacist'),
        ('laboratory_technologist', 'Laboratory Technologist/Technician'),
        ('nurse', 'Registered Nurse (General Nurse)'),
        ('midwife', 'Midwife'),
        ('physiotherapist', 'Physiotherapist'),
        ('radiographer', 'Radiographer (Diagnostic and Therapeutic)'),
        ('nutritionist', 'Nutritionist/Dietitian'),
        ('biomedical_scientist', 'Biomedical Scientist'),
        ('public_health_specialist', 'Public Health Specialist'),
        ('paramedic', 'Paramedic/Emergency Medical'),
        ('optometrist', 'Optometrist/Ophthalmic Technologist'),
        ('anaesthetist', 'Anaesthetist'),
        ('anesthetic_technologist', 'Anesthetic Technologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('environmental_technologist', 'Environmental Health Technologist')
    ])
    specialization = StringField('Specialization')
    experience_years = IntegerField('Years of Experience',
                                    validators=[
                                        Optional(),
                                        NumberRange(min=0, max=50, message='Experience years must be between 0 and 50')
                                    ])

    def validate_experience_years(self, field):
        """Additional validation for experience years"""
        if field.data is not None:
            if not isinstance(field.data, int) or field.data < 0 or field.data > 50:
                raise ValidationError('Experience years must be between 0 and 50')

    institution = StringField('Institution/Hospital')
    bio = TextAreaField('About Me')
    profile_image = FileField('Profile Picture',
                              validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    filter_course = SelectField('Course', choices=[('', 'All Courses')], default='')
    filter_profession = SelectField('Profession', choices=[('', 'All Professions')], default='')
    filter_difficulty = SelectField('Difficulty', choices=[
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='')


class FeedbackForm(FlaskForm):
    rating = RadioField('Rating', choices=[
        ('5', '⭐⭐⭐⭐⭐ Excellent'),
        ('4', '⭐⭐⭐⭐ Good'),
        ('3', '⭐⭐⭐ Average'),
        ('2', '⭐⭐ Below Average'),
        ('1', '⭐ Poor')
    ], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('content', 'Content Quality'),
        ('difficulty', 'Difficulty Level'),
        ('interface', 'User Interface'),
        ('technical', 'Technical Issues'),
        ('other', 'Other')
    ])


class ReportIssueForm(FlaskForm):
    issue_type = SelectField('Issue Type', choices=[
        ('bug', 'Bug Report'),
        ('content', 'Content Issue'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other')
    ])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    screenshot = FileField('Screenshot (Optional)',
                           validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])


class QuizFilterForm(FlaskForm):
    course = SelectField('Course', choices=[('', 'All Courses')])
    profession = SelectField('Profession', choices=[('', 'All Professions')])
    difficulty = SelectField('Difficulty', choices=[
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    sort_by = SelectField('Sort By', choices=[
        ('newest', 'Newest First'),
        ('popularity', 'Most Popular'),
        ('difficulty_asc', 'Easiest First'),
        ('difficulty_desc', 'Hardest First')
    ])


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])


class QuestionSubmissionForm(FlaskForm):
    """Form for submitting new questions for review"""
    course = SelectField(
        'Course',
        choices=[
            ('anatomy', 'Anatomy'),
            ('pharmacology', 'Pharmacology'),
            ('medicine', 'Medicine'),
            ('microbiology', 'Microbiology'),
            ('surgery', 'Surgery'),
            ('pediatrics', 'Pediatrics'),
            ('obstetrics', 'Obstetrics & Gynecology'),
            ('emergency_medicine', 'Emergency Medicine'),
            ('hiv_aids_medicine', 'HIV/AIDS Medicine'),
            ('psychiatry', 'Psychiatry'),
            ('radiology', 'Radiology'),
            ('neonatology', 'Neonatology'),
            ('pathology', 'Pathology'),
            ('preventive_medicine', 'Preventive Medicine'),
            ('leadership_and_management', 'Leadership & Management')
        ],
        validators=[DataRequired(message="Please select a course")]
    )

    content = TextAreaField(
        'Question Content',
        validators=[
            DataRequired(message="Question content is required"),
            Length(min=10, max=2000,
                   message="Question content must be between 10 and 2000 characters")
        ],
        render_kw={"placeholder": "Enter your question here...", "rows": 3}
    )

    difficulty_level = SelectField(
        'Difficulty Level',
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='intermediate',
        validators=[DataRequired(message="Please select a difficulty level")]
    )

    option1 = TextAreaField(
        'Option 1',
        validators=[
            DataRequired(message="Option 1 is required"),
            Length(max=500, message="Option must not exceed 500 characters")
        ],
        render_kw={"placeholder": "Enter first option..."}
    )

    option2 = TextAreaField(
        'Option 2',
        validators=[
            DataRequired(message="Option 2 is required"),
            Length(max=500, message="Option must not exceed 500 characters")
        ],
        render_kw={"placeholder": "Enter second option..."}
    )

    option3 = TextAreaField(
        'Option 3',
        validators=[
            DataRequired(message="Option 3 is required"),
            Length(max=500, message="Option must not exceed 500 characters")
        ],
        render_kw={"placeholder": "Enter third option..."}
    )

    option4 = TextAreaField(
        'Option 4',
        validators=[
            DataRequired(message="Option 4 is required"),
            Length(max=500, message="Option must not exceed 500 characters")
        ],
        render_kw={"placeholder": "Enter fourth option..."}
    )

    correct_answer = RadioField(
        'Correct Answer',
        choices=[
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
            ('4', 'Option 4')
        ],
        validators=[DataRequired(message="Please select the correct answer")]
    )

    explanation = TextAreaField(
        'Explanation',
        validators=[
            DataRequired(message="Please provide an explanation for the correct answer"),
            Length(max=2000, message="Explanation cannot exceed 2000 characters")
        ],
        render_kw={
            "placeholder": "Explain why the correct answer is right...",
            "rows": 2
        }
    )

    reference = StringField(
        'Reference/Source',
        validators=[
            Optional(),
            Length(max=500, message="Reference cannot exceed 500 characters")
        ],
        render_kw={"placeholder": "Optional: Cite your source or reference material"}
    )

    def validate_options(self):
        """Custom validation to ensure options are unique"""
        options = [
            self.option1.data,
            self.option2.data,
            self.option3.data,
            self.option4.data
        ]

        if len(set(options)) != len(options):
            return False
        return True


class ReviewSubmissionForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('approved', 'Approve'),
        ('rejected', 'Reject')
    ], validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[Optional()])


class ReportForm:
    pass


class ReportReviewForm:
    pass


# Admin user management forms
class AdminUserCreateForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired()]
    )
    lastname = StringField(
        label='Last Name',
        validators=[DataRequired()]
    )
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25),
        Regexp(r'^[\w.]+$', message="Username can only contain letters, numbers, and dots.")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
               message="Password must contain at least one letter, one number, and one special character.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Medical Doctor'),
        ('medical_licentiate', 'Medical Licentiate'),
        ('clinical_officer', 'Clinical Officer'),
        ('dentist', 'Dentist'),
        ('pharmacist', 'Pharmacist'),
        ('laboratory_technologist', 'Laboratory Technologist/Technician'),
        ('nurse', 'Registered Nurse (General Nurse)'),
        ('midwife', 'Midwife'),
        ('physiotherapist', 'Physiotherapist'),
        ('radiographer', 'Radiographer (Diagnostic and Therapeutic)'),
        ('nutritionist', 'Nutritionist/Dietitian'),
        ('biomedical_scientist', 'Biomedical Scientist'),
        ('public_health_specialist', 'Public Health Specialist'),
        ('paramedic', 'Paramedic/Emergency Medical'),
        ('optometrist', 'Optometrist/Ophthalmic Technologist'),
        ('anaesthetist', 'Anaesthetist'),
        ('anesthetic_technologist', 'Anesthetic Technologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('environmental_technologist', 'Environmental Health Technologist')
    ])
    specialization = StringField('Specialization')
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
    institution = StringField('Institution/Hospital')
    is_admin = BooleanField('Administrator Access')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class AdminUserEditForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired(), Length(min=2, max=64)])
    lastname = StringField(
        label='Last Name',
        validators=[DataRequired(), Length(min=2, max=64)])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25),
        Regexp(r'^[\w.]+$', message="Username can only contain letters, numbers, and dots.")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$',
               message="Password must contain at least one letter, one number, and one special character.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        EqualTo('new_password', message='Passwords must match.')
    ])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Medical Doctor'),
        ('medical_licentiate', 'Medical Licentiate'),
        ('clinical_officer', 'Clinical Officer'),
        ('dentist', 'Dentist'),
        ('pharmacist', 'Pharmacist'),
        ('laboratory_technologist', 'Laboratory Technologist/Technician'),
        ('nurse', 'Registered Nurse (General Nurse)'),
        ('midwife', 'Midwife'),
        ('physiotherapist', 'Physiotherapist'),
        ('radiographer', 'Radiographer (Diagnostic and Therapeutic)'),
        ('nutritionist', 'Nutritionist/Dietitian'),
        ('biomedical_scientist', 'Biomedical Scientist'),
        ('public_health_specialist', 'Public Health Specialist'),
        ('paramedic', 'Paramedic/Emergency Medical'),
        ('optometrist', 'Optometrist/Ophthalmic Technologist'),
        ('anaesthetist', 'Anaesthetist'),
        ('anesthetic_technologist', 'Anesthetic Technologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('environmental_technologist', 'Environmental Health Technologist')
    ])
    specialization = StringField('Specialization')
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
    institution = StringField('Institution/Hospital')
    is_admin = BooleanField('Administrator Access')
    is_active = BooleanField('Active Account')

    def __init__(self, original_username, *args, **kwargs):
        super(AdminUserEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, field):
        if field.data != self.original_username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError('Username already exists.')
