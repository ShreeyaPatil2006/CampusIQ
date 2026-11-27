from datetime import datetime, timezone
from .extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False, default="General")
    keywords = db.Column(db.Text, default="")
    source = db.Column(db.String(300), default="CampusIQ demo knowledge base")
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    programs = db.Column(db.Text, default="")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    level = db.Column(db.String(80), default="Undergraduate")
    duration = db.Column(db.String(80), default="4 years")
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(40), nullable=False)
    tag = db.Column(db.String(80), default="Campus")

class SemanticEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False, unique=True)
    entity_type = db.Column(db.String(100), default="Concept")
    description = db.Column(db.Text, default="")

class SemanticRelationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("semantic_entity.id"), nullable=False)
    relation = db.Column(db.String(120), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey("semantic_entity.id"), nullable=False)
    source = db.relationship("SemanticEntity", foreign_keys=[source_id])
    target = db.relationship("SemanticEntity", foreign_keys=[target_id])

class ChatSession(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(80), db.ForeignKey("chat_session.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

class UnansweredQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(100), default="Unknown")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
