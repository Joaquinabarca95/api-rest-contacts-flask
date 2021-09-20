from flask import Flask, render_template, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Profile
import json

app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
Migrate(app, db) #recibe 2 parametros, 1 instancia de la apliacion flask, 2 instancia de la base de datos 
# db init = inicializa las migraciones, db migrate = migrar, querys, db uppgrade = llevar las migraciones hacia la base de datos 
# se escriben en el terminal
# db init solo ejecutar cuando no tengo la carpeta migrations. Solo la primera vez!!
# db migrate crea la version que migramos
# db upgrade crea la base de datos database.db
CORS(app)  # evita que de error CORS y no bloquee las peticiones a esta url, puedo decir desde que ip puedo aceptar peticiones



@app.route("/")
def main():
    return render_template('index.html')


@app.route("/api/users", methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize_with_profile(), users))
    return jsonify(users), 200



@app.route("/api/users", methods=['POST'])
def add_new_user():
    name = request.json.get('name')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')

    bio = request.json.get('bio', "")
    twitter = request.json.get('twitter', "")
    facebook = request.json.get('facebook', "")
    instagram = request.json.get('instagram', "")
    linkedin = request.json.get('linkedin', "")


    if not email: return jsonify({"status": False, "msg": "Email is required"}), 400
   
    user = User.query.filter_by(email=email).first()  # buscando si existe el email o si el usuario existe 
    if user: return jsonify({"status": False, "msg": "Email already in use!"}), 400
   
    """
    newUser = User()
    newUser.name = name
    newUser.lastname = lastname
    newUser.email = email
    newUser.password = password
    newUser.save()
    

    profile = Profile()
    profile.bio = bio
    profile.twitter = twitter
    profile.facebook = facebook
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.user_id = newUser.id
    profile.save()

    return jsonify(newUser.serialize()), 201
    """

    newUser = User()
    newUser.name = name
    newUser.lastname = lastname
    newUser.email = email
    newUser.password = password
    

    profile = Profile()
    profile.bio = bio
    profile.twitter = twitter
    profile.facebook = facebook
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.user_id = newUser.id

    newUser.profile = profile  # usando el relationship creado
    newUser.save()

    return jsonify(newUser.serialize_with_profile()), 201


@app.route("/api/users/<int:id>", methods=['PUT'])  # la url necesita un parametro para encontrar el usuario a modificar
def put_users(id):
    name = request.json.get('name')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.update()

    return jsonify(user.serialize()), 200



@app.route("/api/users/<int:id>", methods=['DELETE'])  # la url necesita un parametro para encontrar el usuario a eliminar
def delete_user(id):
    user = User.query.get(id)
    if not user: return jsonify({"status": False, "msg":"User doesn't exist"}), 404
    user.delete()
    return jsonify({"status": True, "msg":"User deleted"}), 200





#ALFINAL DEL ARCHIVO
if __name__ == '__main__':
    app.run()