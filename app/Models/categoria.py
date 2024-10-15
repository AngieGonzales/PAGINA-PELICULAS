from app import db

class Categorias(db.Model):
    __tablename__ = 'categoria'
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(50), nullable=False)

    peliculass = db.relationship('Peliculas', back_populates='categorias')
