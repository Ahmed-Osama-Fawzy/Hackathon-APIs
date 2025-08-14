from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from app.models import Users, Invitations
from datetime import date
from app.handler.notification_handler import *

@app.route("/InvitePerson", methods=["POST"])
@jwt_required()
def InvitePerson():
    try:
        claims = get_jwt()
        username = claims.get("Username")
        if claims.get("Role") != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        PersonId = data.get("PersonId")

        if not PersonId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Team = Users.query.filter_by(Username=username).first()

        if not Team:
            return jsonify({"Status": "Warning", "Message": "Team Must be Founded First"}), 400

        TeamId = Team.Id
        TeamMemeberCount = Invitations.query.filter_by(TeamId=TeamId).count()

        Duplicate = Invitations.query.filter(and_( Invitations.TeamId==TeamId,  Invitations.PersonId==PersonId)).first()
        
        if Duplicate:
            return jsonify({"Status": "Warning", "Message": "You Already Invite this User Before"}), 400

        the_person = Users.query.get_or_404(PersonId)
        Email = the_person.Email
        Message = f"An Invitaion has been sent to your email. from {Team.Username} Team, Please check your inbox."
        if TeamMemeberCount < 6:
            today = date.today()
            new_invitation = Invitations(Date=today, TeamId=TeamId, PersonId=PersonId, Status="Pending")
            db.session.add(new_invitation)
            SendOTPEmail(Message,"Team Invitaion", Email)
            db.session.commit()
        else:
            return jsonify({"Status": "Error", "Message": "Team Completed (Max is 6 Persons)"}), 309
        return jsonify({"Status": "Success", "Message": "Invitation Sended successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/RemoveInvitation", methods=["POST"])
@jwt_required()
def RemoveInvitation():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        InvitationId = data.get("InvitationId")

        if not InvitationId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Invitation = Invitations.query.get_or_404(InvitationId)

        if not Invitation:
            return jsonify({"Status": "Warning", "Message": "Invitation Must be Founded First"}), 400

        db.session.delete(Invitation)
        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Invitation Removed successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

