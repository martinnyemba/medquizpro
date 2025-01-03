#!/usr/bin/env python3

from app import create_app, db
from werkzeug.security import generate_password_hash
from app.models import User, Quiz, Question, QuestionOption
from datetime import datetime


def create_users():
    """Create admin and regular users for each profession"""
    users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin3487',
            'profession': 'doctor',
            'is_admin': True,
            'institution': 'Central Medical Hospital',
            'experience_years': 10,
            'specialization': 'General Practice'
        }
    ]

    professions = ['doctor', 'nurse', 'pharmacist', 'clinical_officer', 'medical_licentiate']
    institutions = ['City General Hospital', 'Rural Health Center', 'University Medical Center',
                    'Community Clinic', 'Regional Hospital']

    for i, profession in enumerate(professions):
        users.append({
            'username': f'user_{profession}',
            'email': f'{profession}@example.com',
            'password': 'user3487',
            'profession': profession,
            'is_admin': False,
            'institution': institutions[i],
            'experience_years': 5 + i,
            'specialization': f'General {profession.replace("_", " ").title()}'
        })

    created_users = []
    for user_data in users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            profession=user_data['profession'],
            is_admin=user_data['is_admin'],
            institution=user_data['institution'],
            experience_years=user_data['experience_years'],
            specialization=user_data['specialization'],
            bio=f"Healthcare professional with {user_data['experience_years']} years of experience"
        )
        db.session.add(user)
        created_users.append(user)

    return created_users


def create_quiz_content():
    """Create comprehensive quiz content with updated option structure"""
    return {
        'anatomy': {
            'questions': [
                {
                    'content': 'Which of the following bones is part of the axial skeleton?',
                    'options': [
                        {'content': 'Skull', 'is_correct': True},
                        {'content': 'Humerus', 'is_correct': False},
                        {'content': 'Femur', 'is_correct': False},
                        {'content': 'Radius', 'is_correct': False}
                    ],
                    'explanation': 'The axial skeleton includes the skull, vertebral column, and rib cage.'
                },
                {
                    'content': 'What is the function of the mitral valve?',
                    'options': [
                        {'content': 'Controls blood flow between left atrium and left ventricle', 'is_correct': True},
                        {'content': 'Controls blood flow between right atrium and right ventricle', 'is_correct': False},
                        {'content': 'Controls blood flow from left ventricle to aorta', 'is_correct': False},
                        {'content': 'Controls blood flow from right ventricle to pulmonary artery', 'is_correct': False}
                    ],
                    'explanation': 'The mitral valve is located between the left atrium and left ventricle, controlling blood flow between these chambers.'
                },
                {
                    'content': 'Which cranial nerve controls taste in the anterior two-thirds of the tongue?',
                    'options': [
                        {'content': 'Facial nerve (CN VII)', 'is_correct': True},
                        {'content': 'Glossopharyngeal nerve (CN IX)', 'is_correct': False},
                        {'content': 'Vagus nerve (CN X)', 'is_correct': False},
                        {'content': 'Hypoglossal nerve (CN XII)', 'is_correct': False}
                    ],
                    'explanation': 'The facial nerve (CN VII) provides taste sensation to the anterior two-thirds of the tongue via the chorda tympani branch.'
                },
                {
                    'content': 'Which muscle is the primary flexor of the hip joint?',
                    'options': [
                        {'content': 'Iliopsoas', 'is_correct': True},
                        {'content': 'Gluteus maximus', 'is_correct': False},
                        {'content': 'Rectus femoris', 'is_correct': False},
                        {'content': 'Sartorius', 'is_correct': False}
                    ],
                    'explanation': 'The iliopsoas, composed of the iliacus and psoas major muscles, is the primary and most powerful hip flexor.'
                },
                {
                    'content': 'Which part of the nephron is responsible for countercurrent multiplication?',
                    'options': [
                        {'content': 'Loop of Henle', 'is_correct': True},
                        {'content': 'Proximal convoluted tubule', 'is_correct': False},
                        {'content': 'Distal convoluted tubule', 'is_correct': False},
                        {'content': 'Collecting duct', 'is_correct': False}
                    ],
                    'explanation': 'The loop of Henle creates and maintains the medullary concentration gradient through countercurrent multiplication.'
                }
            ]
        },
        'pharmacology': {
            'questions': [
                {
                    'content': 'Which antihypertensive medication class is contraindicated in bilateral renal artery stenosis?',
                    'options': [
                        {'content': 'ACE inhibitors', 'is_correct': True},
                        {'content': 'Calcium channel blockers', 'is_correct': False},
                        {'content': 'Beta blockers', 'is_correct': False},
                        {'content': 'Thiazide diuretics', 'is_correct': False}
                    ],
                    'explanation': 'ACE inhibitors are contraindicated in bilateral renal artery stenosis as they can cause acute kidney injury by reducing efferent arteriolar tone.'
                },
                {
                    'content': 'Which drug is the first-line treatment for acute status epilepticus?',
                    'options': [
                        {'content': 'Lorazepam', 'is_correct': True},
                        {'content': 'Phenytoin', 'is_correct': False},
                        {'content': 'Valproic acid', 'is_correct': False},
                        {'content': 'Carbamazepine', 'is_correct': False}
                    ],
                    'explanation': 'Lorazepam is the preferred first-line benzodiazepine for status epilepticus due to its rapid onset and longer duration of action.'
                },
                {
                    'content': 'What is the mechanism of action of metformin in treating type 2 diabetes?',
                    'options': [
                        {'content': 'Decreases hepatic glucose production and increases insulin sensitivity', 'is_correct': True},
                        {'content': 'Increases insulin secretion from pancreatic beta cells', 'is_correct': False},
                        {'content': 'Delays glucose absorption in the intestine', 'is_correct': False},
                        {'content': 'Increases glucose excretion in urine', 'is_correct': False}
                    ],
                    'explanation': 'Metformin primarily works by reducing hepatic glucose production and improving peripheral insulin sensitivity.'
                },
                {
                    'content': 'Which antibiotic class is most appropriate for treating atypical pneumonia?',
                    'options': [
                        {'content': 'Macrolides', 'is_correct': True},
                        {'content': 'Penicillins', 'is_correct': False},
                        {'content': 'Cephalosporins', 'is_correct': False},
                        {'content': 'Aminoglycosides', 'is_correct': False}
                    ],
                    'explanation': 'Macrolides are effective against atypical organisms like Mycoplasma pneumoniae and Chlamydophila pneumoniae.'
                }
            ]
        },
        'medicine': {
            'questions': [
                {
                    'content': 'What is the most appropriate initial management for acute STEMI?',
                    'options': [
                        {'content': 'Primary PCI within 90 minutes', 'is_correct': True},
                        {'content': 'Thrombolysis if PCI unavailable within 30 minutes', 'is_correct': False},
                        {'content': 'Conservative medical management', 'is_correct': False},
                        {'content': 'Immediate coronary artery bypass surgery', 'is_correct': False}
                    ],
                    'explanation': 'Primary PCI within 90 minutes is the gold standard treatment for STEMI if available at a capable facility.'
                },
                {
                    'content': 'Which finding is most specific for systemic lupus erythematosus?',
                    'options': [
                        {'content': 'Anti-dsDNA antibodies', 'is_correct': True},
                        {'content': 'ANA positivity', 'is_correct': False},
                        {'content': 'Arthralgia', 'is_correct': False},
                        {'content': 'Malar rash', 'is_correct': False}
                    ],
                    'explanation': 'Anti-dsDNA antibodies are highly specific for SLE and correlate with disease activity.'
                },
                {
                    'content': 'What is the most common cause of hospital-acquired pneumonia?',
                    'options': [
                        {'content': 'Staphylococcus aureus', 'is_correct': True},
                        {'content': 'Streptococcus pneumoniae', 'is_correct': False},
                        {'content': 'Klebsiella pneumoniae', 'is_correct': False},
                        {'content': 'Haemophilus influenzae', 'is_correct': False}
                    ],
                    'explanation': 'Staphylococcus aureus, including MRSA, is the most common cause of hospital-acquired pneumonia.'
                },
                {
                    'content': 'Which condition is most strongly associated with HLA-B27?',
                    'options': [
                        {'content': 'Ankylosing spondylitis', 'is_correct': True},
                        {'content': 'Rheumatoid arthritis', 'is_correct': False},
                        {'content': 'Systemic lupus erythematosus', 'is_correct': False},
                        {'content': 'Osteoarthritis', 'is_correct': False}
                    ],
                    'explanation': 'HLA-B27 is strongly associated with ankylosing spondylitis and other spondyloarthropathies.'
                }
            ]
        },
        'surgery': {
            'questions': [
                {
                    'content': 'What is the most appropriate initial management for acute cholecystitis?',
                    'options': [
                        {'content': 'Early laparoscopic cholecystectomy', 'is_correct': True},
                        {'content': 'Antibiotics alone', 'is_correct': False},
                        {'content': 'Percutaneous cholecystostomy', 'is_correct': False},
                        {'content': 'ERCP', 'is_correct': False}
                    ],
                    'explanation': 'Early laparoscopic cholecystectomy (within 72 hours) is the preferred treatment for acute cholecystitis in suitable candidates.'
                },
                {
                    'content': 'Which is the most appropriate fluid for initial resuscitation in hemorrhagic shock?',
                    'options': [
                        {'content': 'Balanced crystalloid solution', 'is_correct': True},
                        {'content': 'Normal saline', 'is_correct': False},
                        {'content': 'Albumin', 'is_correct': False},
                        {'content': 'Dextrose solution', 'is_correct': False}
                    ],
                    'explanation': 'Balanced crystalloid solutions are preferred for initial resuscitation as they cause less metabolic derangement.'
                },
                {
                    'content': 'What is the most common complication after splenectomy?',
                    'options': [
                        {'content': 'Left lower lobe atelectasis', 'is_correct': True},
                        {'content': 'Hemorrhage', 'is_correct': False},
                        {'content': 'Subphrenic abscess', 'is_correct': False},
                        {'content': 'Thrombocytosis', 'is_correct': False}
                    ],
                    'explanation': 'Left lower lobe atelectasis is the most common post-splenectomy complication due to decreased left diaphragm movement.'
                }
            ]
        },
        'pediatrics': {
            'questions': [
                {
                    'content': 'What is the most common presenting symptom of intussusception?',
                    'options': [
                        {'content': 'Intermittent severe abdominal pain', 'is_correct': True},
                        {'content': 'Bilious vomiting', 'is_correct': False},
                        {'content': 'Bloody stool', 'is_correct': False},
                        {'content': 'Fever', 'is_correct': False}
                    ],
                    'explanation': 'Intermittent severe abdominal pain is typically the first symptom of intussusception, often causing a child to draw their knees to their chest.'
                },
                {
                    'content': 'Which congenital heart defect is most commonly associated with Down syndrome?',
                    'options': [
                        {'content': 'Atrioventricular septal defect', 'is_correct': True},
                        {'content': 'Tetralogy of Fallot', 'is_correct': False},
                        {'content': 'Transposition of great arteries', 'is_correct': False},
                        {'content': 'Patent ductus arteriosus', 'is_correct': False}
                    ],
                    'explanation': 'Atrioventricular septal defect (AVSD) is the most common cardiac defect in Down syndrome.'
                },
                {
                    'content': 'What is the most appropriate initial treatment for febrile seizures?',
                    'options': [
                        {'content': 'Observation and fever control', 'is_correct': True},
                        {'content': 'Long-term anticonvulsants', 'is_correct': False},
                        {'content': 'Emergency CT scan', 'is_correct': False},
                        {'content': 'Lumbar puncture', 'is_correct': False}
                    ],
                    'explanation': 'Simple febrile seizures are benign and self-limiting, requiring only observation and fever control.'
                }
            ]
        },
        'obstetrics': {
            'questions': [
                {
                    'content': 'What is the most appropriate management for severe preeclampsia at 34 weeks gestation?',
                    'options': [
                        {'content': 'Delivery after antenatal corticosteroids', 'is_correct': True},
                        {'content': 'Expectant management with close monitoring', 'is_correct': False},
                        {'content': 'Immediate cesarean delivery', 'is_correct': False},
                        {'content': 'Antihypertensive therapy alone', 'is_correct': False}
                    ],
                    'explanation': 'Severe preeclampsia at 34 weeks warrants delivery after completing antenatal corticosteroids for fetal lung maturity.'
                },
                {
                    'content': 'Which medication is first-line for postpartum hemorrhage?',
                    'options': [
                        {'content': 'Oxytocin', 'is_correct': True},
                        {'content': 'Methylergonovine', 'is_correct': False},
                        {'content': 'Carboprost', 'is_correct': False},
                        {'content': 'Misoprostol', 'is_correct': False}
                    ],
                    'explanation': 'Oxytocin is the first-line uterotonic agent for prevention and treatment of postpartum hemorrhage.'
                },
                {
                    'content': 'What is the most common cause of third-trimester bleeding?',
                    'options': [
                        {'content': 'Placental abruption', 'is_correct': True},
                        {'content': 'Placenta previa', 'is_correct': False},
                        {'content': 'Vasa previa', 'is_correct': False},
                        {'content': 'Cervical ectropion', 'is_correct': False}
                    ],
                    'explanation': 'Placental abruption is the most common cause of third-trimester bleeding and can lead to significant maternal and fetal complications.'
                }
            ]
        },
        'emergency_medicine': {
            'questions': [
                {
                    'content': 'What is the first-line treatment for anaphylactic shock?',
                    'options': [
                        {'content': 'Intramuscular epinephrine', 'is_correct': True},
                        {'content': 'Intravenous antihistamines', 'is_correct': False},
                        {'content': 'Oral corticosteroids', 'is_correct': False},
                        {'content': 'Nebulized albuterol', 'is_correct': False}
                    ],
                    'explanation': 'Intramuscular epinephrine is the first-line treatment for anaphylaxis due to its rapid onset and effectiveness in treating multiple aspects of the reaction.'
                },
                {
                    'content': 'Which rhythm is most appropriate for immediate defibrillation?',
                    'options': [
                        {'content': 'Ventricular fibrillation', 'is_correct': True},
                        {'content': 'Pulseless electrical activity', 'is_correct': False},
                        {'content': 'Asystole', 'is_correct': False},
                        {'content': 'Complete heart block', 'is_correct': False}
                    ],
                    'explanation': 'Ventricular fibrillation is a shockable rhythm that requires immediate defibrillation as the first-line treatment.'
                },
                {
                    'content': 'What is the most appropriate initial fluid for severe diabetic ketoacidosis?',
                    'options': [
                        {'content': 'Normal saline', 'is_correct': True},
                        {'content': 'Lactated Ringers', 'is_correct': False},
                        {'content': 'D5W', 'is_correct': False},
                        {'content': 'Half-normal saline', 'is_correct': False}
                    ],
                    'explanation': 'Normal saline is the preferred initial fluid for DKA to correct volume depletion and provide sodium replacement.'
                }
            ]
        },
        'psychiatry': {
            'questions': [
                {
                    'content': 'Which antipsychotic medication has the lowest risk of extrapyramidal symptoms?',
                    'options': [
                        {'content': 'Quetiapine', 'is_correct': True},
                        {'content': 'Haloperidol', 'is_correct': False},
                        {'content': 'Risperidone', 'is_correct': False},
                        {'content': 'Chlorpromazine', 'is_correct': False}
                    ],
                    'explanation': 'Quetiapine has the lowest risk of extrapyramidal symptoms among antipsychotics due to its low D2 receptor affinity.'
                },
                {
                    'content': 'What is the first-line treatment for major depressive disorder?',
                    'options': [
                        {'content': 'SSRIs', 'is_correct': True},
                        {'content': 'TCAs', 'is_correct': False},
                        {'content': 'MAOIs', 'is_correct': False},
                        {'content': 'Benzodiazepines', 'is_correct': False}
                    ],
                    'explanation': 'SSRIs are the first-line treatment for major depression due to their favorable side effect profile and efficacy.'
                }
            ]
        },
        'radiology': {
            'questions': [
                {
                    'content': 'Which imaging modality is most appropriate for diagnosing acute pulmonary embolism?',
                    'options': [
                        {'content': 'CT pulmonary angiogram', 'is_correct': True},
                        {'content': 'Chest X-ray', 'is_correct': False},
                        {'content': 'VQ scan', 'is_correct': False},
                        {'content': 'MRI', 'is_correct': False}
                    ],
                    'explanation': 'CT pulmonary angiogram is the gold standard for diagnosing pulmonary embolism due to its high sensitivity and specificity.'
                },
                {
                    'content': 'What is the best initial imaging study for suspected acute appendicitis?',
                    'options': [
                        {'content': 'Ultrasound in pediatric/pregnant patients, CT for others', 'is_correct': True},
                        {'content': 'MRI for all patients', 'is_correct': False},
                        {'content': 'Plain abdominal radiograph', 'is_correct': False},
                        {'content': 'Nuclear medicine scan', 'is_correct': False}
                    ],
                    'explanation': 'Ultrasound is preferred in children and pregnant patients to avoid radiation, while CT is more sensitive and specific in other adults.'
                }
            ]
        },
        'pathology': {
            'questions': [
                {
                    'content': 'Which immunohistochemical stain is most specific for melanoma?',
                    'options': [
                        {'content': 'S100 and HMB-45', 'is_correct': True},
                        {'content': 'Cytokeratin', 'is_correct': False},
                        {'content': 'CD20', 'is_correct': False},
                        {'content': 'TTF-1', 'is_correct': False}
                    ],
                    'explanation': 'S100 and HMB-45 are highly specific markers for melanoma and are used in combination for diagnosis.'
                },
                {
                    'content': 'What is the characteristic histological finding in celiac disease?',
                    'options': [
                        {'content': 'Villous atrophy with crypt hyperplasia', 'is_correct': True},
                        {'content': 'Granulomas', 'is_correct': False},
                        {'content': 'Viral inclusions', 'is_correct': False},
                        {'content': 'Dysplasia', 'is_correct': False}
                    ],
                    'explanation': 'Villous atrophy with crypt hyperplasia is the hallmark histological finding in celiac disease.'
                }
            ]
        },
        'preventive_medicine': {
            'questions': [
                {
                    'content': 'At what age should colorectal cancer screening begin for average-risk individuals?',
                    'options': [
                        {'content': '45 years', 'is_correct': True},
                        {'content': '50 years', 'is_correct': False},
                        {'content': '40 years', 'is_correct': False},
                        {'content': '55 years', 'is_correct': False}
                    ],
                    'explanation': 'Current guidelines recommend starting colorectal cancer screening at age 45 for average-risk individuals.'
                },
                {
                    'content': 'Which vaccine is contraindicated in immunocompromised patients?',
                    'options': [
                        {'content': 'Live attenuated influenza vaccine', 'is_correct': True},
                        {'content': 'Inactivated influenza vaccine', 'is_correct': False},
                        {'content': 'Pneumococcal vaccine', 'is_correct': False},
                        {'content': 'Tdap vaccine', 'is_correct': False}
                    ],
                    'explanation': 'Live attenuated vaccines are contraindicated in immunocompromised patients due to the risk of vaccine-strain infection.'
                },
                {
                    'content': 'What is the recommended first-line intervention for primary prevention of cardiovascular disease?',
                    'options': [
                        {'content': 'Lifestyle modifications', 'is_correct': True},
                        {'content': 'Aspirin therapy', 'is_correct': False},
                        {'content': 'Statin therapy', 'is_correct': False},
                        {'content': 'Beta blockers', 'is_correct': False}
                    ],
                    'explanation': 'Lifestyle modifications including diet, exercise, and smoking cessation are the cornerstone of primary cardiovascular disease prevention.'
                }
            ]
        }
    }


def create_quizzes(admin_user):
    """Create quizzes with updated question and option structure"""
    courses = [
        'anatomy', 'pharmacology', 'medicine', 'surgery', 'pediatrics', 'obstetrics',
        'emergency_medicine', 'psychiatry', 'radiology', 'pathology', 'preventive_medicine'
    ]

    professions = ['doctor', 'nurse', 'pharmacist', 'clinical_officer', 'medical_licentiate']
    quiz_content = create_quiz_content()

    for profession in professions:
        for course in courses:
            # Create quiz with profession-specific title and description
            quiz = Quiz(
                title=f'{course.replace("_", " ").title()} for {profession.replace("_", " ").title()}',
                course=course,
                profession=profession,
                time_limit=30,
                description=f'Comprehensive {course.replace("_", " ")} assessment for {profession.replace("_", " ")} professionals',
                created_by_id=admin_user.id,
                difficulty_level='intermediate',
                passing_score=70.0,
                instructions="""
                    Please read each question carefully and select the best answer.
                    - Each question has one correct answer
                    - Time limit is 30 minutes
                    - A score of 70% or higher is required to pass
                    - Complete all questions to submit the quiz
                """,
                tags=['core_curriculum', course, profession],
                prerequisites={'minimum_qualification': profession},
                is_published=True,
                requires_approval=False,
                approved_at=datetime.utcnow(),
                approved_by_id=admin_user.id
            )
            db.session.add(quiz)
            db.session.flush()

            # Get questions for this course
            questions = quiz_content.get(course, {}).get('questions', [])

            # Create questions and options
            for q_data in questions:
                # First, create all options and find the correct one
                options = []
                correct_option_id = None

                # Create all options first
                for opt_data in q_data['options']:
                    option = QuestionOption(
                        content=opt_data['content'],
                        is_correct=opt_data['is_correct']
                    )
                    # Don't add to session yet as we need the question_id
                    options.append((option, opt_data['is_correct']))

                # Now create the question with the correct_answer set to a temporary value
                question = Question(
                    quiz_id=quiz.id,
                    content=q_data['content'],
                    explanation=q_data.get('explanation', ''),
                    question_type='multiple_choice',
                    difficulty_level='intermediate',
                    points=1,
                    created_by_id=admin_user.id,
                    correct_answer=1  # Temporary value
                )
                db.session.add(question)
                db.session.flush()  # Get the question ID

                # Now add the options with the question_id and find the correct one
                for option, is_correct in options:
                    option.question_id = question.id
                    db.session.add(option)
                    db.session.flush()
                    if is_correct:
                        correct_option_id = option.id

                # Update the question with the correct answer ID
                question.correct_answer = correct_option_id
                db.session.add(question)
                db.session.flush()

    db.session.commit()

def init_db():
    """Initialize the database with updated structure"""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # Create users
        users = create_users()
        admin_user = next(user for user in users if user.is_admin)

        # Create quizzes with questions and options
        create_quizzes(admin_user)

        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")


if __name__ == '__main__':
    init_db()