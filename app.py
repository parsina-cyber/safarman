from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

# app.secret_key = "amoo"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.db"
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class City(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.name
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
        return render_template("login.html")
    

@app.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
                
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("email", None)
        flash("You have been logged out!", "info")
    return redirect(url_for("login"))



#---------------------------------------------------------------------------



# @app.route('/', methods=['POST', 'GET'])
# def home_page():
#     if request.method == "POST":
#         city_name = request.form['name']
#         new_city = City(name=city_name)
#         print("new city = ", new_city)

#         try:
#             db.session.add(new_city)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "City cannot be submitted"
#     else:
#         cities_list = City.query.order_by(City._id).all()
#         return render_template('pages/home.html', cities=cities_list)

# @app.route('/delete/<int:id>')
# def city_delete_view(id):
#     city_obj = City.query.get_or_404(id)
#     try:
#         db.session.delete(city_obj)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return "You cannot delete this city!"

# @app.route('/detail/<int:id>', methods=['GET'])
# def city_detail_view(id):
#     city_obj = City.query.get_or_404(id)
#     return render_template('pages/city.html', city=city_obj)

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def city_update_view(id):
#     city_obj = City.query.get_or_404(id)
#     if request.method == "POST":
#         city_obj.name = request.form['name']
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'City cannot be updated'
#     return render_template('pages/city_update.html', city=city_obj)
    

if __name__ == '__main__':
    app.run(debug=True)

