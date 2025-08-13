# from flask import request, jsonify
# from app import app, db
# from flask_jwt_extended import jwt_required, get_jwt
# from sqlalchemy import and_
# from app.models import Courses

# @app.route("/GetAllCourses", methods=["GET"])
# @jwt_required()
# def GetAllCourses():
#     try:
#         claims = get_jwt()
#         role = claims.get("Role")
#         username = claims.get("Username")
#         if role != "Owner":
#             return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

#         Data = [
#             {
#                 "Id": Course.id,
#                 "Title": Course.Title,
#                 "HPrice": Course.HPrice,
#                 "Type": Course.Type
#             }
#             for Course in Courses.query.order_by(Courses.id.asc()).all()
#         ]

#         if Data:
#             return jsonify({"Status":"Success", "Data":Data}), 200

#         return jsonify({"Status":"Success", "Data":[], "Message":"Not Found Courses"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Status":"Error", "Message":str(e)}), 500


# @app.route("/InsertCourse", methods=["POST"])
# @jwt_required()
# def InsertCourse():
#     try:
#         claims = get_jwt()
#         role = claims.get("Role")
#         if role == "Instructor":
#             return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403
    
#         data = request.get_json()
#         CourseTitle = data.get("Title")
#         CourseHPrice = data.get("Price")
#         CourseType = data.get("Type")

#         if not all([CourseTitle, CourseHPrice, CourseType]):
#             return jsonify({"Status": "Warning", "Message": "All Inputs Required to Insert New Course"}), 300

#         Duplicate = Courses.query.filter_by(Title=CourseTitle).first()
#         if Duplicate:
#             return jsonify({"Status": "Warning", "Message": "The Title Found Before, Please Write New One"}), 302
    
#         new_course = Courses(Title=CourseTitle, HPrice=CourseHPrice, Type=CourseType)
#         db.session.add(new_course)
#         db.session.commit()
#         return jsonify({"Status": "Success", "Message": "The Course Inserted Successfully"}), 200
    
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Status": "Error", "Message": str(e)}), 500

# @app.route("/ModifyCourse", methods=["POST"])
# @jwt_required()
# def ModifyCourse():
#     try:
#         claims = get_jwt()
#         role = claims.get("Role")
#         if role == "Instructor":
#             return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403
    
#         data = request.get_json()
#         CourseId = data.get("Id")
#         CourseTitle = data.get("Title")
#         CourseHPrice = data.get("Price")
#         CourseType = data.get("Type")

#         if not all([CourseId, CourseTitle, CourseHPrice, CourseType]):
#             return jsonify({"Status": "Warning", "Message": "All Inputs Required to Modify The Course"}), 400

#         Duplicate = Courses.query.filter(and_(Courses.Title==CourseTitle, Courses.id!=CourseId)).first()
#         if Duplicate:
#             return jsonify({"Status": "Warning", "Message": "The Title Found Before, Please Write New One"}), 409
    
#         the_course = Courses.query.get_or_404(CourseId)
#         the_course.Title = CourseTitle
#         the_course.HPrice = CourseHPrice
#         the_course.Type = CourseType
#         db.session.commit()
#         return jsonify({"Status": "Success", "Message": "The Course Modified Successfully"}), 200
    
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Status": "Error", "Message": str(e)}), 500

# @app.route("/DeleteCourse", methods=["POST"])
# @jwt_required()
# def DeleteCourse():
#     try:
#         claims = get_jwt()
#         role = claims.get("Role")
#         if role == "Instructor":
#             return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403
    
#         data = request.get_json()
#         CourseId = data.get("Id")

#         if not CourseId:
#             return jsonify({"Status": "Warning", "Message": "All Inputs Required to Delete The Course"}), 400

#         the_course = Courses.query.get_or_404(CourseId)
        
#         if not the_course:
#             return jsonify({"Status": "Warning", "Message": "This Course's Id Not Found"}), 400
        
#         db.session.delete(the_course)
#         db.session.commit()
#         return jsonify({"Status": "Success", "Message": "The Course Removed Successfully"}), 200
    
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Status": "Error", "Message": str(e)}), 500

