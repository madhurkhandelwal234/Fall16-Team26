from flask import Flask, request, Response, jsonify, json
from prerequiste import Prerequisite
from corequiste_db import Corequisite
from prerequiste import db

def validPrereqCourse(courses_selected, pre_req):
    prereq_not_found =  True
    for i, course in enumerate(courses_selected):
        if (pre_req.prereq_course in course):
            prereq_not_found = False
            break;

    if prereq_not_found:
        return False
        

    for k, course in enumerate(courses_selected):
        if (pre_req.primary_course in course):
          break;

    if i >= k:
      return False;
    return True

def validCoreqCourse(courses_selected, co_req):
    coreq_not_found  = True
    for i, course in enumerate(courses_selected):
        if (co_req.coreq_course) in course:
           coreq_not_found = False
           break;
    if coreq_not_found:
        return False

    for k, course in enumerate(courses_selected):
        if (co_req.primary_course) in course:
           break;

    if i > k:
      return False;
    return True


app = Flask(__name__)
@app.route('/prerequisite_check', methods=['POST'])
def create_expense():

    #if request.is_json:
    args = request.get_json(silent=True)
    #else:
    #  args = json.loads(request.data)
    data_out = {}
    courses = args["course_list"]
    course_in_list = []
    for course in courses:
        course_in_list.extend(course)
    print course_in_list
    prereq_list =  Prerequisite.query.filter(Prerequisite.primary_course.in_(course_in_list)).all()
    coreq_list =  Corequisite.query.filter(Corequisite.primary_course.in_(course_in_list)).all()
    
    for course in prereq_list:
      if not (validPrereqCourse(course_in_list, course)):
        if not (str(course.primary_course + "WhichViolates_prereq") in data_out.keys()):
           data_out[course.primary_course + "WhichViolates_prereq"] = [course.prereq_course]
        else:
           data_out[course.primary_course + "WhichViolates_prereq"].append(course.prereq_course)



    for course in coreq_list:
      if  not (validCoreqCourse(course_in_list, course)):
        if not (str(course.primary_course + "WhichViolates_coreq") in data_out.keys()):
           data_out[course.primary_course + "WhichViolates_coreq"] = [course.coreq_course]
        else:
           data_out[course.primary_course + "WhichViolates_coreq"].append(course.coreq_course)

    resp = Response(status=201, mimetype='application/json')
    resp.data = json.dumps(data_out)
    return resp

#@app.route('/v1/expenses/<expense_id>', methods=['GET'])
#def get_expense(expense_id):
#    expense =  Expense.query.get(expense_id)
#    print expense_id
#    if expense is not None:
#        resp = Response(status=200, mimetype='application/json')
#        resp.data = json.dumps(expense.toJson)
#    else:
#        resp = Response(status=404)
#    return resp

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
