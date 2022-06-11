from flask import Blueprint, render_template, session, request, url_for, redirect
from Bleuprints.auth import login_required, first_responder_required
from services.util import create_case, get_form_to_dict, hash_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from datetime import datetime


first_responder = Blueprint('first_responder', __name__, url_prefix='/', template_folder='../templates', static_folder='../static')
client = MongoClient("localhost", 27017)
db = client["pfe"]


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@first_responder.route('/create_case', methods=['GET', 'POST'])
@login_required
@first_responder_required
def create_casing():

    user_id = session['user_id']
    user = db['users'].find_one({"_id": user_id})
    date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        dic = get_form_to_dict(request.form)
        dic["created_by"] = user["first_name"] +" "+ user["last_name"]
        
        form = UploadFileForm()
        file = request.files['file']
        if file:
            file = form.file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/files",secure_filename(file.filename))) 
            mongo_file = {
                "file_name": secure_filename(file.filename),
                "index": db['files'].count_documents({})
                }
            db["files"].insert_one(mongo_file)
        else:
            return render_template('create_case.html', error="please provide a file")

        dic["file_hash"] = hash_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/files",secure_filename(file.filename)))
        create_case(mongo_file, dic)
        return redirect(url_for('general.dashboard'))
    return render_template('create_case.html', date=date, username=user["first_name"] +" "+ user["last_name"])