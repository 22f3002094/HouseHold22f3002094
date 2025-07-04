from app import app
from flask import render_template,request ,redirect
from .models import db, Admin , ServiceCategory, User , ServiceProfessional 

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register" , methods=["GET" , "POST"])
def register():
    print("hello")
    if request.method =="GET":
        if request.args.get("u_type") == "customer":
            return render_template("/customer/register.html ")
        elif request.args.get("u_type") =="professional":
            cats = db.session.query(ServiceCategory).all()
            return render_template("/professional/register.html" , categories = cats)
    elif request.method=="POST":
        if request.args.get("u_type") == "professional":
            p_name =request.form.get("prof_name")
            p_email =request.form.get("prof_email")
            p_password =request.form.get("prof_password")
            p_city =request.form.get("prof_city")
            
            p_phone =request.form.get("prof_phone")
            p_cat = request.form.get("prof_cat")
            
            prof = db.session.query(ServiceProfessional).filter_by(email=p_email).first()
            if prof:
                return "email already exist"
            else:
                
                new_prof = ServiceProfessional(name=p_name , email=p_email , password = p_password,
                                               city = p_city , phone = p_phone , cat_id = p_cat )
                db.session.add(new_prof)
                db.session.commit()
                return redirect("/login")
        elif request.args.get("u_type") =="customer":
            c_name =request.form.get("c_name")
            c_email =request.form.get("c_email")
            c_password =request.form.get("c_password")
            c_city =request.form.get("c_city")
            
            c_phone =request.form.get("c_phone")
            c_address = request.form.get("c_address")
            
            cust= db.session.query(User).filter_by(email=c_email).first()
            if cust:
                return "email already exist"
            else:
                
                new_cust= User(name=c_name , email=c_email , password =c_password,
                                               city = c_city , phone = c_phone , address=c_address )
                db.session.add(new_cust)
                db.session.commit()
                return redirect("/login")

            
        

            






@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # 1st Logic
        # u = db.session.query(Admin).filter_by(email=email).first() or \
        #     db.session.query(User).filter_by(email=email).first() or \
        #         db.session.query(ServiceProfessional).filter_by(email=email).first()

        # if u:
        #     if u.password==password:
        #         if isinstance(u , Admin):
        #             return redirect("/admin/dashboard")
        #         elif isinstance(u ,User ):
        #             return redirect("/customer/dashboard")
        #         elif isinstance(u , ServiceProfessional):
        #             return redirect("/professional/dashboard")
        #     else:
        #         return "incorrect password"
        # else:
        #     return "email doesn't exist"


        ####2nd logic

        role = request.form.get("role")

        if role == "admin":
            ad = db.session.query(Admin).filter_by(email = email).first()
            if ad:
                if ad.password == password:
                    return redirect("/admin/dashboard")
                else:
                    return "incorrect password"
            else:
                return "email doesn't exist for admin"
        elif role == "customer":
            cust = db.session.query(User).filter_by(email = email).first()
            if cust:
                if cust.password == password:
                    return redirect("/customer/dashboard")
                else:
                    return "incorrect password"
            else:
                return "email doesn't exist for customer"
        elif role == "professional":
            prof = db.session.query(ServiceProfessional).filter_by(email = email).first()
            if prof:
                if prof.password == password:
                    return redirect("/professional/dashboard")
                else:
                    return "incorrect password"
            else:
                return "email doesn't exist for professional"
            
        
        




@app.route("/admin/dashboard")
def admin_dash():
    return "welcome to admin"


@app.route("/customer/dashboard")
def cust_dash():
    return "welcome to customer"

@app.route("/professional/dashboard")
def prof_dash():
    return "welcome to professional"

