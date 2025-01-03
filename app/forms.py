from flask_wtf import FlaskForm
from werkzeug.datastructures import FileStorage
from wtforms import (StringField, PasswordField, BooleanField, SelectField,
                     TextAreaField, IntegerField, FileField, SelectMultipleField,
                     RadioField, DecimalField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from app.models import User
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('pharmacist', 'Pharmacist'),
        ('clinical_officer', 'Clinical Officer'),
        ('medical_licentiate', 'Medical Licentiate')
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
        ('surgery', 'Surgery'),
        ('pediatrics', 'Pediatrics'),
        ('obstetrics', 'Obstetrics & Gynecology'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('pathology', 'Pathology'),
        ('preventive_medicine', 'Preventive Medicine')
    ], validators=[DataRequired(message="Please select a Course Type")]
                         )
    profession = SelectField('Target Profession', choices=[
        ('all', 'All Professions'),
        ('doctor', 'Doctors Only'),
        ('nurse', 'Nurses Only'),
        ('pharmacist', 'Pharmacists Only'),
        ('clinical_officer', 'Clinical Officers Only'),
        ('medical_licentiate', 'Medical Licentiates Only')
    ])
    difficulty_level = SelectField('Difficulty Level', choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    passing_score = IntegerField('Passing Score (%)',
                                 validators=[DataRequired(), NumberRange(min=0, max=100)],
                                 default=70)
    time_limit = IntegerField('Time Limit (minutes)',
                              validators=[DataRequired(), NumberRange(min=5, max=180)])
    max_attempts = IntegerField('Maximum Attempts',
                                validators=[DataRequired(), NumberRange(min=1, max=10)],
                                default=3)
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

        if len(set(options)) != len(options):
            raise ValidationError('All options must be unique')


class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password', message='Passwords must match')])
    profession = SelectField('Profession', choices=[
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('pharmacist', 'Pharmacist'),
        ('clinical_officer', 'Clinical Officer'),
        ('medical_licentiate', 'Medical Licentiate')
    ])
    specialization = StringField('Specialization')
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=50)])
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
            ('surgery', 'Surgery'),
            ('pediatrics', 'Pediatrics'),
            ('obstetrics', 'Obstetrics & Gynecology'),
            ('emergency_medicine', 'Emergency Medicine'),
            ('psychiatry', 'Psychiatry'),
            ('radiology', 'Radiology'),
            ('pathology', 'Pathology'),
            ('preventive_medicine', 'Preventive Medicine')
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
