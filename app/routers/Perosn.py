from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt
from app.models import Users, Invitations, Selections, Tasks

@app.route("/GetAllPersons", methods=["GET"])
@jwt_required()
def GetAllPersons():
    try:
        claims = get_jwt()
        role = claims.get("Role")
        if role != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = [
            {
                "Id": person.Id,
                "Username": person.Username,
                "Email": person.Email,
            }
            for person in Users.query.filter(Users.Role=="Person").order_by(Users.Id.asc()).all()
        ]

        if data:
            return jsonify({"Status": "Success", "Data": data, "Message": ""}), 200
        return jsonify({"Status": "Success", "Data": [], "Message": "No Persons Found"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/GetPersonInvitations", methods=["GET"])
@jwt_required()
def GetPersonInvitations():
    try:
        claims = get_jwt()
        role = claims.get("Role")
        username = claims.get("Username")
        
        if role != "Person":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = [
            {
                "Id": inviation.Id,
                "Username": inviation.team.Username,
                "Status": inviation.Status
            }
            for inviation in Invitations.query.filter(Invitations.person.has(Users.Username == username)).all()
        ]

        if data:
            return jsonify({"Status": "Success", "Data": data, "Message": ""}), 200
        return jsonify({"Status": "Success", "Data": [], "Message": "No Inviations Found"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/GetPersonTasks", methods=["GET"])
@jwt_required()
def GetPersonTasks():
    try:
        claims = get_jwt()
        role = claims.get("Role")
        username = claims.get("Username")

        if role != "Person":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        accepted_invitations = Invitations.query.join(Users, Invitations.PersonId == Users.Id) \
            .filter(Users.Username == username, Invitations.Status == "Accepted").all()

        team_ids = [inv.TeamId for inv in accepted_invitations]

        if not team_ids:
            return jsonify({"Status": "Success", "Data": [], "Message": "No Accepted Invitations"}), 200

        selections = Selections.query.join(Tasks, Selections.TaskId == Tasks.Id) \
            .filter(Selections.TeamId.in_(team_ids)).all()

        data = [
            {
                "TaskId": sel.task.Id,
                "Category": sel.task.Category,
                "Section": sel.task.Section,
                "Code": sel.task.Code,
                "Disease": sel.task.Disease,
                "Status": sel.task.Disease,
                "Datasets": [sel.task.Dataset1, sel.task.Dataset2, sel.task.Dataset3],
                "TeamUsername": sel.team.Username
            }
            for sel in selections
        ]

        return jsonify({"Status": "Success", "Data": data, "Message": ""}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/AcceptInvitation", methods=["POST"])
@jwt_required()
def AcceptInvitation():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Person":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        InvitationId = data.get("InvitationId")

        if not InvitationId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Invitation = Invitations.query.get_or_404(InvitationId)

        if not Invitation:
            return jsonify({"Status": "Warning", "Message": "Invitation Must be Founded First"}), 400

        Invitation.Status = "Accepted"
        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Invitation Accepted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/RejectInvitation", methods=["POST"])
@jwt_required()
def RejectInvitation():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Person":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        InvitationId = data.get("InvitationId")

        if not InvitationId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Invitation = Invitations.query.get_or_404(InvitationId)

        if not Invitation:
            return jsonify({"Status": "Warning", "Message": "Invitation Must be Founded First"}), 400

        Invitation.Status = "Rejected"
        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Invitation Rejected successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500
