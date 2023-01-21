import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

ALLOWING_EXTENSIONS = set(['mp4'])
def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWING_EXTENSIONS

editor = Blueprint('editor', __name__, url_prefix='/')

@editor.route('/editor', methods=["GET"])
@login_required
def edit_mp4():
    return render_template('video_editor.html', name=current_user.name), 200

@editor.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        response_code = 500
        response_dict = {}
        try:
            if 'file' not in request.files:
                flash('Any file is not found.')
                response_code = 400
                response_dict['message'] = 'Any file is not found.'
                raise({'code': 400, 'dict': {'message': 'Any file is not found.'}})

            flash('A file is found.')
            file = request.files['file']
            if file.filename == '':
                flash('The name of uploaded file is invalid.')
                raise({'code': 400, 'dict': {'message': 'The name of uploaded file is invalid.'}})

            flash('The name of uploaded file is valid.')
            if not is_file_allowed(file.filename):
                flash('The extension of uploaded file is invalid.')
                raise({'code': 400, 'dict': {'message': 'The extension of uploaded file is invalid.'}})

            flash('The extension of uploaded file is valid.')
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join('./upload', filename))
            response_code = 200
            response_dict = {'message': 'Uploading file is completed.'}
        except Exception as e:
            response_code = e['code'] if 'code' in e.keys() else 500
            response_dict = e['dict'] if 'dict' in e.keys() else {'message': 'Internal server error.'}

        return jsonify(response_dict), response_code

    else:
        return redirect(url_for('editor.edit_mp4')), 200
