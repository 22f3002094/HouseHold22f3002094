from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Admin(db.Model , UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True )
    name = db.Column(db.String  , nullable = False)
    email = db.Column(db.String , unique =True , nullable=False)
    password = db.Column(db.String , nullable= False)
    def get_id(self):
        return self.email

class ServiceCategory(db.Model):
    __tablename__  = "category"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True )
    name = db.Column(db.String  ,unique=True, nullable = False)
    professionals= db.relationship("ServiceProfessional" , backref="category" )

    
class User(db.Model , UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True )
    name = db.Column(db.String  , nullable = False)
    email = db.Column(db.String , unique =True , nullable=False)
    password = db.Column(db.String , nullable= False)
    address = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable=False)
    phone = db.Column(db.String , nullable = False)
    created_bookings= db.relationship("Booking" , backref="user" )
    def get_id(self):
        return self.email


class ServiceProfessional(db.Model , UserMixin):
    __tablename__ = "professional"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True )
    name = db.Column(db.String  , nullable = False)
    email = db.Column(db.String , unique =True , nullable=False)
    password = db.Column(db.String , nullable= False)
    city = db.Column(db.String, nullable=False)
    phone = db.Column(db.String , nullable = False)
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    packages= db.relationship("ServicePackage" , backref="professional" )
    recieved_bookings= db.relationship("Booking" , backref="professional" )
    def get_id(self):
        return self.email
    


class ServicePackage(db.Model):
    __tablename__ = "package"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True)
    name = db.Column(db.String  ,unique=True, nullable = False)
    price = db.Column(db.Integer , nullable=False)
    prof_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    associate_bookings= db.relationship("Booking" , backref="package" )


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer , primary_key = True , autoincrement=True)
    pack_id = db.Column(db.Integer, db.ForeignKey("package.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prof_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)
    date = db.Column(db.String,nullable =False )
    time = db.Column(db.String,nullable =False ) 
    status = db.Column(db.String, nullable=False)






 