from flask import redirect,render_template,request,flash
from flask_smorest import Blueprint, abort
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView

from db import db
from Models.models import Influencer, Sponsor, Campaign,User
# from Schemas.schemas import RegisterSchema, LoginSchema

blp = Blueprint("Auth", __name__, description="Authentication APIs")

@blp.route('/register')
class Register(MethodView):
    def get(self):
        return render_template('register.html')
    
    def post(self):
        role = request.form.get('role')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if role == 'influencer':
            new_user = Influencer(email=email, name=name, password=hashed_password)
        elif role == 'sponsor':
            new_user = Sponsor(email=email, name=name, password=hashed_password)
        elif role == 'admin':
            new_user = User(email=email,password=hashed_password,type="admin")
        else:
            flash("Invalid details",category="error")
            abort(400, message="Invalid role specified")

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="A user with that email already exists")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        # return {"message": f"{role.capitalize()} registered successfully!"}
        return redirect('/login')

@blp.route('/login')
class Login(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        print(email)
        # admin = User.query.filter_by(type="admin").first()
        user = Influencer.query.filter_by(email=email).first() or Sponsor.query.filter_by(email=email).first()
        print(password)
        if email == "admin@123" and password=="1045":
            return redirect('/admin')

        if not user or not check_password_hash(user.password,password):
            flash("check your credentials",category="error")
            return redirect('/login')
            # flask.alert("Invalid credentials")
            # abort(401, message="Invalid credentials")
        login_user(user)
        if user.type == "sponsor" :
            return redirect("/sponsor")
        elif user.type == "influencer" :
            return redirect("/influencer")
        # elif admin.type == "admin":
        #     return redirect("/admin")
        else:
            flash("Invalid user role!",category="error")
    
@blp.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

@blp.route("/admin")
def index():
    inf = User.query.filter_by(type="influencer").count()
    sp = User.query.filter_by(type="sponsor").count()
    sport = Influencer.query.filter_by(niche="Sport").count()
    an = Influencer.query.filter_by(niche="Animal").count()
    tr = Influencer.query.filter_by(niche = "Travel").count()
    food = Influencer.query.filter_by(niche="Food").count()
    ent = Influencer.query.filter_by(niche="Entertainment").count()
    ot = Influencer.query.filter_by(niche="Others").count()
    users = User.query.all() 
    cam = Campaign.query.all()
    print(inf,sp)
    return render_template("admin.html",inf = inf,sp=sp,sport=sport,an =an,tr=tr,food=food,ot=ot,ent=ent,total=inf+sp,users=users,tc =sport+an+tr+food+ent+ot,cam=cam)