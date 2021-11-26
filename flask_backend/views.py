from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
import json


from .models import Note
from . import db


#from medicine_proc.medicine import ProgressSocket, Medicine

views = Blueprint('views', __name__)

@views.route('/test')
def test_view():
    return "<h1>Test</h1>"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})








