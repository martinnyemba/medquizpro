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
                        {'content': 'Humerus', 'is_correct': False},
                        {'content': 'Femur', 'is_correct': False},
                        {'content': 'Skull', 'is_correct': True},
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
                    'explanation': 'The mitral valve is located between the left atrium and left ventricle, '
                                   'controlling blood flow between these chambers.'
                },
                {
                    'content': 'Which cranial nerve controls taste in the anterior two-thirds of the tongue?',
                    'options': [
                        {'content': 'Glossopharyngeal nerve (CN IX)', 'is_correct': False},
                        {'content': 'Facial nerve (CN VII)', 'is_correct': True},
                        {'content': 'Vagus nerve (CN X)', 'is_correct': False},
                        {'content': 'Hypoglossal nerve (CN XII)', 'is_correct': False}
                    ],
                    'explanation': 'The facial nerve (CN VII) provides taste sensation to the anterior two-thirds of '
                                   'the tongue via the chorda tympani branch.'
                },
                {
                    "content": "What is the primary function of the cerebellum in the human brain?",
                    "options": [
                        {"content": "Coordination of voluntary movements", "is_correct": True},
                        {"content": "Regulation of emotions", "is_correct": False},
                        {"content": "Control of heartbeat", "is_correct": False},
                        {"content": "Processing of visual information", "is_correct": False}
                    ],
                    "explanation": "The cerebellum plays a crucial role in coordinating voluntary movements, balance, and posture."
                },
                {
                    "content": "Which bone is known as the longest bone in the human body?",
                    "options": [
                        {"content": "Tibia", "is_correct": False},
                        {"content": "Humerus", "is_correct": False},
                        {"content": "Femur", "is_correct": True},
                        {"content": "Radius", "is_correct": False}
                    ],
                    "explanation": "The femur, or thigh bone, is the longest and strongest bone in the human body."
                },
                {
                    "content": "What structure connects muscles to bones?",
                    "options": [
                        {"content": "Tendons", "is_correct": True},
                        {"content": "Ligaments", "is_correct": False},
                        {"content": "Cartilage", "is_correct": False},
                        {"content": "Fascia", "is_correct": False}
                    ],
                    "explanation": "Tendons are connective tissues that attach muscles to bones, allowing movement."
                },
                {
                    "content": "What is the name of the outermost layer of the skin?",
                    "options": [

                        {"content": "Dermis", "is_correct": False},
                        {"content": "Hypodermis", "is_correct": False},
                        {"content": "Subcutaneous tissue", "is_correct": False},
                        {"content": "Epidermis", "is_correct": True}
                    ],
                    "explanation": "The epidermis is the outermost layer of the skin that acts as a protective barrier."
                },
                {
                    "content": "Which chamber of the heart pumps oxygenated blood into the aorta?",
                    "options": [
                        {"content": "Left ventricle", "is_correct": True},
                        {"content": "Right ventricle", "is_correct": False},
                        {"content": "Left atrium", "is_correct": False},
                        {"content": "Right atrium", "is_correct": False}
                    ],
                    "explanation": "The left ventricle pumps oxygenated blood into the aorta to supply the body."
                },
                {
                    'content': 'Which muscle is the primary flexor of the hip joint?',
                    'options': [
                        {'content': 'Gluteus maximus', 'is_correct': False},
                        {'content': 'Iliopsoas', 'is_correct': True},
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
                    'explanation': 'The loop of Henle creates and maintains the medullary concentration gradient '
                                   'through countercurrent multiplication.'
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
                    'explanation': 'ACE inhibitors are contraindicated in bilateral renal artery stenosis as they can '
                                   'cause acute kidney injury by reducing efferent arteriolar tone.'
                },
                {
                    "content": "Which antihypertensive medication class is contraindicated in bilateral renal artery stenosis?",
                    "options": [
                        {"content": "Calcium channel blockers", "is_correct": False},
                        {"content": "Beta blockers", "is_correct": False},
                        {"content": "Thiazide diuretics", "is_correct": False},
                        {"content": "ACE inhibitors", "is_correct": True}
                    ],
                    "explanation": "ACE inhibitors are contraindicated in bilateral renal artery stenosis as they can "
                                   "cause acute kidney injury by reducing efferent arteriolar tone."
                },
                {
                    "content": "Which drug is the first-line treatment for acute status epilepticus?",
                    "options": [
                        {"content": "Phenytoin", "is_correct": False},
                        {"content": "Valproic acid", "is_correct": False},
                        {"content": "Lorazepam", "is_correct": True},
                        {"content": "Carbamazepine", "is_correct": False}
                    ],
                    "explanation": "Lorazepam is the preferred first-line benzodiazepine for status epilepticus due "
                                   "to its rapid onset and longer duration of action."
                },
                {
                    "content": "What is the mechanism of action of metformin in treating type 2 diabetes?",
                    "options": [
                        {"content": "Decreases hepatic glucose production and increases insulin sensitivity",
                         "is_correct": True},
                        {"content": "Increases insulin secretion from pancreatic beta cells", "is_correct": False},
                        {"content": "Delays glucose absorption in the intestine", "is_correct": False},
                        {"content": "Increases glucose excretion in urine", "is_correct": False}
                    ],
                    "explanation": "Metformin primarily works by reducing hepatic glucose production and improving "
                                   "peripheral insulin sensitivity."
                },
                {
                    "content": "Which antibiotic class is most appropriate for treating atypical pneumonia?",
                    "options": [
                        {"content": "Penicillins", "is_correct": False},
                        {"content": "Macrolides", "is_correct": True},
                        {"content": "Cephalosporins", "is_correct": False},
                        {"content": "Aminoglycosides", "is_correct": False}
                    ],
                    "explanation": "Macrolides are effective against atypical organisms like Mycoplasma pneumoniae and Chlamydophila pneumoniae."
                },
                {
                    "content": "What is the antidote for acetaminophen toxicity?",
                    "options": [
                        {"content": "N-acetylcysteine", "is_correct": True},
                        {"content": "Atropine", "is_correct": False},
                        {"content": "Epinephrine", "is_correct": False},
                        {"content": "Activated charcoal", "is_correct": False}
                    ],
                    "explanation": "N-acetylcysteine replenishes glutathione stores and protects the liver in acetaminophen toxicity."
                },
                {
                    'content': 'Which drug is the first-line treatment for acute status epilepticus?',
                    'options': [
                        {'content': 'Phenytoin', 'is_correct': False},
                        {'content': 'Lorazepam', 'is_correct': True},
                        {'content': 'Valproic acid', 'is_correct': False},
                        {'content': 'Carbamazepine', 'is_correct': False}
                    ],
                    'explanation': 'Lorazepam is the preferred first-line benzodiazepine for status epilepticus due '
                                   'to its rapid onset and longer duration of action.'
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
                        {'content': 'Penicillins', 'is_correct': False},
                        {'content': 'Cephalosporins', 'is_correct': False},
                        {'content': 'Macrolides', 'is_correct': True},
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
                        {'content': 'Thrombolysis if PCI unavailable within 30 minutes', 'is_correct': False},
                        {'content': 'Primary PCI within 90 minutes', 'is_correct': True},
                        {'content': 'Conservative medical management', 'is_correct': False},
                        {'content': 'Immediate coronary artery bypass surgery', 'is_correct': False}
                    ],
                    'explanation': 'Primary PCI within 90 minutes is the gold standard treatment for STEMI if available at a capable facility.'
                },
                {
                    "content": "What is the most appropriate initial management for acute STEMI?",
                    "options": [
                        {"content": "Primary PCI within 90 minutes", "is_correct": True},
                        {"content": "Thrombolysis if PCI unavailable within 30 minutes", "is_correct": False},
                        {"content": "Conservative medical management", "is_correct": False},
                        {"content": "Immediate coronary artery bypass surgery", "is_correct": False}
                    ],
                    "explanation": "Primary PCI within 90 minutes is the gold standard treatment for STEMI if available at a capable facility."
                },
                {
                    "content": "Which finding is most specific for systemic lupus erythematosus?",
                    "options": [
                        {"content": "Anti-dsDNA antibodies", "is_correct": True},
                        {"content": "ANA positivity", "is_correct": False},
                        {"content": "Arthralgia", "is_correct": False},
                        {"content": "Malar rash", "is_correct": False}
                    ],
                    "explanation": "Anti-dsDNA antibodies are highly specific for SLE and correlate with disease activity."
                },
                {
                    "content": "What is the most common cause of hospital-acquired pneumonia?",
                    "options": [
                        {"content": "Streptococcus pneumoniae", "is_correct": False},
                        {"content": "Klebsiella pneumoniae", "is_correct": False},
                        {"content": "Haemophilus influenzae", "is_correct": False},
                        {"content": "Staphylococcus aureus", "is_correct": True}
                    ],
                    "explanation": "Staphylococcus aureus, including MRSA, is the most common cause of hospital-acquired pneumonia."
                },
                {
                    "content": "Which condition is most strongly associated with HLA-B27?",
                    "options": [
                        {"content": "Ankylosing spondylitis", "is_correct": True},
                        {"content": "Rheumatoid arthritis", "is_correct": False},
                        {"content": "Systemic lupus erythematosus", "is_correct": False},
                        {"content": "Osteoarthritis", "is_correct": False}
                    ],
                    "explanation": "HLA-B27 is strongly associated with ankylosing spondylitis and other spondyloarthropathies."
                },
                {
                    "content": "What is the diagnostic hallmark of nephrotic syndrome?",
                    "options": [
                        {"content": "Hematuria", "is_correct": False},
                        {"content": "Pyuria", "is_correct": False},
                        {"content": "Proteinuria >3.5 g/day", "is_correct": True},
                        {"content": "Oliguria", "is_correct": False}
                    ],
                    "explanation": "Nephrotic syndrome is characterized by proteinuria >3.5 g/day, hypoalbuminemia, "
                                   "edema, and often hyperlipidemia. Additional features may include an increased "
                                   "risk of infections and thromboembolism."
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
                        {'content': 'Streptococcus pneumoniae', 'is_correct': False},
                        {'content': 'Staphylococcus aureus', 'is_correct': True},
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
                    'explanation': 'Early laparoscopic cholecystectomy (within 72 hours) is the preferred treatment '
                                   'for acute cholecystitis in suitable candidates.'
                },
                {
                    'content': 'What is the most appropriate management for a patient with a perforated peptic ulcer?',
                    'options': [
                        {'content': 'Antibiotics alone', 'is_correct': False},
                        {'content': 'Endoscopic clipping', 'is_correct': False},
                        {'content': 'Emergency laparotomy and ulcer repair', 'is_correct': True},
                        {'content': 'Observation and pain management', 'is_correct': False}
                    ],
                    'explanation': 'Emergency laparotomy with repair or resection is the standard treatment for '
                                   'perforated peptic ulcer to prevent peritonitis.'
                },
                {
                    'content': 'What is the most common cause of postoperative fever within the first 48 hours?',
                    'options': [
                        {'content': 'Atelectasis', 'is_correct': True},
                        {'content': 'Urinary tract infection', 'is_correct': False},
                        {'content': 'Wound infection', 'is_correct': False},
                        {'content': 'Deep vein thrombosis', 'is_correct': False}
                    ],
                    'explanation': 'Atelectasis is the most common cause of fever in the first 48 hours after '
                                   'surgery, due to impaired lung expansion.'
                },
                {
                    'content': 'What is the most appropriate initial management for acute cholecystitis?',
                    'options': [
                        {'content': 'Antibiotics alone', 'is_correct': False},
                        {'content': 'Percutaneous cholecystostomy', 'is_correct': False},
                        {'content': 'ERCP', 'is_correct': False},
                        {'content': 'Early laparoscopic cholecystectomy', 'is_correct': True}
                    ],
                    'explanation': 'Early laparoscopic cholecystectomy (within 72 hours) is the preferred treatment '
                                   'for acute cholecystitis in suitable candidates.'
                },
                {
                    'content': 'Which is the most appropriate fluid for initial resuscitation in hemorrhagic shock?',
                    'options': [
                        {'content': 'Balanced crystalloid solution', 'is_correct': True},
                        {'content': 'Normal saline', 'is_correct': False},
                        {'content': 'Albumin', 'is_correct': False},
                        {'content': 'Dextrose solution', 'is_correct': False}
                    ],
                    'explanation': 'Balanced crystalloid solutions are preferred for initial resuscitation as they '
                                   'cause less metabolic derangement.'
                },
                {
                    'content': 'What is the most common complication after splenectomy?',
                    'options': [
                        {'content': 'Hemorrhage', 'is_correct': False},
                        {'content': 'Subphrenic abscess', 'is_correct': False},
                        {'content': 'Thrombocytosis', 'is_correct': False},
                        {'content': 'Left lower lobe atelectasis', 'is_correct': True},
                    ],
                    'explanation': 'Left lower lobe atelectasis is the most common post-splenectomy complication due '
                                   'to decreased left diaphragm movement.'
                },
                {
                    'content': 'Which is the most appropriate fluid for initial resuscitation in hemorrhagic shock?',
                    'options': [
                        {'content': 'Balanced crystalloid solution', 'is_correct': True},
                        {'content': 'Normal saline', 'is_correct': False},
                        {'content': 'Albumin', 'is_correct': False},
                        {'content': 'Dextrose solution', 'is_correct': False}
                    ],
                    'explanation': 'Balanced crystalloid solutions are preferred for initial resuscitation as they '
                                   'cause less metabolic derangement.'
                },
                {
                    'content': 'What is the most common complication after splenectomy?',
                    'options': [
                        {'content': 'Hemorrhage', 'is_correct': False},
                        {'content': 'Left lower lobe atelectasis', 'is_correct': True},
                        {'content': 'Subphrenic abscess', 'is_correct': False},
                        {'content': 'Thrombocytosis', 'is_correct': False}
                    ],
                    'explanation': 'Left lower lobe atelectasis is the most common post-splenectomy complication due '
                                   'to decreased left diaphragm movement.'
                }
            ]
        },
        'pediatrics': {
            'questions': [
                {
                    'content': 'What is the most common presenting symptom of intussusception?',
                    'options': [
                        {'content': 'Bilious vomiting', 'is_correct': False},
                        {'content': 'Bloody stool', 'is_correct': False},
                        {'content': 'Intermittent severe abdominal pain', 'is_correct': True},
                        {'content': 'Fever', 'is_correct': False}
                    ],
                    'explanation': 'Intermittent severe abdominal pain is typically the first symptom of '
                                   'intussusception, often causing a child to draw their knees to their chest.'
                },
                {
                    'content': 'What is the first-line treatment for a child with croup?',
                    'options': [
                        {'content': 'Dexamethasone', 'is_correct': True},
                        {'content': 'Ceftriaxone', 'is_correct': False},
                        {'content': 'Albuterol', 'is_correct': False},
                        {'content': 'Epinephrine', 'is_correct': False}
                    ],
                    'explanation': 'Dexamethasone is the first-line treatment for croup to reduce inflammation and improve symptoms.'
                },
                {
                    'content': 'Which vaccine is recommended for infants at birth?',
                    'options': [
                        {'content': 'Hepatitis B', 'is_correct': True},
                        {'content': 'Rotavirus', 'is_correct': False},
                        {'content': 'Diphtheria, tetanus, and pertussis (DTP)', 'is_correct': False},
                        {'content': 'Pneumococcal', 'is_correct': False}
                    ],
                    'explanation': 'Hepatitis B vaccine is recommended for infants at birth to prevent vertical transmission.'
                },
                {
                    'content': 'What is the first-line treatment for acute otitis media in children?',
                    'options': [
                        {'content': 'Azithromycin', 'is_correct': False},
                        {'content': 'Amoxicillin-clavulanate', 'is_correct': False},
                        {'content': 'Amoxicillin', 'is_correct': True},
                        {'content': 'Cefuroxime', 'is_correct': False}
                    ],
                    'explanation': 'Amoxicillin is the first-line treatment for uncomplicated acute otitis media in children.'
                },
                {
                    'content': 'Which vaccine is recommended at birth?',
                    'options': [
                        {'content': 'Rotavirus', 'is_correct': False},
                        {'content': 'Hepatitis B', 'is_correct': True},
                        {'content': 'Diphtheria, tetanus, and pertussis (DTaP)', 'is_correct': False},
                        {'content': 'Polio', 'is_correct': False}
                    ],
                    'explanation': 'The first dose of the Hepatitis B vaccine should be given at birth to prevent perinatal transmission.'
                },
                {
                    'content': 'Which of the following is a common cause of bronchiolitis in infants?',
                    'options': [
                        {'content': 'Respiratory syncytial virus (RSV)', 'is_correct': True},
                        {'content': 'Influenza virus', 'is_correct': False},
                        {'content': 'Adenovirus', 'is_correct': False},
                        {'content': 'Coronavirus', 'is_correct': False}
                    ],
                    'explanation': 'Respiratory syncytial virus (RSV) is the most common cause of bronchiolitis in infants.'
                },
                {
                    'content': 'Which congenital heart defect is most commonly associated with Down syndrome?',
                    'options': [
                        {'content': 'Tetralogy of Fallot', 'is_correct': False},
                        {'content': 'Transposition of great arteries', 'is_correct': False},
                        {'content': 'Patent ductus arteriosus', 'is_correct': False},
                        {'content': 'Atrioventricular septal defect', 'is_correct': True}
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
                    'explanation': 'Severe preeclampsia at 34 weeks warrants delivery after completing antenatal '
                                   'corticosteroids for fetal lung maturity.'
                },
                {
                    'content': 'What is the most common cause of postpartum hemorrhage?',
                    'options': [
                        {'content': 'Cervical lacerations', 'is_correct': False},
                        {'content': 'Retained placenta', 'is_correct': False},
                        {'content': 'Uterine atony', 'is_correct': True},
                        {'content': 'Coagulopathy', 'is_correct': False}
                    ],
                    'explanation': 'Uterine atony, or failure of the uterus to contract after delivery, is the '
                                   'leading cause of postpartum hemorrhage.'
                },
                {
                    'content': 'Which is the recommended method of delivery for a breech presentation at term?',
                    'options': [
                        {'content': 'Vaginal delivery', 'is_correct': False},
                        {'content': 'Cesarean section', 'is_correct': True},
                        {'content': 'Vacuum-assisted delivery', 'is_correct': False},
                        {'content': 'Forceps delivery', 'is_correct': False}
                    ],
                    'explanation': 'Cesarean section is recommended for breech presentation at term to reduce the '
                                   'risk of injury to both mother and baby.'
                },
                {
                    'content': 'What is the most appropriate management for a patient with preeclampsia at 34 weeks '
                               'gestation?',
                    'options': [
                        {'content': 'Induction of labor', 'is_correct': True},
                        {'content': 'Observation with blood pressure monitoring', 'is_correct': False},
                        {'content': 'Administration of antihypertensive medications alone', 'is_correct': False},
                        {'content': 'Cesarean delivery', 'is_correct': False}
                    ],
                    'explanation': 'Induction of labor is the recommended management for preeclampsia at or beyond 34 weeks gestation.'
                },
                {
                    'content': 'Which test is most commonly used to screen for gestational diabetes?',
                    'options': [
                        {'content': 'Oral glucose tolerance test (OGTT)', 'is_correct': True},
                        {'content': 'Random glucose test', 'is_correct': False},
                        {'content': 'Fasting blood glucose test', 'is_correct': False},
                        {'content': 'Hemoglobin A1c', 'is_correct': False}
                    ],
                    'explanation': 'The oral glucose tolerance test (OGTT) is the standard screening method for gestational diabetes.'
                },
                {
                    'content': 'What is the recommended management for a patient with a ruptured ectopic pregnancy?',
                    'options': [
                        {'content': 'Methotrexate therapy', 'is_correct': False},
                        {'content': 'Surgical removal of the ectopic pregnancy', 'is_correct': True},
                        {'content': 'Expectant management', 'is_correct': False},
                        {'content': 'Intravenous antibiotics', 'is_correct': False}
                    ],
                    'explanation': 'Surgical removal is typically required for a ruptured ectopic pregnancy to control bleeding.'
                },
                {
                    'content': 'Which medication is first-line for postpartum hemorrhage?',
                    'options': [
                        {'content': 'Methylergonovine', 'is_correct': False},
                        {'content': 'Carboprost', 'is_correct': False},
                        {'content': 'Oxytocin', 'is_correct': True},
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
                    'explanation': 'Placental abruption is the most common cause of third-trimester bleeding and can '
                                   'lead to significant maternal and fetal complications.'
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
                    'explanation': 'Intramuscular epinephrine is the first-line treatment for anaphylaxis due to its '
                                   'rapid onset and effectiveness in treating multiple aspects of the reaction.'
                },
                {
                    'content': 'What is the initial management for a patient with a suspected acute myocardial infarction (MI)?',
                    'options': [
                        {'content': 'Morphine and oxygen', 'is_correct': False},
                        {'content': 'Fibrinolysis alone', 'is_correct': False},
                        {'content': 'Aspirin and nitroglycerin', 'is_correct': True},
                        {'content': 'Beta-blockers', 'is_correct': False}
                    ],
                    'explanation': 'Aspirin and nitroglycerin are typically given immediately in suspected MI to '
                                   'reduce clot formation and improve coronary perfusion.'
                },
                {
                    'content': 'Which of the following is the most common cause of non-traumatic abdominal pain in the emergency department?',
                    'options': [
                        {'content': 'Cholecystitis', 'is_correct': False},
                        {'content': 'Peptic ulcer disease', 'is_correct': False},
                        {'content': 'Diverticulitis', 'is_correct': False},
                        {'content': 'Acute appendicitis', 'is_correct': True},
                    ],
                    'explanation': 'Acute appendicitis is the most common cause of non-traumatic abdominal pain requiring emergency care.'
                },
                {
                    'content': 'What is the first-line treatment for anaphylaxis?',
                    'options': [
                        {'content': 'Epinephrine', 'is_correct': True},
                        {'content': 'Antihistamines', 'is_correct': False},
                        {'content': 'Corticosteroids', 'is_correct': False},
                        {'content': 'Oxygen therapy', 'is_correct': False}
                    ],
                    'explanation': 'Epinephrine is the first-line treatment for anaphylaxis, as it reverses life-threatening symptoms rapidly.'
                },
                {
                    'content': 'Which rhythm is most appropriate for immediate defibrillation?',
                    'options': [
                        {'content': 'Ventricular fibrillation', 'is_correct': True},
                        {'content': 'Pulseless electrical activity', 'is_correct': False},
                        {'content': 'Asystole', 'is_correct': False},
                        {'content': 'Complete heart block', 'is_correct': False}
                    ],
                    'explanation': 'Ventricular fibrillation is a shockable rhythm that requires immediate '
                                   'defibrillation as the first-line treatment.'
                },
                {
                    'content': 'What is the first step in managing a patient with suspected myocardial infarction?',
                    'options': [
                        {'content': 'Obtain an ECG', 'is_correct': False},
                        {'content': 'Administer aspirin', 'is_correct': True},
                        {'content': 'Administer morphine', 'is_correct': False},
                        {'content': 'Insert an intravenous line', 'is_correct': False}
                    ],
                    'explanation': 'Aspirin is given early in myocardial infarction to inhibit platelet aggregation and reduce the infarct size.'
                },
                {
                    'content': 'What is the most appropriate initial treatment for anaphylaxis?',
                    'options': [
                        {'content': 'Intramuscular epinephrine', 'is_correct': True},
                        {'content': 'Oral antihistamines', 'is_correct': False},
                        {'content': 'Intravenous fluids', 'is_correct': False},
                        {'content': 'Corticosteroids', 'is_correct': False}
                    ],
                    'explanation': 'Intramuscular epinephrine is the first-line treatment for anaphylaxis to '
                                   'counteract the effects of histamine release.'
                },
                {
                    'content': 'What is the most appropriate initial fluid for severe diabetic ketoacidosis?',
                    'options': [
                        {'content': 'Lactated Ringers', 'is_correct': False},
                        {'content': 'D5W', 'is_correct': False},
                        {'content': 'Half-normal saline', 'is_correct': False},
                        {'content': 'Normal saline', 'is_correct': True}
                    ],
                    'explanation': 'Normal saline is the preferred initial fluid for DKA to correct volume depletion '
                                   'and provide sodium replacement.'
                }
            ]
        },
        'psychiatry': {
            'questions': [
                {
                    'content': 'Which antipsychotic medication has the lowest risk of extrapyramidal symptoms?',
                    'options': [
                        {'content': 'Haloperidol', 'is_correct': False},
                        {'content': 'Risperidone', 'is_correct': False},
                        {'content': 'Chlorpromazine', 'is_correct': False},
                        {'content': 'Quetiapine', 'is_correct': True}
                    ],
                    'explanation': 'Quetiapine has the lowest risk of extrapyramidal symptoms among antipsychotics '
                                   'due to its low D2 receptor affinity.'
                },
                {
                    'content': 'What is the first-line treatment for generalized anxiety disorder (GAD)?',
                    'options': [
                        {'content': 'Selective serotonin reuptake inhibitors (SSRIs)', 'is_correct': True},
                        {'content': 'Benzodiazepines', 'is_correct': False},
                        {'content': 'Antipsychotics', 'is_correct': False},
                        {'content': 'Tricyclic antidepressants', 'is_correct': False}
                    ],
                    'explanation': 'SSRIs are considered first-line treatment for generalized anxiety disorder due to '
                                   'their efficacy and safety profile.'
                },
                {
                    'content': 'Which of the following is a common side effect of antipsychotic medications?',
                    'options': [
                        {'content': 'Extrapyramidal symptoms (EPS)', 'is_correct': True},
                        {'content': 'Weight loss', 'is_correct': False},
                        {'content': 'Hyperactivity', 'is_correct': False},
                        {'content': 'Dizziness', 'is_correct': False}
                    ],
                    'explanation': 'Extrapyramidal symptoms (EPS) such as tremors, rigidity, and bradykinesia are '
                                   'common side effects of antipsychotic medications.'
                },
                {
                    'content': 'What is the most common symptom of generalized anxiety disorder?',
                    'options': [
                        {'content': 'Mood swings', 'is_correct': False},
                        {'content': 'Excessive worry', 'is_correct': True},
                        {'content': 'Delusions', 'is_correct': False},
                        {'content': 'Hallucinations', 'is_correct': False}
                    ],
                    'explanation': 'Excessive and uncontrollable worry is the hallmark symptom of generalized anxiety disorder.'
                },
                {
                    'content': 'Which class of medications is commonly used in the treatment of depression?',
                    'options': [
                        {'content': 'Antipsychotics', 'is_correct': False},
                        {'content': 'Selective serotonin reuptake inhibitors (SSRIs)', 'is_correct': True},
                        {'content': 'Benzodiazepines', 'is_correct': False},
                        {'content': 'Opioids', 'is_correct': False}
                    ],
                    'explanation': 'SSRIs are the first-line treatment for depression, as they increase serotonin levels in the brain.'
                },
                {
                    'content': 'What is the hallmark symptom of major depressive disorder (MDD)?',
                    'options': [
                        {'content': 'Persistent low mood', 'is_correct': True},
                        {'content': 'Mania', 'is_correct': False},
                        {'content': 'Grandiosity', 'is_correct': False},
                        {'content': 'Euphoria', 'is_correct': False}
                    ],
                    'explanation': 'The hallmark symptom of major depressive disorder is a persistent low mood or '
                                   'loss of interest in daily activities.'
                },
                {
                    'content': 'What is the first-line treatment for major depressive disorder?',
                    'options': [
                        {'content': 'TCAs', 'is_correct': False},
                        {'content': 'MAOIs', 'is_correct': False},
                        {'content': 'SSRIs', 'is_correct': True},
                        {'content': 'Benzodiazepines', 'is_correct': False}
                    ],
                    'explanation': 'SSRIs are the first-line treatment for major depression due to their favorable '
                                   'side effect profile and efficacy.'
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
                    'explanation': 'CT pulmonary angiogram is the gold standard for diagnosing pulmonary embolism due '
                                   'to its high sensitivity and specificity.'
                },
                {
                    'content': 'Which imaging modality is most appropriate for evaluating suspected pulmonary embolism?',
                    'options': [
                        {'content': 'CT pulmonary angiography', 'is_correct': True},
                        {'content': 'Chest X-ray', 'is_correct': False},
                        {'content': 'Ultrasound', 'is_correct': False},
                        {'content': 'MRI', 'is_correct': False}
                    ],
                    'explanation': 'CT pulmonary angiography is the gold standard for evaluating pulmonary embolism.'
                },
                {
                    'content': 'What is the most common finding in a chest X-ray of a patient with pneumonia?',
                    'options': [
                        {'content': 'Pleural effusion', 'is_correct': False},
                        {'content': 'Cardiomegaly', 'is_correct': False},
                        {'content': 'Consolidation', 'is_correct': True},
                        {'content': 'Lung nodules', 'is_correct': False}
                    ],
                    'explanation': 'Consolidation is the most common radiological finding in pneumonia, indicating '
                                   'areas of alveolar fluid accumulation.'
                },
                {
                    'content': 'What does a “snowman sign” on a chest X-ray suggest?',
                    'options': [
                        {'content': 'Total anomalous pulmonary venous return (TAPVR)', 'is_correct': True},
                        {'content': 'Pulmonary embolism', 'is_correct': False},
                        {'content': 'Lung cancer', 'is_correct': False},
                        {'content': 'Aortic dissection', 'is_correct': False}
                    ],
                    'explanation': 'The “snowman sign” is a classic radiologic feature of total anomalous pulmonary '
                                   'venous return (TAPVR) due to the enlarged superior vena cava and dilated heart.'
                },
                {
                    'content': 'Which of the following is the best initial imaging test for a patient with suspected stroke?',
                    'options': [
                        {'content': 'MRI', 'is_correct': False},
                        {'content': 'Non-contrast CT scan of the head', 'is_correct': True},
                        {'content': 'Ultrasound of the carotid arteries', 'is_correct': False},
                        {'content': 'Chest X-ray', 'is_correct': False}
                    ],
                    'explanation': 'A non-contrast CT scan is the best initial test to rule out hemorrhagic stroke.'
                },
                {
                    'content': 'What is the primary advantage of using ultrasound in the assessment of abdominal pain?',
                    'options': [
                        {'content': 'High resolution of soft tissues', 'is_correct': False},
                        {'content': 'Cost-effectiveness compared to CT', 'is_correct': False},
                        {'content': 'Ability to diagnose tumors', 'is_correct': False},
                        {'content': 'Real-time imaging and safety', 'is_correct': True}
                    ],
                    'explanation': 'Ultrasound provides real-time imaging and is considered safe, making it an '
                                   'excellent tool for assessing abdominal pain.'
                },
                {
                    'content': 'What is the best initial imaging study for suspected acute appendicitis?',
                    'options': [
                        {'content': 'Ultrasound in pediatric/pregnant patients, CT for others', 'is_correct': True},
                        {'content': 'MRI for all patients', 'is_correct': False},
                        {'content': 'Plain abdominal radiograph', 'is_correct': False},
                        {'content': 'Nuclear medicine scan', 'is_correct': False}
                    ],
                    'explanation': 'Ultrasound is preferred in children and pregnant patients to avoid radiation, '
                                   'while CT is more sensitive and specific in other adults.'
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
                    'content': 'Which of the following is the most common cause of acute kidney injury in hospitalized patients?',
                    'options': [
                        {'content': 'Pre-renal azotemia', 'is_correct': False},
                        {'content': 'Post-renal obstruction', 'is_correct': False},
                        {'content': 'Acute tubular necrosis', 'is_correct': True},
                        {'content': 'Glomerulonephritis', 'is_correct': False}
                    ],
                    'explanation': 'Acute tubular necrosis is the most common cause of acute kidney injury in hospitalized patients.'
                },
                {
                    'content': 'Which of the following best describes the characteristic histologic finding in Crohn\'s disease?',
                    'options': [
                        {'content': 'Transmural inflammation', 'is_correct': True},
                        {'content': 'Mucosal ulcerations', 'is_correct': False},
                        {'content': 'Pseudopolyps', 'is_correct': False},
                        {'content': 'Crypt abscesses', 'is_correct': False}
                    ],
                    'explanation': 'Transmural inflammation is the hallmark histologic finding in Crohn\'s disease.'
                },
                {
                    'content': 'Which of the following is a characteristic feature of a malignant tumor?',
                    'options': [
                        {'content': 'Well-defined borders', 'is_correct': False},
                        {'content': 'Infiltration into surrounding tissue', 'is_correct': True},
                        {'content': 'Slow growth', 'is_correct': False},
                        {'content': 'Capsule formation', 'is_correct': False}
                    ],
                    'explanation': 'Malignant tumors typically invade surrounding tissues and lack well-defined borders.'
                },
                {
                    'content': 'Which type of hypersensitivity reaction is associated with systemic lupus erythematosus (SLE)?',
                    'options': [
                        {'content': 'Type III (immune complex)', 'is_correct': True},
                        {'content': 'Type I (IgE-mediated)', 'is_correct': False},
                        {'content': 'Type II (cytotoxic)', 'is_correct': False},
                        {'content': 'Type IV (delayed-type)', 'is_correct': False}
                    ],
                    'explanation': 'SLE is a type III hypersensitivity reaction, where immune complexes deposit in '
                                   'tissues, causing inflammation and tissue damage.'
                },
                {
                    'content': 'Which is the most common type of lung cancer?',
                    'options': [
                        {'content': 'Squamous cell carcinoma', 'is_correct': False},
                        {'content': 'Small cell carcinoma', 'is_correct': False},
                        {'content': 'Adenocarcinoma', 'is_correct': True},
                        {'content': 'Large cell carcinoma', 'is_correct': False}
                    ],
                    'explanation': 'Adenocarcinoma is the most common type of lung cancer, particularly among non-smokers.'
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
        'neonatology': {
            'questions': [
                {
                    'content': 'What is the most common cause of neonatal jaundice?',
                    'options': [
                        {'content': 'Biliary atresia', 'is_correct': False},
                        {'content': 'Sepsis', 'is_correct': False},
                        {'content': 'Hemolytic disease of the newborn', 'is_correct': False},
                        {'content': 'Physiological jaundice', 'is_correct': True}
                    ],
                    'explanation': 'Physiological jaundice is the most common cause in the first few days of life due to immature liver enzymes.'
                },
                {
                    'content': 'Which is the most important intervention in the management of neonatal respiratory distress syndrome (RDS)?',
                    'options': [
                        {'content': 'Surfactant therapy', 'is_correct': True},
                        {'content': 'Antibiotics', 'is_correct': False},
                        {'content': 'Intubation', 'is_correct': False},
                        {'content': 'Diuretics', 'is_correct': False}
                    ],
                    'explanation': 'Surfactant therapy is the key intervention in neonatal RDS, as it reduces '
                                   'alveolar collapse and improves oxygenation.'
                },
                {
                    'content': 'At what gestational age is surfactant therapy most commonly administered to preterm infants?',
                    'options': [
                        {'content': 'Before 28 weeks gestation', 'is_correct': True},
                        {'content': '32-34 weeks gestation', 'is_correct': False},
                        {'content': '37-40 weeks gestation', 'is_correct': False},
                        {'content': 'After 40 weeks gestation', 'is_correct': False}
                    ],
                    'explanation': 'Surfactant therapy is most commonly administered to infants born before 28 weeks '
                                   'gestation due to the lack of surfactant production.'
                },
                {
                    'content': 'What is the primary cause of hypoxic-ischemic encephalopathy (HIE) in neonates?',
                    'options': [
                        {'content': 'Intrauterine infection', 'is_correct': False},
                        {'content': 'Neonatal seizures', 'is_correct': False},
                        {'content': 'Perinatal asphyxia', 'is_correct': True},
                        {'content': 'Kernicterus', 'is_correct': False}
                    ],
                    'explanation': 'Perinatal asphyxia, leading to oxygen deprivation to the brain, is the primary '
                                   'cause of hypoxic-ischemic encephalopathy.'
                },
                {
                    'content': 'What is the most common congenital cardiac defect in neonates?',
                    'options': [
                        {'content': 'Atrial septal defect (ASD)', 'is_correct': False},
                        {'content': 'Ventricular septal defect (VSD)', 'is_correct': True},
                        {'content': 'Tetralogy of Fallot', 'is_correct': False},
                        {'content': 'Patent ductus arteriosus (PDA)', 'is_correct': False}
                    ],
                    'explanation': 'Ventricular septal defect (VSD) is the most common congenital cardiac defect, '
                                   'accounting for about 25% of cases.'
                }
            ]
        },
        'leadership_and_management': {
            'questions': [
                {
                    'content': 'Which of the following is a key element of transformational leadership?',
                    'options': [
                        {'content': 'Micromanaging team tasks', 'is_correct': False},
                        {'content': 'Focusing only on results and goals', 'is_correct': False},
                        {'content': 'Inspiring and motivating employees', 'is_correct': True},
                        {'content': 'Maintaining strict control over team behavior', 'is_correct': False}
                    ],
                    'explanation': 'Transformational leadership focuses on inspiring and motivating employees to '
                                   'achieve higher levels of performance.'
                },
                {
                    'content': 'What is the primary purpose of strategic planning in leadership?',
                    'options': [
                        {'content': 'Aligning the team with the organization’s vision and goals', 'is_correct': True},
                        {'content': 'Developing individual performance reviews', 'is_correct': False},
                        {'content': 'Creating a team-building exercise', 'is_correct': False},
                        {'content': 'Assigning tasks based on skill sets', 'is_correct': False}
                    ],
                    'explanation': 'Strategic planning aligns the team with the overall vision and goals of the '
                                   'organization to ensure success.'
                },
                {
                    'content': 'Which of the following is a key challenge of leadership in a diverse workforce?',
                    'options': [
                        {'content': 'Ensuring uniformity in work processes', 'is_correct': False},
                        {'content': 'Managing different communication styles and perspectives', 'is_correct': True},
                        {'content': 'Limiting innovation and change', 'is_correct': False},
                        {'content': 'Restricting decision-making to a single group', 'is_correct': False}
                    ],
                    'explanation': 'Managing diverse communication styles and perspectives is a key challenge in '
                                   'leadership, requiring sensitivity and flexibility.'
                },
                {
                    'content': 'What is a common characteristic of a transactional leadership style?',
                    'options': [
                        {'content': 'Encouraging personal development and innovation', 'is_correct': False},
                        {'content': 'Fostering a sense of shared vision and motivation', 'is_correct': False},
                        {'content': 'Empowering employees to make autonomous decisions', 'is_correct': False},
                        {'content': 'Rewarding compliance with clear tasks and goals', 'is_correct': True}
                    ],
                    'explanation': 'Transactional leadership focuses on rewarding compliance and performance, '
                                   'typically within a structured environment.'
                },
                {
                    'content': 'Which of the following is a critical component of effective management?',
                    'options': [
                        {'content': 'Clear communication and setting expectations', 'is_correct': True},
                        {'content': 'Avoiding delegation to maintain control', 'is_correct': False},
                        {'content': 'Focusing solely on short-term goals', 'is_correct': False},
                        {'content': 'Limiting employee feedback and interaction', 'is_correct': False}
                    ],
                    'explanation': 'Clear communication and setting clear expectations are key to ensuring effective '
                                   'management and achieving organizational goals.'
                }
            ]
        },
        'microbiology': {
            'questions': [
                {
                    'content': 'What is the most common causative organism of community-acquired pneumonia?',
                    'options': [
                        {'content': 'Streptococcus pneumoniae', 'is_correct': True},
                        {'content': 'Mycoplasma pneumoniae', 'is_correct': False},
                        {'content': 'Haemophilus influenzae', 'is_correct': False},
                        {'content': 'Chlamydia pneumoniae', 'is_correct': False}
                    ],
                    'explanation': 'Streptococcus pneumoniae is the most common causative organism of community-acquired pneumonia.'
                },
                {
                    'content': 'Which of the following bacteria is commonly associated with urinary tract infections?',
                    'options': [
                        {'content': 'Staphylococcus aureus', 'is_correct': False},
                        {'content': 'Streptococcus pyogenes', 'is_correct': False},
                        {'content': 'Escherichia coli', 'is_correct': True},
                        {'content': 'Clostridium difficile', 'is_correct': False}
                    ],
                    'explanation': 'Escherichia coli is the most common pathogen responsible for urinary tract infections.'
                },
                {
                    'content': 'Which bacterium is the causative agent of tuberculosis?',
                    'options': [
                        {'content': 'Mycobacterium tuberculosis', 'is_correct': True},
                        {'content': 'Streptococcus pneumoniae', 'is_correct': False},
                        {'content': 'Neisseria gonorrhoeae', 'is_correct': False},
                        {'content': 'Salmonella typhi', 'is_correct': False}
                    ],
                    'explanation': 'Mycobacterium tuberculosis is the causative organism responsible for tuberculosis.'
                },
                {
                    'content': 'Which of the following is a characteristic feature of Gram-negative bacteria?',
                    'options': [
                        {'content': 'Thick peptidoglycan layer', 'is_correct': False},
                        {'content': 'No cell wall', 'is_correct': False},
                        {'content': 'Endospores formation', 'is_correct': False},
                        {'content': 'Thin peptidoglycan layer and outer membrane', 'is_correct': True}
                    ],
                    'explanation': 'Gram-negative bacteria have a thin peptidoglycan layer and an outer membrane that '
                                   'contains lipopolysaccharides.'
                },
                {
                    'content': 'What is the most common cause of food poisoning in the United States?',
                    'options': [
                        {'content': 'Salmonella spp.', 'is_correct': True},
                        {'content': 'Staphylococcus aureus', 'is_correct': False},
                        {'content': 'Clostridium botulinum', 'is_correct': False},
                        {'content': 'Escherichia coli', 'is_correct': False}
                    ],
                    'explanation': 'Salmonella is the most common cause of foodborne illness in the U.S., '
                                   'particularly from undercooked poultry.'
                }
            ]
        },
        'hiv_aids_medicine': {
            'questions': [
                {
                    'content': 'Which class of drugs is commonly used as part of highly active antiretroviral therapy (HAART)?',
                    'options': [
                        {'content': 'Nucleoside reverse transcriptase inhibitors (NRTIs)', 'is_correct': True},
                        {'content': 'Beta-blockers', 'is_correct': False},
                        {'content': 'Statins', 'is_correct': False},
                        {'content': 'Proton pump inhibitors', 'is_correct': False}
                    ],
                    'explanation': 'NRTIs are a class of antiretroviral drugs that inhibit reverse transcriptase, '
                                   'a key enzyme in HIV replication.'
                },
                {
                    'content': 'What is the primary mode of HIV transmission?',
                    'options': [
                        {'content': 'Airborne droplets', 'is_correct': False},
                        {'content': 'Sharing of needles', 'is_correct': True},
                        {'content': 'Touching an infected person', 'is_correct': False},
                        {'content': 'Insect bites', 'is_correct': False}
                    ],
                    'explanation': 'HIV is primarily transmitted through contact with infected blood, semen, vaginal '
                                   'fluids, or breast milk, often via sharing needles or unprotected sexual activity.'
                },
                {
                    'content': 'Which laboratory test is commonly used to monitor the effectiveness of HIV treatment?',
                    'options': [
                        {'content': 'CD4 count', 'is_correct': True},
                        {'content': 'Complete blood count (CBC)', 'is_correct': False},
                        {'content': 'Liver function test', 'is_correct': False},
                        {'content': 'Blood glucose levels', 'is_correct': False}
                    ],
                    'explanation': 'The CD4 count is a key measure to assess the immune system’s health and monitor '
                                   'the effectiveness of HIV treatment.'
                },
                {
                    'content': 'What is the significance of achieving an undetectable viral load in HIV patients?',
                    'options': [
                        {'content': 'It eliminates the virus from the body.', 'is_correct': False},
                        {'content': 'It cures the patient of HIV.', 'is_correct': False},
                        {'content': 'It reduces the risk of HIV transmission.', 'is_correct': True},
                        {'content': 'It means the patient no longer needs treatment.', 'is_correct': False}
                    ],
                    'explanation': 'Achieving an undetectable viral load greatly reduces the risk of transmitting HIV '
                                   'to others but does not indicate the virus has been eliminated.'
                },
                {
                    'content': 'What is a key strategy to prevent mother-to-child transmission of HIV?',
                    'options': [
                        {'content': 'Administering antiretroviral therapy to the mother during pregnancy',
                         'is_correct': True},
                        {'content': 'Avoiding vaccination during pregnancy', 'is_correct': False},
                        {'content': 'Reducing the mother’s weight gain during pregnancy', 'is_correct': False},
                        {'content': 'Using only herbal medicine', 'is_correct': False}
                    ],
                    'explanation': 'Administering antiretroviral therapy during pregnancy significantly reduces the '
                                   'risk of mother-to-child transmission of HIV.'
                },
                {
                    'content': 'Which of the following is an effective method to prevent HIV transmission?',
                    'options': [
                        {'content': 'Regular handwashing', 'is_correct': False},
                        {'content': 'Avoiding contact with animals', 'is_correct': False},
                        {'content': 'Drinking boiled water', 'is_correct': False},
                        {'content': 'Consistent and correct use of condoms', 'is_correct': True}
                    ],
                    'explanation': 'Consistent and correct use of condoms is one of the most effective ways to '
                                   'prevent HIV transmission during sexual activity.'
                }
            ],

        'preventive_medicine': {
            'questions': [
                {
                    'content': 'At what age should colorectal cancer screening begin for average-risk individuals?',
                    'options': [
                        {'content': '50 years', 'is_correct': False},
                        {'content': '45 years', 'is_correct': True},
                        {'content': '40 years', 'is_correct': False},
                        {'content': '55 years', 'is_correct': False}
                    ],
                    'explanation': 'Current guidelines recommend starting colorectal cancer screening at age 45 for '
                                   'average-risk individuals.'
                },
                {
                    'content': 'Which vaccination is recommended for all healthcare workers?',
                    'options': [
                        {'content': 'Hepatitis B', 'is_correct': True},
                        {'content': 'Influenza', 'is_correct': False},
                        {'content': 'Tdap', 'is_correct': False},
                        {'content': 'Varicella', 'is_correct': False}
                    ],
                    'explanation': 'Hepatitis B vaccination is recommended for all healthcare workers due to their '
                                   'potential exposure to bloodborne pathogens.'
                },
                {
                    'content': 'Which is the most effective method for primary prevention of cardiovascular disease?',
                    'options': [
                        {'content': 'Statins', 'is_correct': False},
                        {'content': 'Aspirin therapy', 'is_correct': False},
                        {'content': 'Lifestyle modifications', 'is_correct': True},
                        {'content': 'Blood pressure medications', 'is_correct': False}
                    ],
                    'explanation': 'Lifestyle modifications such as exercise, diet, and smoking cessation are the '
                                   'most effective methods for primary prevention of cardiovascular disease.'
                },
                {
                    'content': 'Which screening test is recommended for colorectal cancer in individuals aged 50 and above?',
                    'options': [
                        {'content': 'Fecal occult blood test (FOBT)', 'is_correct': False},
                        {'content': 'CT colonography', 'is_correct': False},
                        {'content': 'Sigmoidoscopy', 'is_correct': False},
                        {'content': 'Colonoscopy', 'is_correct': True}
                    ],
                    'explanation': 'Colonoscopy is the gold standard screening test for colorectal cancer in '
                                   'individuals aged 50 and above.'
                },
                {
                    'content': 'Which vaccine is contraindicated in immunocompromised patients?',
                    'options': [
                        {'content': 'Live attenuated influenza vaccine', 'is_correct': True},
                        {'content': 'Inactivated influenza vaccine', 'is_correct': False},
                        {'content': 'Pneumococcal vaccine', 'is_correct': False},
                        {'content': 'Tdap vaccine', 'is_correct': False}
                    ],
                    'explanation': 'Live attenuated vaccines are contraindicated in immunocompromised patients due to '
                                   'the risk of vaccine-strain infection.'
                },
                {
                    'content': 'Which of the following is a primary prevention strategy for cardiovascular disease?',
                    'options': [
                        {'content': 'Lifestyle modifications (e.g., diet, exercise)', 'is_correct': True},
                        {'content': 'Statin therapy', 'is_correct': False},
                        {'content': 'Angioplasty', 'is_correct': False},
                        {'content': 'Coronary artery bypass grafting (CABG)', 'is_correct': False}
                    ],
                    'explanation': 'Primary prevention involves lifestyle changes to reduce the risk of developing cardiovascular disease.'
                },
                {
                    'content': 'What is the recommended age for the first dose of the HPV vaccine?',
                    'options': [
                        {'content': '15-16 years old', 'is_correct': False},
                        {'content': '5-6 years old', 'is_correct': False},
                        {'content': '11-12 years old', 'is_correct': True},
                        {'content': '18 years old', 'is_correct': False}
                    ],
                    'explanation': 'The HPV vaccine is recommended at age 11-12 to provide protection before any potential exposure to the virus.'
                },
                {
                    'content': 'What is the recommended first-line intervention for primary prevention of cardiovascular disease?',
                    'options': [
                        {'content': 'Aspirin therapy', 'is_correct': False},
                        {'content': 'Lifestyle modifications', 'is_correct': True},
                        {'content': 'Statin therapy', 'is_correct': False},
                        {'content': 'Beta blockers', 'is_correct': False}
                    ],
                    'explanation': 'Lifestyle modifications including diet, exercise, and smoking cessation are the '
                                   'cornerstone of primary cardiovascular disease prevention.'
                }
            ]
        },
    }
}


def create_quizzes(admin_user):
    """Create quizzes with updated question and option structure"""
    courses = [
        'anatomy', 'pharmacology', 'medicine', 'surgery', 'pediatrics', 'obstetrics',
        'emergency_medicine', 'psychiatry', 'radiology', 'pathology', 'preventive_medicine',
        'microbiology', 'hiv_aids_medicine', 'leadership_and_management', 'neonatology'
    ]

    professions = [
        'doctor', 'nurse', 'pharmacist', 'clinical_officer', 'medical_licentiate',
        'scientist', 'medical_student', 'nursing_student', 'clinical_officer_student',
        'pharmacy_student'
    ]
    quiz_content = create_quiz_content()

    for profession in professions:
        for course in courses:
            # Create quiz with profession-specific title and description
            quiz = Quiz(
                title=f'{course.replace("_", " ").title()} for {profession.replace("_", " ").title()}',
                course=course,
                profession=profession,
                time_limit=15,
                description=f'Comprehensive {course.replace("_", " ")} assessment for {profession.replace("_", " ")} professionals',
                created_by_id=admin_user.id,
                difficulty_level='intermediate',
                passing_score=60.0,
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