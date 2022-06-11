from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory
from Bleuprints.auth import login_required, lawyer_required
from pymongo import MongoClient
from services.util import get_case, get_description_index, get_description

lawyer = Blueprint('lawyer', __name__, url_prefix='/', template_folder='../templates', static_folder='../static')
client = MongoClient("localhost", 27017)
db = client["pfe"]

@lawyer.route('/lawyer_cases')
@lawyer_required
@login_required
def law_cases():
    user_id = session['user_id']
    user = db['users'].find_one({"_id": user_id})
    username = user["username"]
    cases = []
    for x in db['files'].find({}):
        case = get_case(x["index"])

        new_case = {
            "created_by": case[0],
            "created_at": case[1],
            "file_hash": case[2],
            "index": x["index"]
        }
        if case[0] != '':
            cases.append(new_case)
    return render_template('lawyer_cases.html', username=username, cases=cases)

@lawyer.route('/lawyer_case/<id>')
@lawyer_required
@login_required
def law_case(id):
    user_id = session['user_id']
    user = db['users'].find_one({"_id": user_id})
    file_name = db['files'].find_one({"index": int(id)})["file_name"]
    descriptions = []
    case = get_case(int(id))
    case_desc = case[4]
    for x in range(0, get_description_index(int(id))):
        desc = get_description(int(id), x)
        new_desc = {
            "updated_by": desc[0],
            "updated_at": desc[1],
            "report_hash": desc[2],
            "vote_app": desc[3],
            "vote_den": desc[4],
            "report_file": db['files'].find_one({"index": int(desc[6])})["file_name"]
        }
        descriptions.append(new_desc)
    
    return render_template('lawyer_case.html', descriptions=descriptions, file_name=file_name, case_desc=case_desc)