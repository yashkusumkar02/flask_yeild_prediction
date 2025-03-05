from flask import Flask, render_template
from api.routes import yield_prediction

app = Flask(__name__)

# Register API Routes
app.register_blueprint(yield_prediction)

@app.route("/")
def home():
    return render_template("index.html")  # Render UI

if __name__ == '__main__':
    app.run(debug=True)
