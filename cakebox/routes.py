from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from cakebox import app, db, mongo
from cakebox.models import Category, Users


@app.route("/")
def index():
    return render_template("index.html")


def login_required(f):
    # Restricts page access - adapted from
    # https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You need to be logged in to view this page")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/categories")
@login_required
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


@app.route("/contact")
def contact():
    return render_template("contact.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Allows users to login into an existing account
    and verifies username and password """
    if "user" in session:
        flash("You're already logged in!")
        return redirect(url_for('profile'))

    if request.method == "POST":
        # check if username exists
        existing_user = Users.query.filter(
            Users.username == request.form.get("username").lower()).all()

        if existing_user:
            request.form.get("username")
            # password check
            if check_password_hash(existing_user[0].password, request.form.get(
                    "password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")
    

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out. See you soon!")
    session.pop("user")
    return redirect(url_for("index"))


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        flash("You're already logged in!")
        return redirect(url_for('profile'))

    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.username ==
                                           request.form.get(
                                            "username").lower()).all()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        user = Users(
            username=request.form.get("username").lower(),
            firstname=request.form.get("firstname").lower(),
            password=generate_password_hash(request.form.get("password")),
        )

        db.session.add(user)
        db.session.commit()

        new_user = Users.query.get_or_404(user.id)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        flash("Registration successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/recipes")
def recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


# @app.route("/search_recipes", methods=["GET", "POST"])
# def search_recipes():
#     """ finds recipes from db and renders them on recipes page """
#     query = request.form.get("query")
#     recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
#     if len(recipes) == 0:
#         flash("Sorry, there are no results!")
#         return redirect(url_for("recipes"))

#     return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe():
    if "user" not in session:
        flash("You must be logged in to add a recipe")
        return redirect(url_for("login"))

    if request.method == "POST":

        recipe = {
            "category_id": request.form.get("category_id"),
            "recipe_name": request.form.get("recipe_name"),
            "image_url": request.form.get("image_url"),
            "created_by": session["user"],
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_inst": request.form.get("recipe_inst"),
            "recipe_prep": request.form.get("recipe_prep"),
            "recipe_bake": request.form.get("recipe_bake"),
            "recipe_serves": request.form.get("recipe_serves")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Thank you for sharing your recipe!")
        return redirect(url_for("recipes"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if "user" not in session or session["user"] != recipe["created_by"]:
        flash("You can edit only your own recipes and must be logged in!")
        return redirect(url_for("recipes"))

    if request.method == "POST":
        request.form.get("recipe_name")
        submit = {
            "category_id": request.form.get("category_id"),
            "recipe_name": request.form.get("recipe_name"),
            "image_url": request.form.get("image_url"),
            "created_by": session["user"],
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_inst": request.form.get("recipe_inst"),
            "recipe_prep": request.form.get("recipe_prep"),
            "recipe_bake": request.form.get("recipe_bake"),
            "recipe_serves": request.form.get("recipe_serves")
        }
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)},
                                    {"$set": submit})
        flash("Recipe successfully updated!")
        return redirect(url_for("recipes"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("edit_recipe.html", recipe=recipe,
                           categories=categories)


@app.route("/delete_recipe/<recipe_id>")
@login_required
def delete_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if "user" not in session or session["user"] != recipe["created_by"]:
        flash("You must be logged in to edit your own recipes!")
        return redirect(url_for("recipes"))

    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("recipes"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" in session:
        recipe_list = mongo.db.recipes.find(
            {"created_by": {'$eq': session['user']}})
        categories = list(
                          Category.query.order_by(
                            Category.category_name).all())
        return render_template("profile.html", username=session["user"],
                               recipe_list=recipe_list, categories=categories)
    return redirect(url_for("login"))
