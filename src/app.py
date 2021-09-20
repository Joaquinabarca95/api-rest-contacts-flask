from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User

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
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200






#ALFINAL DEL ARCHIVO
if __name__ == '__main__':
    app.run()