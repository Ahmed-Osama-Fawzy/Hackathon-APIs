from app import app, db
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models import Users
from datetime import timedelta
from app.handler.notification_handler import *

CONST_DATA = {}

def store_and_send_otp(email, title, startmess):
    otp = str(generate_numeric_otp())
    CONST_DATA["OTP"] = otp
    message = f"{startmess}: {otp}"
    return SendOTPEmail(message, title, email)

@app.route("/Login", methods=["POST"])
def Login():
    try:
        data = request.get_json()
        Username = data.get("Username", "").strip()
        Password = data.get("Password", "").strip()

        if not all([Username, Password]):
            return jsonify({"Status":"Warning", "Message":"All inputs required"}), 403
        
        user = Users.query.filter_by(Username=Username).first()
        if user:
            if user.CheckPassword(Password):
                access_token = create_access_token(
                    identity=str(user.Id),
                    additional_claims={
                        "Username": user.Username,
                        "Role": user.Role
                    },
                    expires_delta=timedelta(days=15)
                )
                return jsonify({"Status":"Success", "Message":"Access Right", "access_token":access_token}), 200
            else:
                return jsonify({"Status":"Error", "Message":"Wrong password"}), 401
        else:
            return jsonify({"Status":"Error", "Message":"Username not found"}), 403
        
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"Status":"Warning", "Message":f"You have Error: {e}"}), 500
    
@app.route("/Register", methods=["POST"])
def Register():
    try:
        data = request.get_json()
        Type = data.get("Type", "").strip()
        Username = data.get("Username", "").strip()
        Email = data.get("Email", "").strip()
        Password = data.get("Password", "").strip()
        RePassword = data.get("RePassword", "").strip()

        if not all([Type, Username, Email, Password, RePassword]):
            return jsonify({"Status":"Warning", "Message":"All inputs required"}), 403
        
        duplicate = Users.query.filter_by(Username=Username).first()
        if duplicate:
            return jsonify({"Status": "Warning", "Message": "Username already used"}), 409
        
        CONST_DATA.update({
            "Type": Type,
            "Username": Username,
            "Email": Email,
            "Password": Password
        })

        if store_and_send_otp(Email, "Confirm Email Via Message", "OTP is"):
            return jsonify({"Status":"Success", "Message":"OTP sent successfully"}), 200
        else:
            return jsonify({"Status":"Error", "Message":"Failed to send OTP"}), 410 

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"Status":"Warning", "Message":f"You have Error: {e}"}), 500

@app.route("/CheckOTP", methods=["POST"])
def CheckOTP():
    try:
        data = request.get_json()
        the_otp = str(data.get("OTP", "")).strip()

        if not the_otp:
            return jsonify({"Status":"Warning", "Message":"OTP is required"}), 403

        if CONST_DATA.get("OTP") == the_otp:
            new_user = Users(
                Username=CONST_DATA["Username"],
                Role=CONST_DATA["Type"],
                Email=CONST_DATA["Email"]
            )
            new_user.SetPassword(CONST_DATA["Password"])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"Status":"Success", "Message":"Account activated successfully"}), 200
        else:
            return jsonify({"Status":"Error", "Message":"Incorrect OTP"}), 410 

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"Status":"Warning", "Message":f"You have Error: {e}"}), 500

@app.route("/ResendOTP", methods=["GET"])
def ResendOTP():
    try:
        if not CONST_DATA.get("Email"):
            return jsonify({"Status":"Error", "Message":"No registration in progress"}), 400

        if store_and_send_otp(CONST_DATA["Email"], "Confirm Email Via Message", "New OTP is"):
            return jsonify({"Status":"Success", "Message":"New OTP sent successfully"}), 200
        else:
            return jsonify({"Status":"Error", "Message":"Failed to send new OTP"}), 410 

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"Status":"Warning", "Message":f"You have Error: {e}"}), 500
