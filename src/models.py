from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#los modelos nos permiten interactuar con la informacion dentro de las tablas

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    profile = db.relationship('Profile', backref='user', cascade="all, delete", uselist=False) # 1er atribuito es el modelo con el que estoy relacionado, 2do indica como quiero que la tabla de profile pueda acceder a mis datos, 3er (uselist) defino si es una relacion 1a1 o 1aMuchos, si se omite es 1 a muchos y devuelve un array por defecto

    def serialize(self):     # permite tomar los datos y devolverlos como un objeto/diccionario
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email
        }

    def serialize_with_profile(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "profile": self.profile.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, default ="")
    twitter = db.Column(db.String(100), default ="")
    facebook = db.Column(db.String(100), default ="")
    instagram = db.Column(db.String(100), default ="")
    linkedin = db.Column(db.String(100), default ="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False) 
    # ondelete="CASCADE" permite eliminar datos que son relaciones directas entre padre e hijo, ya que estipulamos que el id no puede ser nulo y al eliminar tira error pqe no existe ese dato que no puede ser nulo (user_id)

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin
        }


    def serialize_with_user(self):
        return {
            "id": self.id,
            "name": self.user.name + " " + self.user.lastname,
            "bio": self.bio,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()