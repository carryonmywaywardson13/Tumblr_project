from app import db
from app import app
from app.models.StorageModel import StorageModel

from flask import request

import random
import os


result_data = """
<html><body><script>window.parent.CKEDITOR.tools.callFunction("{num}", "{path}", "{error}");</script></body></html>
"""


@app.route('/admin/upload-image', methods=['POST'])
def upload_image_post():
    item = request.files.get('upload')
    hash = random.getrandbits(128)
    ext = item.filename.split('.')[-1]
    path = '%s.%s' % (hash, ext)

    item.save(
		# STORAGE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/static/storage/')
        os.path.join(app.config['STORAGE'], path)
    )

    storage = StorageModel(
        name=item.filename,
        type=ext,
        path=path,
    )

    db.session.add(storage)
    db.session.commit()

    result = result_data.replace('{num}', request.args.get('CKEditorFuncNum'))
    result = result.replace('{path}', '/static/storage/' + storage.path)
    result = result.replace('{error}', '')

    return result