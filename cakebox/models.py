from cakebox import db

class Users(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    firstname = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return db.Column(db.String(40), unique=True, nullable=False), self.firstname


class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    recipes = db.relationship("Recipe", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name


class Recipe(db.Model):
    # schema for the Recipe model
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), unique=True, nullable=False)
    recipe_desc = db.Column(db.String(500), nullable=False)
    recipe_prep = db.Column(db.String(2), nullable=True)
    recipe_bake = db.Column(db.String(2), nullable=True)
    recipe_serves = db.Column(db.String(2), nullable=True)
    recipe_difficulty = db.Column(db.String(10), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.id, self.recipe_name, self.recipe_desc, self.recipe_prep, self.recipe_bake, self.recipe_serves, self.recipe_difficulty