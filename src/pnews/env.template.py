from .config import __version__


class env:
    client_id = "CHANGE_ME"
    client_secret = "CHANGE_ME"
    username = "CHANGE_ME"
    password = "CHANGE_ME"
    app_name = "CHANGE_ME"
    user_agent = f"web:{app_name}:v{__version__} (by /u/{username})"
