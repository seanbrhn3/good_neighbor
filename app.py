from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        if "register" in request.form:
            return redirect(url_for("register"))
        if "signin" in request.form:
            return redirect(url_for("signin"))
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    return render_template("register.html")

@app.route("/signin",methods=["GET","POST"])
def signin():
    return render_template("signin.html")

if __name__ == "__main__":
    app.run(debug=True)
