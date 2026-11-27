from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

TRAINING = [
("attendance minimum attendance lectures shortage exam eligibility", "Attendance"),
("admission apply application eligibility documents enrolment", "Admissions"),
("exam examination hall ticket result timetable assessment", "Examinations"),
("fee fees tuition payment accounts receipt", "Fees"),
("scholarship financial aid funding grant", "Scholarships"),
("placement internship job career company recruitment", "Placements"),
("library books journals reading room resources", "Facilities"),
("course branch department faculty academics syllabus", "Academics"),
("assignment submit deadline coursework practical", "Academics"),
("complaint help issue support campus", "Student Support"),
]

_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
_x = _vectorizer.fit_transform([x for x, _ in TRAINING])
_y = [y for _, y in TRAINING]
_classifier = LogisticRegression(max_iter=500).fit(_x, _y)

def classify_intent(text):
    probabilities = _classifier.predict_proba(_vectorizer.transform([text]))[0]
    idx = probabilities.argmax()
    confidence = float(probabilities[idx])
    return (_classifier.classes_[idx] if confidence >= 0.18 else "General"), confidence
