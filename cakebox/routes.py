from flask import render_template, request, redirect, url_for
from cakebox import app, db
from cakebox.models import Category, Recipe


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add_category")
def add_category():
    return render_template("add_category.html")
    

@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
    

@app.route("/edit_category")
def edit_category():
    return render_template("edit_category.html")


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