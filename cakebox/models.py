from cakebox import db

class Users(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    firstname = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.firstname


class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name