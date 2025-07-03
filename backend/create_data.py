from .models import db, Admin, ServiceCategory, ServiceProfessional

if db.session.query(Admin).count() == 0:
    A = Admin(name = "admin" , email="admin@myapp.com" , password = "pass")
    db.session.add(A)
    db.session.commit()

if db.session.query(ServiceCategory).count() == 0:
    hc = ServiceCategory(name="Home Cleaning")
    db.session.add(hc)
    g= ServiceCategory(name="Gardening")
    db.session.add(g)
    e = ServiceCategory(name="Electrician")
    db.session.add(e)
    db.session.commit()


if db.session.query(ServiceProfessional).count()==0:
    r  = ServiceProfessional(name="Ram" , email="Ram@myapp.com" , password="pass" , city = "Jaipur" , cat_id = 2 , phone="9999999999")
    db.session.add(r)

    s  = ServiceProfessional(name="Shyam" , email="shyam@myapp.com" , password="pass" , city = "Delhi" , cat_id = 2 , phone="9999999999")
    db.session.add(s)

    p  = ServiceProfessional(name="Prakash" , email="Prakash@myapp.com" , password="pass" , city = "Indore" , cat_id = 3 , phone="9999999999")
    db.session.add(p)
    db.session.commit()


