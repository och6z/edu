import random

from flask import request
from flask_restful import Resource, reqparse, marshal

from app.resources import create_or_update_resource, delete_resource
from app.models import Student, Subject
from app.serializers import student_serializer


class StudentListAPI(Resource):
    """View all students; add new student
    URL: /api/v1/students
    Request methods: POST, GET
    """

    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        students = Student.query.filter_by(**kwargs).paginate(
                             page=page, per_page=limit, error_out=False)
        page_count = students.pages
        has_next = students.has_next
        has_previous = students.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/students?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/students?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        students = students.items

        output = {"students": marshal(students, student_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if students:
            return output
        else:
            return {"error": "Nincsenek regisztrált hallgatók. "
                             "Adjon hozzá egy újat!"}, 404

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "first_name",
            required=True,
            help="Kérjük, adja meg a keresztnevet.")
        parser.add_argument(
            "last_name",
            required=True,
            help="Kérjük, adja meg a vezetéknevet.")
        parser.add_argument(
            "email_address",
            required=True,
            help="Kérjük, adja meg az e-mail címet.")
        parser.add_argument(
            "minors",
            help="Válasszon több tárgyazonosítót vesszővel elválasztva.")
        args = parser.parse_args()
        first_name, last_name, email_address, minors = \
            args["first_name"], args["last_name"], args["email_address"], \
            args["minors"]
        student = Student(first_name=first_name,
                          last_name=last_name,
                          email_address=email_address,
                          student_id="ST" + str(random.randint(1, 999)))


        if minors:
            minors_list = [minor.strip() for minor in minors.split(',')]
            for subject_id in minors_list:
                try:
                    minor = Subject.query.get(subject_id)
                    if minor:
                        student.minors.append(minor)
                    else:
                        return {"error": "Egy vagy több tárgyazonosító "
                                "érvénytelen."}, 400
                except:
                    return {"error": "Tartalmaznia kell "
                            "vesszővel elválasztott egész számok."}, 400
        return create_or_update_resource(
            resource=student,
            resource_type="student",
            serializer=student_serializer,
            create=True)


class StudentAPI(Resource):
    """View, update and delete a single student.
    URL: /api/v1/students/<id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            return marshal(student, student_serializer)
        else:
            return {"error": "Hallgatói azonosító " + id + " "
                             "nem létezik."}, 404

    def put(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            parser = reqparse.RequestParser()
            parser.add_argument("first_name")
            parser.add_argument("last_name")
            parser.add_argument("email_address")
            parser.add_argument("minors")
            args = parser.parse_args()

            for field in args:
                if args[field] is not None:
                    if field == "minors":
                        # Clear the student's list of minors
                        for subject in student.minors:
                            subject.minor_students.remove(student)
                        student.minors = []
                        minors = args["minors"]
                        minors_list = [minor.strip() for minor in
                                       minors.split(',')]
                        # Append new minors into list
                        if minors_list != ['']:
                            for subject_id in minors_list:
                                try:
                                    minor = Subject.query.get(subject_id)
                                    if minor:
                                        student.minors.append(minor)
                                    else:
                                        return {"error": "Egy vagy több tantárgy "
                                                "azonosítója "
                                                "érvénytelen."}, 400
                                except:
                                    return {"error": "A tantárgyak mező "
                                            "csak a tárgyazonosítót tartalmazza "
                                            "vesszővel elválasztva."}, 400
                    elif field == "email_address":
                        return {"error": "Nem frissítheti az e-mail címet "
                                "field."}, 400
                    else:
                        updated_field = args[field]
                        setattr(student, field, updated_field)
        else:
            return {"error": "A hallgatói azonosító " + id + " "
                             "nem létezik."}, 404

        return create_or_update_resource(
            resource=student,
            resource_type="student",
            serializer=student_serializer,
            create=False)

    def delete(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            return delete_resource(resource=student,
                                   resource_type="student",
                                   id=id)
        else:
            return {"error": "A hallgatói azonosító " + id + " "
                             "nem létezik."}, 404
