import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app.Models.pelicula import Peliculas
from app.Models.categoria import Categorias
from app import db

bp = Blueprint('pelicula', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/index/pelicula/<int:categoria_id>', methods=['GET'])
def index(categoria_id):
    peliculas = Peliculas.query.all()
    categorias = Categorias.query.all()
    peliculas = Peliculas.query.filter_by(categoria_id=categoria_id).all()
    return render_template('pelicula/index.html', data=peliculas, categorias=categorias, categoria_id=categoria_id)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        categoria_id = request.form['categoria'] 

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

            # Crear el nuevo producto incluyendo la categoría seleccionada
            new_pelicula = Peliculas(nombre=nombre, imagen=filename, categoria_id=categoria_id, fecha=fecha)
            db.session.add(new_pelicula)
            db.session.commit() 

            # Redirigir al índice del cliente con el 'id' de la categoría
            return redirect(url_for('pelicula.index', categoria_id=categoria_id))

    categorias = Categorias.query.all()
    print(categorias)
    return render_template('pelicula/add.html', categorias=categorias)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    pelicula = Peliculas.query.get_or_404(id)

    if request.method == 'POST':
        pelicula.nombre = request.form.get('nombre') 
        pelicula.descripcion = request.form.get('descripcion')
        pelicula.fecha = request.form.get('fecha')
        pelicula.categoria_id = request.form.get('categoria')
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                if pelicula.imagen:
                    old_image_path = os.path.join(upload_folder, pelicula.imagen)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                file.save(os.path.join(upload_folder, filename))
                pelicula.imagen = filename

        db.session.commit()
        return redirect(url_for('pelicula.index', categoria_id=pelicula.categoria_id))

    categorias = Categorias.query.all()
    return render_template('pelicula/edit.html', pelicula=pelicula, categorias=categorias)

@bp.route('/delete/<int:id>')
def delete(id):
    pelicula = Peliculas.query.get_or_404(id)
    categoria_id = pelicula.categoria_id  
    db.session.delete(pelicula)
    db.session.commit()

    return redirect(url_for('pelicula.index', categoria_id=categoria_id))