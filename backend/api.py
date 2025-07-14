from flask_restful import Resource , Api,request
from .models import *

from flask_login import login_required
api = Api()


class CategoryResource(Resource):
    def get(self):
        all_cats = db.session.query(ServiceCategory).all()
        cats = []
        for cat in all_cats:
            cats.append({"cat_id" : cat.id , "cat_name" : cat.name})

        return cats
    def post(self):
        cat_name = request.form.get("cat_name")
        cat  = db.session.query(ServiceCategory).filter_by(name=cat_name).first()
        if cat:
            return {"message" :"category already exist"} , 409
        else:
            new_cat = ServiceCategory(name=cat_name)
            db.session.add(new_cat)
            db.session.commit()
            return {"message" : "Category is created"}
    def delete(self):
        if request.args.get("cat_id"):
            cat  = db.session.query(ServiceCategory).filter_by(id=request.args.get("cat_id")).first()
            if cat:
                db.session.delete(cat)
                db.session.commit()
                return {"message" : "category is deleted"}
            else:
                return {"message" : "category doesn't exist"}  , 409



api.add_resource(CategoryResource , "/api/category")


