from ..models import SemanticEntity, SemanticRelationship

def related_context(query, category=None, limit=12):
    terms = set(query.lower().replace("?", " ").split())
    entities = SemanticEntity.query.all()
    matched = [e for e in entities if e.name.lower() in terms or any(t in e.name.lower() for t in terms if len(t) > 3)]
    if category:
        cat = next((e for e in entities if e.name.lower() == category.lower()), None)
        if cat and cat not in matched:
            matched.append(cat)
    if not matched:
        matched = [e for e in entities if e.name in ("College", "Student")][:1]
    ids = {e.id for e in matched}
    edges = SemanticRelationship.query.filter(
        (SemanticRelationship.source_id.in_(ids)) | (SemanticRelationship.target_id.in_(ids))
    ).limit(limit).all() if ids else []
    return [
        f"{edge.source.name} --{edge.relation}--> {edge.target.name}"
        for edge in edges
    ]
