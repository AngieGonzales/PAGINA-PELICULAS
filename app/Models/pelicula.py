from app import db

class Peliculas(db.Model):
    __tablename__ = 'pelicula'

    idPelicula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.idCategoria'))

    categorias = db.relationship("Categorias", back_populates="peliculass")
