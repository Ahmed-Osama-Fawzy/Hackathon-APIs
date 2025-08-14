from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from app.models import Users, Selections, Invitations, Tasks
from datetime import date

@app.route("/GetTeamMembers", methods=["GET"]) 
@jwt_required() 
def GetTeamMembers(): 
    try: 
        claims = get_jwt() 
        role = claims.get("Role") 
        username = claims.get("Username") 
        if role != "Team": 
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403 
        
        data = [ 
            { 
                "Id": person.Id, 
                "Username": person.person.Username, 
                "Email": person.person.Email, "Status": 
                person.Status 
            } 
            for person in Invitations.query.join(Invitations.team).filter(Users.Username == username).all() 
        ] 
        if data: 
            return jsonify({"Status": "Success", "Data": data, "Message": ""}), 200 
        return jsonify({"Status": "Success", "Data": [], "Message": "No Invivations Found"}), 200 
    except Exception as e: 
        db.session.rollback() 
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/GetSelectedTasks", methods=["GET"])
@jwt_required()
def GetSelectedTasks():
    try:
        claims = get_jwt()
        role = claims.get("Role")
        username = claims.get("Username")

        if role != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        selections = (
            Selections.query.join(Selections.team).filter(Users.Username == username).all())

        data = [
            {
                "Id": inv.Id,
                "Category": inv.task.Category,
                "Section": inv.task.Section,
                "Code": inv.task.Code,
                "Disease": inv.task.Disease,
                "Datasets": [inv.task.Dataset1, inv.task.Dataset2, inv.task.Dataset3],
                "Status": inv.Status
            }
            for inv in selections
        ]

        return jsonify({
            "Status": "Success",
            "Data": data,
            "Message": "" if data else "No Selected Tasks Found"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/SelectTask", methods=["POST"])
@jwt_required()
def SelectTask():
    try:
        claims = get_jwt()
        username = claims.get("Username")

        if claims.get("Role") != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        TaskId = data.get("TaskId")

        if not TaskId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Team = Users.query.filter_by(Username=username).first()

        if not Team:
            return jsonify({"Status": "Warning", "Message": "Team Must be Founded First"}), 400

        TeamId = Team.Id
        SelectedTasksCount = Selections.query.filter_by(TeamId=TeamId).count()

        Duplicate = Selections.query.filter(and_( Selections.TeamId==TeamId,  Selections.TaskId==TaskId)).first()
        if Duplicate:
            return jsonify({"Status": "Warning", "Message": "You Already Select this Task Before"}), 400

        the_task = Tasks.query.get_or_404(TaskId)
        if the_task.Status not in ["ReOpen", "Opened"]:
            return jsonify({"Status": "Warning", "Message": "This Task Already Closed"}), 400

        if SelectedTasksCount < 5:
            today = date.today()
            new_invitation = Selections(Date=today, TeamId=TeamId, TaskId=TaskId, Status="InProcess")
            db.session.add(new_invitation)
            the_task.Status = "Closed"
            db.session.commit()
        else:
            return jsonify({"Status": "Error", "Message": "Team's Selected Tasks Completed (Max is 5 Tasks)"}), 309
        return jsonify({"Status": "Success", "Message": "Task selected successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/CancelTask", methods=["POST"])
@jwt_required()
def CancelTask():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        SelectionId = data.get("SelectionId")

        if not SelectionId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Selection = Selections.query.get_or_404(SelectionId)

        if not Selection:
            return jsonify({"Status": "Warning", "Message": "The Task Must be Founded First"}), 400
        
        the_task = Tasks.query.get_or_404(Selection.TaskId)

        if not the_task:
            return jsonify({"Status": "Warning", "Message": "The Task Must be Founded First"}), 400
        
        Selection.Status = "Cancel"
        the_task.Status = "ReOpen"
        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Task Canceled successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/ResumeTask", methods=["POST"])
@jwt_required()
def ResumeTask():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Team":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        SelectionId = data.get("SelectionId")

        if not SelectionId:
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        Selection = Selections.query.get_or_404(SelectionId)

        if not Selection:
            return jsonify({"Status": "Warning", "Message": "The Task Must be Founded First"}), 400
        
        if Selection.Status != "Cancel":
            return jsonify({"Status": "Warning", "Message": "The Task Must be Founded First"}), 400

        the_task = Tasks.query.get_or_404(Selection.TaskId)

        if the_task.Status not in ["ReOpen", "Opened"]:
            return jsonify({"Status": "Warning", "Message": "This Task Already Closed"}), 400

        if not the_task:
            return jsonify({"Status": "Warning", "Message": "The Task Must be Founded First"}), 400
        
        the_task.Status = "ReClosed"
        Selection.Status = "Resumed"
        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Task Canceled successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500