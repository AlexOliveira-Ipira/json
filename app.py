from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
app.secret_key = 'docker'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(40))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    

    def __init__(self, usuario, name, email):
        self.usuario = usuario
        self.name = name
        self.email = email
       

class userschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

user_schema = userschema()
users_schema = userschema(many=True)
 


@app.route('/post', methods = ['POST'])
def add_post():
    usuario = request.json['usuario']
    name = request.json['name']
    email = request.json['email']

    newuser = Users(usuario, name, email)
    db.session.add(newuser)
    db.session.commit()

    return users_schema.jsonify(newuser)


@app.route('/get', methods = ['GET'])
def get_post():
    all_post = Users.query.all()
    result = users_schema.dump(all_post)

    return jsonify(result)

@app.route('/viewr/<id>', methods=['GET'])
def post_viewr(id):
    viewr = Users.query.get(id)
    return user_schema.jsonify(viewr)

@app.route('/update/<id>/', methods= ['PUT'])
def post_update(id):
    uppost = Users.query.get(id)

    usuario = request.json['usuario']
    name = request.json['name']
    email = request.json['email']

    uppost.usuario = usuario
    uppost.name = name
    uppost.email = email

    db.session.commit()
    return user_schema.jsonify(uppost)


@app.route('/delete/<id>/', methods = ['DELETE'])
def post_delter(id):
    delpost = Users.query.get(id)
    db.session.delete(delpost)
    db.session.commit()

    return user_schema.jsonify(delpost)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True , port=8880)
