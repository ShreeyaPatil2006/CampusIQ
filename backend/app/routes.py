import os, uuid
from functools import wraps
from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db
from .models import FAQ, Department, Course, Announcement, SemanticEntity, SemanticRelationship, ChatSession, ChatMessage, UnansweredQuery
from .ai.retrieval import retrieve
from .ai.intent import classify_intent
from .ai.knowledge_graph import related_context
from .ai.rag import generate_answer

api = Blueprint("api", __name__)

def serialize_faq(f):
    return {"id": f.id, "question": f.question, "answer": f.answer, "category": f.category,
            "keywords": f.keywords or "", "source": f.source}

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.replace("Bearer ", "", 1) if header.startswith("Bearer ") else ""
        try:
            payload = jwt.decode(token, os.getenv("FLASK_SECRET_KEY", "local-development-only-change-me"), algorithms=["HS256"])
            if payload.get("role") != "admin":
                raise ValueError("Not an admin")
        except Exception:
            return jsonify({"error": "Authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper

@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "CampusIQ API"})

@api.get("/content")
def content():
    return jsonify({
        "college": {"name": "Northstar Institute of Technology", "tagline": "Learn. Build. Lead.",
                    "description": "A demonstration engineering college portal showcasing academic information and student support."},
        "departments": [{"id": d.id, "name": d.name, "description": d.description, "programs": d.programs} for d in Department.query.all()],
        "courses": [{"id": c.id, "name": c.name, "level": c.level, "duration": c.duration} for c in Course.query.all()],
        "announcements": [{"id": a.id, "title": a.title, "body": a.body, "date": a.date, "tag": a.tag} for a in Announcement.query.order_by(Announcement.id.desc()).all()]
    })

@api.get("/faqs")
def faqs():
    return jsonify([serialize_faq(f) for f in FAQ.query.order_by(FAQ.category, FAQ.id).all()])

@api.get("/departments")
def departments():
    return jsonify([{"id": d.id, "name": d.name, "description": d.description, "programs": d.programs} for d in Department.query.all()])

@api.get("/courses")
def courses():
    return jsonify([{"id": c.id, "name": c.name, "level": c.level, "duration": c.duration} for c in Course.query.all()])

@api.get("/announcements")
def announcements():
    return jsonify([{"id": a.id, "title": a.title, "body": a.body, "date": a.date, "tag": a.tag} for a in Announcement.query.order_by(Announcement.id.desc()).all()])

@api.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please enter a question."}), 400
    if len(message) > 1500:
        return jsonify({"error": "Question is too long (maximum 1500 characters)."}), 400
    session_id = data.get("session_id") or str(uuid.uuid4())
    session = db.session.get(ChatSession, session_id)
    if not session:
        session = ChatSession(id=session_id)
        db.session.add(session)
    history_rows = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.id.desc()).limit(8).all()
    history = [{"role": m.role, "content": m.content} for m in reversed(history_rows)]
    intent, intent_confidence = classify_intent(message)
    results = retrieve(message)
    graph = related_context(message, intent)
    answer, mode = generate_answer(message, results, graph, history)
    db.session.add(ChatMessage(session_id=session_id, role="user", content=message))
    db.session.add(ChatMessage(session_id=session_id, role="assistant", content=answer))
    if not results or results[0]["score"] < 0.16:
        db.session.add(UnansweredQuery(question=message, intent=intent))
    db.session.commit()
    sources = [{"question": r["question"], "category": r["category"], "source": r["source"], "relevance": round(r["score"], 3)} for r in results[:3] if r["score"] >= 0.10]
    return jsonify({"answer": answer, "session_id": session_id, "intent": intent,
                    "intent_confidence": round(intent_confidence, 3), "mode": mode,
                    "sources": sources, "related_concepts": graph[:6]})

@api.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    email = os.getenv("ADMIN_EMAIL", "admin@campusiq.demo")
    password = os.getenv("ADMIN_PASSWORD", "CampusIQ@123")
    if data.get("email") != email or data.get("password") != password:
        return jsonify({"error": "Invalid email or password"}), 401
    token = jwt.encode({"role": "admin", "exp": datetime.now(timezone.utc) + timedelta(hours=8)},
                       os.getenv("FLASK_SECRET_KEY", "local-development-only-change-me"), algorithm="HS256")
    return jsonify({"token": token, "email": email})

@api.get("/admin/faqs")
@token_required
def admin_faqs():
    return jsonify([serialize_faq(f) for f in FAQ.query.order_by(FAQ.id.desc()).all()])

@api.post("/admin/faqs")
@token_required
def create_faq():
    d = request.get_json(silent=True) or {}
    if not d.get("question") or not d.get("answer"):
        return jsonify({"error": "Question and answer are required"}), 400
    f = FAQ(question=d["question"].strip(), answer=d["answer"].strip(),
            category=d.get("category", "General"), keywords=d.get("keywords", ""),
            source=d.get("source", "Admin-managed knowledge base"))
    db.session.add(f); db.session.commit()
    return jsonify(serialize_faq(f)), 201

@api.put("/admin/faqs/<int:faq_id>")
@token_required
def update_faq(faq_id):
    f = db.session.get(FAQ, faq_id)
    if not f: return jsonify({"error": "FAQ not found"}), 404
    d = request.get_json(silent=True) or {}
    for key in ("question", "answer", "category", "keywords", "source"):
        if key in d: setattr(f, key, d[key])
    db.session.commit()
    return jsonify(serialize_faq(f))

@api.delete("/admin/faqs/<int:faq_id>")
@token_required
def delete_faq(faq_id):
    f = db.session.get(FAQ, faq_id)
    if not f: return jsonify({"error": "FAQ not found"}), 404
    db.session.delete(f); db.session.commit()
    return jsonify({"success": True})

@api.get("/admin/announcements")
@token_required
def admin_announcements():
    return announcements()

@api.post("/admin/announcements")
@token_required
def create_announcement():
    d = request.get_json(silent=True) or {}
    if not d.get("title") or not d.get("body"):
        return jsonify({"error": "Title and body are required"}), 400
    a = Announcement(title=d["title"], body=d["body"], date=d.get("date", datetime.now().strftime("%Y-%m-%d")), tag=d.get("tag", "Notice"))
    db.session.add(a); db.session.commit()
    return jsonify({"id": a.id, "title": a.title, "body": a.body, "date": a.date, "tag": a.tag}), 201

@api.get("/admin/entities")
@token_required
def admin_entities():
    return jsonify([{"id": e.id, "name": e.name, "type": e.entity_type, "description": e.description} for e in SemanticEntity.query.all()])

@api.post("/admin/entities")
@token_required
def create_entity():
    d = request.get_json(silent=True) or {}
    if not d.get("name"): return jsonify({"error": "Entity name is required"}), 400
    e = SemanticEntity(name=d["name"], entity_type=d.get("type", "Concept"), description=d.get("description", ""))
    db.session.add(e)
    try: db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Entity already exists or could not be saved"}), 409
    return jsonify({"id": e.id, "name": e.name}), 201

@api.post("/admin/relationships")
@token_required
def create_relationship():
    d = request.get_json(silent=True) or {}
    source, target = db.session.get(SemanticEntity, d.get("source_id")), db.session.get(SemanticEntity, d.get("target_id"))
    if not source or not target or not d.get("relation"):
        return jsonify({"error": "Valid source, target and relation are required"}), 400
    edge = SemanticRelationship(source_id=source.id, target_id=target.id, relation=d["relation"])
    db.session.add(edge); db.session.commit()
    return jsonify({"id": edge.id}), 201

@api.get("/admin/unanswered-queries")
@token_required
def unanswered():
    rows = UnansweredQuery.query.order_by(UnansweredQuery.id.desc()).limit(100).all()
    return jsonify([{"id": r.id, "question": r.question, "intent": r.intent, "created_at": r.created_at.isoformat()} for r in rows])
