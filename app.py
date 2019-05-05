from flask import Flask, render_template, url_for, request, redirect
import pymongo
from authorize import Auth
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://seanbrhn3:45305006@goodneighbordb-1pr3o.mongodb.net/test?retryWrites=true")
db = client.test
trans = Auth()
# trans.deleteAll()
# trans.deletePool()
# db.votes.remove()
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
    if request.method == "POST":
        print("LOOK HERE",request.form)
        trans.creds(request.form['account_number'],request.form['exp_date'],"100.00")
        db.userInfo.insert_one({
            "businessName": request.form['business_name'],
            'account_number': request.form['account_number'],
            'exp_date': request.form['exp_date'],
            'description': request.form['description'],
            'password': request.form['password'],
            'amount_given': 100.00
        })
        if "pool" not in db.list_collection_names():
            db.pool.insert_one({
                "amount_given":100
            })
            return redirect(url_for("companies"))
        else:
            value = 0
            for i in db.pool.find():
                value = i['amount_given']
            test = value+100
            db.pool.insert_one(
                {"amount_given":test}
            )
        return redirect(url_for("companies"))
    return render_template("register.html")

@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method == "POST":
        print(request.form)
        foundUserAndPassword = False
        for i in db.userInfo.find():
            if i["businessName"] == request.form['business_name'] and i['password'] == request.form['password']:
                return redirect(url_for("relief",company=request.form['business_name']))
    return render_template("signin.html")

@app.route('/companies')
def companies():
    return render_template("companies.html",comps=db.userInfo.find(),pool=trans.pool())

@app.route('/relief/<company>',methods=["GET","POST"])
def relief(company):
    company1 = db.userInfo.find({"businessName":company})
    if request.method == "POST":
        print(request.form.keys())
        values = {}
        values[company] = company
        reasons = []
        for i in request.form.keys():
            reasons.append(request.form[i])
        values['reasons'] = reasons
        values["votes"] = 0
        db.vote.insert_one(values)
        return redirect(url_for('votes',comp=company))
    return render_template("relief.html",company=company1)

@app.route('/form/<request>',methods=["GET","POST"])
def form(request):
    return render_template("form.html",request=request)

@app.route('/votes/<comp>',methods=["GET","POST"])
def votes(comp):
    return render_template("votes.html",values=db.vote.find())

if __name__ == "__main__":
    app.run(debug=True)
