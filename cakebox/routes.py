from flask import render_template, request, redirect, url_for
from cakebox import app, db
from cakebox.models import Category, Recipe


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


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
    

@app.route("/edit_recipe")
def edit_recipe():
    return render_template("edit_recipe.html")


@app.route("/login")
def login():
    return render_template("login.html")
    

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")