"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsecrets'
app.config['DEBUG_TB_REDIRECT_INTERCEPTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

def serialize(cupcake):
    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

"""Application Functionality"""

@app.route('/')
def homepage():
     return render_template('cupcakes.html')



"""API Functionality"""
@app.route('/api/cupcakes')
def show_all_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [serialize(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    cupcake = Cupcake.query.get(id)
    json_cupcake = serialize(cupcake)
    return jsonify(cupcake = json_cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
        flavor = request.json['flavor']
        size = request.json['size']
        rating = request.json['rating']
        image = request.json['image']
        
        new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

        db.session.add(new_cupcake)
        db.session.commit()
        
        serialized = serialize(new_cupcake)
        return (jsonify(cupcake = serialized), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()

    json_cupcake = serialize(cupcake)

    return jsonify(cupcake = json_cupcake)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='deleted')


