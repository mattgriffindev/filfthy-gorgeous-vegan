from flask import render_template, request, redirect, url_for
from cakebox import app, db
from cakebox.models import Category, Recipe

@app.route("/")
def home():
    return render_template("base.html")