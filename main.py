from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

@app.route("/")
def home():
    return "Welcome to Cafe API!"

@app.route("/random", methods=["GET"])
def get_random_cafe():
    random_cafe = Cafe.query.order_by(db.func.random()).first()
    return jsonify(cafe_to_dict(random_cafe))

@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = Cafe.query.all()
    cafes_list = [cafe_to_dict(cafe) for cafe in cafes]
    return jsonify(cafes_list)

@app.route("/search", methods=["GET"])
def search_cafes():
    loc = request.args.get('loc')
    if not loc:
        return jsonify({'error': 'Location parameter "loc" is required'}), 400
    
    cafes = Cafe.query.filter_by(location=loc).all()
    cafes_list = [cafe_to_dict(cafe) for cafe in cafes]
    return jsonify(cafes_list)

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=request.form.get("has_sockets") == 'True',
        has_toilet=request.form.get("has_toilet") == 'True',
        has_wifi=request.form.get("has_wifi") == 'True',
        can_take_calls=request.form.get("can_take_calls") == 'True',
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
    
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_coffee_price(cafe_id):
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify({"error": "New price is required."}), 400

    cafe = Cafe.query.get_or_404(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({"success": "Successfully updated the coffee price."})
    else:
        return jsonify({"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    
def cafe_to_dict(cafe):
    if cafe:
        return {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price
        }
    else:
        return {}

if __name__ == '__main__':
    app.run(debug=True)
