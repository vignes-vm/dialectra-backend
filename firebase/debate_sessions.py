from firebase.firebase_config import db

def create_debate_session(session_data):
    doc_ref = db.collection("debate_sessions").document(session_data["id"])
    doc_ref.set(session_data)
    return f"Debate session '{session_data['id']}' created."

def get_debate_session(session_id):
    doc_ref = db.collection("debate_sessions").document(session_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def update_debate_session(session_id, update_data):
    doc_ref = db.collection("debate_sessions").document(session_id)
    doc_ref.update(update_data)
    return f"Session '{session_id}' updated."

def delete_debate_session(session_id):
    db.collection("debate_sessions").document(session_id).delete()
    return f"Session '{session_id}' deleted."
