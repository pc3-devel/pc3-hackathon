from flask import session
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            #bounce back for unauthenticated users
            return json.dumps({"status": False, "reason": "requires authentication"}), 401
        else:
            kwargs["team"] = session["username"]
            return f(*args, **kwargs)
    return wrapper
