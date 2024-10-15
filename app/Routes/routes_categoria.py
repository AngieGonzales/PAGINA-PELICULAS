import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app.Models.categoria import Categorias
from app import db

bp = Blueprint('categoria', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    data = Categorias.query.all()
    return render_template('categoria/index.html', data=data)

@bp.route('/categoria/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        
        if 'imagen' not in request.files:
            return "No se ha seleccionado ninguna imagen", 400
        
        file = request.files['imagen']
        if file.filename == '':
            return "Nombre de archivo vacío", 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            new_categoria = Categorias(nombre=nombre, imagen=filename)
            db.session.add(new_categoria)
            db.session.commit()

            return redirect(url_for('categoria.index'))

    return render_template('categoria/add.html')

@bp.route('/categoria/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    categoria = db.session.get(Categorias, id)
    if categoria is None:
        return "Categoría no encontrada", 404

    if request.method == 'POST':
        categoria.nombre = request.form['nombre']

        if 'imagen' in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                categoria.imagen = filename

        db.session.commit()
        return redirect(url_for('categoria.index'))

    return render_template('categoria/edit.html', categoria=categoria)

@bp.route('/categoria/delete/<int:id>')
def delete(id):
    categoria = db.session.get(Categorias, id)
    if categoria is None:
        return "Categoría no encontrada", 404
    
    db.session.delete(categoria)
    db.session.commit()

    return redirect(url_for('categoria.index'))