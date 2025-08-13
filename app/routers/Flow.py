from app import app, db
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models import Users
from datetime import timedelta

@app.route("/Login", methods=["POST"])
def Login():
    try:
        data = request.get_json()
        Username = data.get("Username", "").strip()
        Password = data.get("Password", "").strip()
        if not all([Username, Password]):
            return jsonify({"Status":"Warning", "Message":"all Inputs Required"}), 403
        
        User = Users.query.filter_by(Username=Username).first()
        if User:
            if User.CheckPassword(Password):
                access_token = create_access_token(
                    identity=str(User.Id),
                    additional_claims={
                        "Username": User.Username,
                        "Role": User.Role
                    },
                    expires_delta=timedelta(days=15)
                )
                return jsonify({"Status":"Success", "access_token":access_token}), 200
            else:
                return jsonify({"Status":"Error", "Message":"you entred worng password, try again"}), 401
        else:
            return jsonify({"Status":"Error", "Message":"this username not founded, try again"}), 403
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status":"Warning", "Message":f"you have Error Is f{e}"}), 500