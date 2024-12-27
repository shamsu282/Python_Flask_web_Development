from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder="Templete")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class TODO(db.Model):
    Sr_no = db.Column(db.Integer, primary_key = True)
    Desc = db.Column(db.String(200),nullable=False)
    Rate = db.Column(db.Integer,nullable=False)
    Qty = db.Column(db.Integer,nullable=False)
    ItemType = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"{self.Sr_no}-{self.Desc}-{self.Rate}-{self.Qty}-{self.ItemType}"

with app.app_context():
    db.create_all()

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        desc = request.form["Desc"]
        rate = request.form["Rate"]
        qty  = request.form["Qty"]
        item_type = request.form["ItemType"]
        todo = TODO(Desc=desc,Rate=rate,Qty=qty,ItemType=item_type)
        db.session.add(todo)
        db.session.commit()
    allTodo = TODO.query.all()
    return render_template("index.html",allTodo=allTodo)


@app.route("/Sell")
def show():
    Data = TODO.query.all()
    return render_template('Sell.html',Data=Data)

@app.route("/Update/<int:Sr_no>",methods=["GET","POST"])
def update(Sr_no):
    if request.method == 'POST':
        desc = request.form["Desc"]
        rate = request.form["Rate"]
        qty  = request.form["Qty"]
        Data = TODO.query.filter_by(Sr_no=Sr_no).first()
        Data.Desc = desc
        Data.Rate = rate
        Data.Qty = qty
        db.session.add(Data)
        db.session.commit()
        return redirect("/")
    Data = TODO.query.filter_by(Sr_no=Sr_no).first()
    return render_template("Update.html",Data=Data)

@app.route("/delete/<int:Sr_no>")
def delete(Sr_no):
    delete = TODO.query.filter_by(Sr_no=Sr_no).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)

