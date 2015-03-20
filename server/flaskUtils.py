from flask import session

def requires_auth(f):
    def wrapper(*args, **kwargs):
        if "username" not in session:
        #bounce back for unauthenticated users
            return json.dumps({"status":False, "message":"You must be authenticated to do that!"})
        else:
            kwargs['team'] = session["username"]
            return f(*args, **kwargs)
    return wrapper
