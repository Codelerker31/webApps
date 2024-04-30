from flask import request, jsonify
from config import app, db
from models import Field


# Tried to get the json endpiont data to load initially
# @app.route('/fields/<int:user_id>', methods=['GET'])
# def save_fields(user_id):
#     fields = Field.query.get(user_id)
    
#     try:
#         response = request.get('https://jsonplaceholder.typicode.com/users')
#         data = response.json()
        
#         for field_data in data:
#             field = fields(name=field_data['name'], username=field_data['username'],
#                         email=field_data['email'], website=field_data['website'])
#             db.session.add(field)
        
#         db.session.commit()
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": str(e)}), 400


@app.route("/fields", methods=["GET"])
def fields():
    fields = Field.query.all()
    json_fields = list(map(lambda x: x.to_json(), fields))
    return jsonify({"contacts": json_fields})


@app.route("/create_fields", methods=["POST"])
def create_fields():
    name = request.json.get("name")
    user_name = request.json.get("username")
    email = request.json.get("email")
    website = request.json.get("website")

    if not name or not user_name or not email or not website:
        return (
            jsonify({"message": "You must include a Name, User name, Email and Website"}),
            400,
        )

    new_fields = Field (name=name, user_name=user_name, email=email, website=website)
    try:
        db.session.add(new_fields)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/update_fields/<int:user_id>", methods=["PATCH"])
def update_fields(user_id):
    fields = Field.query.get(user_id)

    if not fields:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    fields.name = data.get("name", fields.name)
    fields.user_name = data.get("username", fields.user_name)
    fields.email = data.get("email", fields.email)
    fields.website = data.get("website", fields.website)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_fields/<int:user_id>", methods=["DELETE"])
def delete_fields(user_id):
    fields = Field.query.get(user_id)

    if not fields:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(fields)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    