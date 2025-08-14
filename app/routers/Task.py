from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_
from app.models import Tasks

@app.route("/GetAllTasks", methods=["GET"])
@jwt_required()
def GetAllTasks():
    try:
        claims = get_jwt()
        role = claims.get("Role")
        if role == "Person":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = [
            {
                "Id": task.Id,
                "Category": task.Category,
                "Section": task.Section,
                "Code": task.Code,
                "Disease": task.Disease,
                "Datasets": [task.Dataset1, task.Dataset2, task.Dataset3],
                "Status": task.Status 
            }
            for task in Tasks.query.order_by(Tasks.Id.asc()).all()
        ]

        if data:
            return jsonify({"Status": "Success", "Data": data, "Message": ""}), 200
        return jsonify({"Status": "Success", "Data": [], "Message": "No Tasks Found"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/InsertTask", methods=["POST"])
@jwt_required()
def InsertTask():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Admin":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

        data = request.get_json()
        category = data.get("Category")
        section = data.get("Section")
        code = data.get("Code")
        disease = data.get("Disease")
        datasets = data.get("Datasets") or []

        if not all([category, section, code, disease, datasets]):
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        duplicate = Tasks.query.filter(
            Tasks.Category == category,
            Tasks.Section == section,
            Tasks.Code == code,
            Tasks.Disease == disease
        ).first()

        if duplicate:
            return jsonify({"Status": "Warning", "Message": "This record already exists"}), 409

        dataset1 = datasets[0] if len(datasets) > 0 else ""
        dataset2 = datasets[1] if len(datasets) > 1 else ""
        dataset3 = datasets[2] if len(datasets) > 2 else ""

        new_task = Tasks(
            Category=category,
            Section=section,
            Code=code,
            Disease=disease,
            Status="Open",
            Dataset1=dataset1,
            Dataset2=dataset2,
            Dataset3=dataset3
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"Status": "Success", "Message": "Task inserted successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/ModifyTask", methods=["POST"])
@jwt_required()
def ModifyTask():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Admin":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403
    
        data = request.get_json()
        task_id = data.get("Id")
        category = data.get("Category")
        section = data.get("Section")
        code = data.get("Code")
        disease = data.get("Disease")
        datasets = data.get("Datasets")

        if not all([category, section, code, disease, datasets]):
            return jsonify({"Status": "Warning", "Message": "All required fields must be filled"}), 400

        duplicate = Tasks.query.filter(
            and_(
                Tasks.Category == category,
                Tasks.Section == section,
                Tasks.Code == code,
                Tasks.Disease == disease,
                Tasks.Id != task_id
            )
        ).first()

        if duplicate:
            return jsonify({"Status": "Warning", "Message": "A similar task already exists"}), 409
    
        task = Tasks.query.get_or_404(task_id)
        task.Category = category
        task.Section = section
        task.Code = code
        task.Disease = disease
        task.Dataset1 = datasets[0]
        task.Dataset2 = datasets[1] if datasets[1] else "" 
        task.Dataset3 = datasets[2] if datasets[2] else "" 

        db.session.commit()
        return jsonify({"Status": "Success", "Message": "Task modified successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

@app.route("/DeleteTask", methods=["POST"])
@jwt_required()
def DeleteTask():
    try:
        claims = get_jwt()
        if claims.get("Role") != "Admin":
            return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403
    
        data = request.get_json()
        task_id = data.get("Id")

        if not task_id:
            return jsonify({"Status": "Warning", "Message": "Task ID is required"}), 400

        task = Tasks.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return jsonify({"Status": "Success", "Message": "Task deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"Status": "Error", "Message": str(e)}), 500

# import csv
# from io import StringIO
# import zipfile
# import xml.etree.ElementTree as ET
# @app.route("/UploadExcel", methods=["POST"])
# @jwt_required()
# def UploadExcel():
#     try:
#         claims = get_jwt()
#         if claims.get("Role") != "Admin":
#             return jsonify({"Status": "Error", "Message": "Unauthorized"}), 403

#         if "Sheet" not in request.files:
#             return jsonify({"Status": "Warning", "Message": "No file uploaded"}), 400

#         file = request.files["Sheet"]
#         if file.filename == "":
#             return jsonify({"Status": "Warning", "Message": "No file selected"}), 400

#         required_columns = ["Category", "Section", "Code", "Disease", "Dataset1", "Dataset2", "Dataset3"]

#         # --- CASE 1: CSV File ---
#         if file.filename.lower().endswith(".csv"):
#             try:
#                 try:
#                     content = file.read().decode("utf-8")
#                 except UnicodeDecodeError:
#                     try:
#                         content = file.read().decode("cp1256")  # Arabic/Windows encoding
#                     except UnicodeDecodeError:
#                         content = file.read().decode("latin-1")  # generic fallback

#                 csv_data = csv.DictReader(StringIO(content))
#             except Exception as e:
#                 return jsonify({"Status": "Error", "Message": f"Invalid CSV file: {str(e)}"}), 400

#             if not set(required_columns).issubset(csv_data.fieldnames):
#                 return jsonify({
#                     "Status": "Warning",
#                     "Message": f"CSV must contain columns: {', '.join(required_columns)}"
#                 }), 400

#             rows = list(csv_data)

#         # --- CASE 2: XLSX File ---
#         elif file.filename.lower().endswith(".xlsx"):
#             try:
#                 rows = []
#                 with zipfile.ZipFile(BytesIO(file.read())) as z:
#                     # Load shared strings for cell values
#                     shared_strings = []
#                     if "xl/sharedStrings.xml" in z.namelist():
#                         root = ET.fromstring(z.read("xl/sharedStrings.xml"))
#                         for si in root.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
#                             text_parts = si.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
#                             shared_strings.append("".join([t.text for t in text_parts if t.text]))

#                     # Load first worksheet
#                     sheet_name = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet1")][0]
#                     root = ET.fromstring(z.read(sheet_name))
#                     ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

#                     # Extract rows
#                     sheet_rows = []
#                     for row in root.findall(".//main:row", ns):
#                         row_data = []
#                         for c in row.findall("main:c", ns):
#                             value = c.find("main:v", ns)
#                             if value is not None:
#                                 if c.attrib.get("t") == "s":
#                                     idx = int(value.text)
#                                     row_data.append(shared_strings[idx] if idx < len(shared_strings) else "")
#                                 else:
#                                     row_data.append(value.text)
#                             else:
#                                 row_data.append("")
#                         sheet_rows.append(row_data)

#                     # First row is header
#                     headers = sheet_rows[0]
#                     if not set(required_columns).issubset(headers):
#                         return jsonify({
#                             "Status": "Warning",
#                             "Message": f"Excel must contain columns: {', '.join(required_columns)}"
#                         }), 400

#                     # Convert to dict list
#                     for r in sheet_rows[1:]:
#                         rows.append(dict(zip(headers, r)))
#             except Exception as e:
#                 return jsonify({"Status": "Error", "Message": f"Invalid Excel file: {str(e)}"}), 400

#         else:
#             return jsonify({"Status": "Warning", "Message": "Only CSV or XLSX files are allowed"}), 400

#         # --- Insert into DB ---
#         inserted_count = 0
#         skipped_count = 0

#         for row in rows:
#             category = (row.get("Category") or "").strip()
#             section = (row.get("Section") or "").strip()
#             code = (row.get("Code") or "").strip()
#             disease = (row.get("Disease") or "").strip()
#             dataset1 = (row.get("Dataset1") or "").strip()
#             dataset2 = (row.get("Dataset2") or "").strip()
#             dataset3 = (row.get("Dataset3") or "").strip()

#             if not all([category, section, code, disease]):
#                 skipped_count += 1
#                 continue

#             duplicate = Tasks.query.filter_by(
#                 Category=category,
#                 Section=section,
#                 Code=code,
#                 Disease=disease
#             ).first()
#             if duplicate:
#                 skipped_count += 1
#                 continue

#             new_task = Tasks(
#                 Category=category,
#                 Section=section,
#                 Code=code,
#                 Disease=disease,
#                 Dataset1=dataset1,
#                 Dataset2=dataset2,
#                 Dataset3=dataset3
#             )
#             db.session.add(new_task)
#             inserted_count += 1

#         db.session.commit()

#         return jsonify({
#             "Status": "Success",
#             "Message": f"{inserted_count} tasks inserted, {skipped_count} skipped (duplicates or invalid)",
#             "Inserted": inserted_count,
#             "Skipped": skipped_count
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Status": "Error", "Message": str(e)}), 500