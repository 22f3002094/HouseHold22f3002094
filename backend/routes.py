from app import app
from flask import render_template,request ,redirect,flash
from .models import db, Admin , ServiceCategory, User , ServiceProfessional 
from flask_login import login_user , login_required , current_user
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import and_

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
                
                new_prof = ServiceProfessional(name=p_name , email=p_email , password = p_password,status="Requested" ,
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
                
                new_cust= User(name=c_name , email=c_email , password =c_password,status="Active" , 
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
        u = db.session.query(Admin).filter_by(email=email).first() or \
            db.session.query(User).filter_by(email=email).first() or \
                db.session.query(ServiceProfessional).filter_by(email=email).first()

        if u:
            if u.password==password:
                if isinstance(u , Admin):
                    login_user(u)
                    return redirect(f"/admin/dashboard" , )
                elif isinstance(u ,User ):
                    login_user(u)
                    return redirect(f"/customer/dashboard")
                elif isinstance(u , ServiceProfessional):
                    login_user(u)
                    return redirect(f"/professional/dashboard")
            else:
                flash("Incorrect password")
                return redirect("/login")
        else:
            flash("Email doesn't exist")
            return redirect("/login")


        ####2nd logic

        # role = request.form.get("role")

        # if role == "admin":
        #     ad = db.session.query(Admin).filter_by(email = email).first()
        #     if ad:
        #         if ad.password == password:
        #             return redirect("/admin/dashboard")
        #         else:
        #             return "incorrect password"
        #     else:
        #         return "email doesn't exist for admin"
        # elif role == "customer":
        #     cust = db.session.query(User).filter_by(email = email).first()
        #     if cust:
        #         if cust.password == password:
        #             return redirect("/customer/dashboard")
        #         else:
        #             return "incorrect password"
        #     else:
        #         return "email doesn't exist for customer"
        # elif role == "professional":
        #     prof = db.session.query(ServiceProfessional).filter_by(email = email).first()
        #     if prof:
        #         if prof.password == password:
        #             return redirect("/professional/dashboard")
        #         else:
        #             return "incorrect password"
        #     else:
        #         return "email doesn't exist for professional"
            
        
        




@app.route("/admin/dashboard")
@login_required
def admin_dash():
    all_cats = db.session.query(ServiceCategory).all()
    active_prof = db.session.query(ServiceProfessional).filter_by(status="Active").all()
    requested_prof = db.session.query(ServiceProfessional).filter_by(status="Requested").all()
    flagged_prof = db.session.query(ServiceProfessional).filter_by(status="Flagged").all()
    active_cust = db.session.query(User).filter_by(status="Active").all()
    flagged_cust = db.session.query(User).filter_by(status="Flagged").all()

    return render_template("/admin/dashboard.html", all_cats = all_cats , active_prof = active_prof , 
                           requested_prof=requested_prof, flagged_prof=flagged_prof ,
                           active_cust=active_cust,flagged_cust=flagged_cust)



@app.route("/customer/dashboard")
@login_required
def cust_dash():

    return render_template("/customer/dashboard.html")

@app.route("/professional/dashboard")
@login_required
def prof_dash():
    
    return render_template("/professional/dashboard.html" , current_prof = current_user)



@app.route("/professional/stats")
@login_required
def prof_stats():
    return f"Welcome to {current_user.name}  stats"




@app.route("/category" , methods=["POST"])
def category():
    if request.args.get("task") =="create":
        cat_name = request.form.get("cat_name")
        
        cat = db.session.query(ServiceCategory).filter_by(name=cat_name).first()
        if cat : 
            flash("Category already exist")
            return redirect("/admin/dashboard")
        else:
            new_cat = ServiceCategory(name=cat_name)
            db.session.add(new_cat)
            db.session.commit()
            flash("Category Created.")
            return redirect("/admin/dashboard")
    elif request.args.get("task") =="edit":
        cat_name = request.form.get("cat_name")
        cat = db.session.query(ServiceCategory).filter_by(name=cat_name).first()
        if cat:
            cat.name  = cat_name
            db.session.commit()
            flash("Category is updated")
            return redirect("/admin/dashboard")
        else:
            flash("category doen't exist")
            return redirect("/admin/dashboard")
        

        

@app.route("/professional" , methods=["POST"])
def professional():
    if request.args.get("task") == "flag":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status = "Flagged"
            db.session.commit()
            flash(f"{prof.name} is flagged")
            return redirect("/admin/dashboard")
    elif request.args.get("task") == "unflag":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status = "Active"
            db.session.commit()
            flash(f"{prof.name} is unflagged")
            return redirect("/admin/dashboard")
    elif request.args.get("task") == "accept":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status = "Active"
            db.session.commit()
            flash(f"{prof.name}'s request is accepted")
            return redirect("/admin/dashboard")
    elif request.args.get("task") == "reject":
        prof_id = request.args.get("prof_id")
        prof = db.session.query(ServiceProfessional).filter_by(id = prof_id).first()
        if prof:
            prof.status = "Rejected"
            db.session.commit()
            flash(f"{prof.name}'s request is Rejected")
            return redirect("/admin/dashboard")




@app.route("/customer" , methods=["POST"])
def customer():
    if request.args.get("task") == "flag":
        cust_id = request.args.get("cust_id")
        cust = db.session.query(User).filter_by(id = cust_id).first()
        if cust:
            cust.status = "Flagged"
            db.session.commit()
            flash(f"{cust.name} is flagged")
            return redirect("/admin/dashboard")
    elif request.args.get("task") == "unflag":
        cust_id = request.args.get("cust_id")
        cust = db.session.query(User).filter_by(id = cust_id).first()
        if cust:
            cust.status = "Active"
            db.session.commit()
            flash(f"{cust.name} is unflagged")
            return redirect("/admin/dashboard")



   
#dummy praking spot booking route
# @app.route("/booking" , methods=["POST"])
# def booking():
#     if request.args.get("p_lot_id"):
#         p_id = request.args.get("p_lot_id")
#         spot = db.session.query(ParkingSpots).filter(and_(  
#                                                         ParkingSpots.parkinglot_id == p_id ,
#                                                        ParkingSpots.status == "available" )).first()
        
#         if spot:
        
#             book = Booking(p_id = P_id , spot_id = spot.id , user_id = current_user.id , booking.status="booked" )
#             db.session.add(book)
#             db.session.commit()
#             spot.status = "occupied"
#             db.session.commit()
#             flash("booked")
#             return redirect("/customer/dashboared")

#         else:
#             flash("not")

    