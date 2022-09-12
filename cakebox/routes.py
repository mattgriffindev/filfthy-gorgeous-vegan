from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from cakebox import app, db
from cakebox.models import Category, Recipe, Users


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


@app.route("/contact")
def contact():
    return render_template("contact.html")
    

@app.route("/login")
def login():
    return render_template("login.html")
    

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


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out. See you soon!")
    session.pop("user")
    return redirect(url_for("index"))


@app.route("/recipes")
def recipes():
    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        recipe = Recipe(
            recipe_name=request.form.get("recipe_name"),
            recipe_desc=request.form.get("recipe_desc"),
            recipe_prep=request.form.get("recipe_prep"),
            recipe_bake=request.form.get("recipe_bake"),
            recipe_serves=request.form.get("recipe_serves"),
            recipe_difficulty=request.form.get("recipe_difficulty"),
            category_id=request.form.get("category_id")
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("recipes"))
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        recipe.recipe_name=request.form.get("recipe_name"),
        recipe.recipe_desc=request.form.get("recipe_desc"),
        recipe.recipe_prep=request.form.get("recipe_prep"),
        recipe.recipe_bake=request.form.get("recipe_bake"),
        recipe.recipe_serves=request.form.get("recipe_serves"),
        recipe.recipe_difficulty=request.form.get("recipe_difficulty"),
        recipe.category_id=request.form.get("category_id")
        db.session.commit()
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")