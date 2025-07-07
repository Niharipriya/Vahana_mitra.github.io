from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def base_page():
    return render_template("home_page.html")

if __name__ == "__main__":
    app.run(debug=True)
