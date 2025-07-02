from app import app


@app.route("/")
def index():
    return "hello world"


@app.route("/home")
def home():
    return "welcome to home"

