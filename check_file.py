# выбор уже загруженных файлов
from app import app
from app.models.StorageModel import StorageModel

from flask import render_template


@app.route('/admin/check-file')
def check_file_handler():
    return render_template('file-browse.html', files=StorageModel.query.all())

