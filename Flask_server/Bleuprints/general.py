from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory
from Bleuprints.auth import login_required
from pymongo import MongoClient
import os

general = Blueprint('general', __name__, url_prefix='/', template_folder='../templates', static_folder='../static')
client = MongoClient("localhost", 27017)
db = client["pfe"]

@general.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = db['users'].find_one({"_id": user_id})
    username = user["username"]
    links = []
    if user["accountType"] == "first_responder":
        links.append({"field":"CREATE A NEW CASE", "link":"/create_case"})
    if user["accountType"] == "investigator":
        links.append({"field":"Case to Update List", "link":"/update_cases"})
        links.append({"field":"Case to Vote List", "link":"/vote_cases"})
    if user["accountType"] == "lawyer":
        links.append({"field":"List of cases", "link":"/lawyer_cases"})
    return render_template('dashboard.html', username=username, links=links)

@general.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))

@general.route('/uploads/<filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/files")
    return send_from_directory(directory=uploads, filename=filename, path=uploads)