import os
from werkzeug.security import generate_password_hash
from .extensions import db
from .models import FAQ, Department, Course, Announcement, SemanticEntity, SemanticRelationship

FAQS = [
("What is the minimum attendance requirement?", "For this demonstration portal, the sample attendance requirement is 75%. This is illustrative only; check your institution's official academic regulations for the binding rule.", "Attendance", "attendance, lectures, eligibility, examination"),
("How do I apply for admission?", "The sample admission process is: review the programme eligibility, complete the application form, upload the required documents, and follow the admissions office instructions. Exact dates and procedures must be confirmed with the official admissions office.", "Admissions", "admission, apply, application, eligibility, documents"),
("Which documents are generally required for admission?", "Commonly requested documents may include previous qualifying examination marksheets, identity proof, photographs and applicable category or transfer certificates. Requirements vary by institution and programme; confirm the official checklist.", "Admissions", "documents, marksheet, certificate, admission"),
("How can I contact the examination department?", "Please contact the examination office through the official contact details published by your institution. This demo portal does not contain verified staff contact information.", "Examinations", "exam, examination, controller, result, hall ticket"),
("How can I apply for a scholarship?", "Start by checking the scholarship eligibility criteria, application window and required documents. The college scholarship office or the relevant government scholarship portal can confirm current schemes and deadlines.", "Scholarships", "scholarship, financial aid, fees, funding"),
("Where can I find information about placements?", "Placement information is usually published by the training and placement cell, including eligibility, company visits, preparation sessions and placement statistics. Contact the official placement cell for current details.", "Placements", "placement, internship, jobs, companies, career"),
("What are the library facilities?", "A college library may provide textbooks, reference material, journals, digital resources and study spaces. Please check the institution's official library rules for borrowing limits and opening hours.", "Facilities", "library, books, journals, reading room"),
("How do I pay my college fees?", "Use only the payment methods and deadlines communicated through the official college fee portal or accounts office. Never share your banking password, OTP or card PIN with anyone.", "Fees", "fees, payment, accounts, tuition"),
("Which engineering departments are available?", "This demonstration portal lists Computer Engineering, Information Technology, Electronics and Telecommunication, and Mechanical Engineering as sample departments. Replace these with verified institutional offerings.", "Academics", "department, branch, engineering, courses"),
("How can I report an issue on campus?", "For a campus concern, contact the relevant department office or student support team. For urgent safety matters, contact campus security or local emergency services.", "Student Support", "complaint, issue, campus, help, support"),
("What is the process for submitting assignments?", "Follow the submission instructions shared by your subject faculty or learning management system. Check the required format, deadline and submission confirmation. This portal does not know individual course deadlines.", "Academics", "assignment, submit, deadline, coursework"),
("Does the college provide internships?", "Internship opportunities may be shared through the training and placement cell, department notices and approved career platforms. Verify eligibility, dates and employer details before applying.", "Placements", "internship, training, placement, career"),
]

def seed_database():
    if FAQ.query.count() == 0:
        for q, a, c, k in FAQS:
            db.session.add(FAQ(question=q, answer=a, category=c, keywords=k))
    if Department.query.count() == 0:
        departments = [
            ("Computer Engineering", "Computing, software systems and intelligent applications.", "B.Tech Computer Engineering"),
            ("Information Technology", "Information systems, networks and digital platforms.", "B.Tech Information Technology"),
            ("Electronics & Telecommunication", "Electronics, communication systems and embedded technologies.", "B.Tech E&TC"),
            ("Mechanical Engineering", "Design, manufacturing and mechanical systems.", "B.Tech Mechanical Engineering"),
        ]
        for name, desc, programs in departments:
            d = Department(name=name, description=desc, programs=programs)
            db.session.add(d)
            db.session.flush()
            db.session.add(Course(name=programs, level="Undergraduate", duration="4 years", department_id=d.id))
    if Announcement.query.count() == 0:
        db.session.add_all([
            Announcement(title="Welcome to the CampusIQ demo portal", body="Explore academic information and try the AI assistant. Content on this demonstration site is illustrative.", date="2026-11-26", tag="Notice"),
            Announcement(title="Student support information", body="For official deadlines, fees and regulations, always refer to verified college communications.", date="2026-11-20", tag="Student Support"),
            Announcement(title="Career development resources", body="Connect with your department and placement cell for current workshops and opportunities.", date="2026-11-14", tag="Careers"),
        ])
    if SemanticEntity.query.count() == 0:
        names = [
            ("College", "Institution", "The educational institution."),
            ("Admissions", "Process", "Applying to an academic programme."),
            ("Student", "Person", "A person enrolled at the institution."),
            ("Department", "AcademicUnit", "An academic department."),
            ("Course", "Programme", "A programme or course of study."),
            ("Faculty", "Person", "Academic teaching staff."),
            ("Examination", "AcademicProcess", "Assessment and examinations."),
            ("Attendance", "AcademicPolicy", "Student attendance requirements."),
            ("Assignment", "AcademicActivity", "Coursework submitted by students."),
            ("Scholarship", "FinancialAid", "Financial support for eligible students."),
            ("Placement", "CareerService", "Career and recruitment support."),
            ("Library", "Facility", "Learning resources and study facilities."),
        ]
        entities = {}
        for name, typ, desc in names:
            e = SemanticEntity(name=name, entity_type=typ, description=desc)
            db.session.add(e)
            db.session.flush()
            entities[name] = e
        edges = [
            ("College", "has", "Department"), ("Department", "offers", "Course"),
            ("Department", "has", "Faculty"), ("Student", "enrols in", "Course"),
            ("Student", "attends", "Attendance"), ("Student", "submits", "Assignment"),
            ("Course", "has", "Examination"), ("Student", "appears in", "Examination"),
            ("Student", "may apply for", "Scholarship"), ("College", "provides", "Library"),
            ("College", "supports", "Placement"), ("Admissions", "admits", "Student"),
        ]
        for s, r, t in edges:
            db.session.add(SemanticRelationship(source_id=entities[s].id, relation=r, target_id=entities[t].id))
    db.session.commit()
