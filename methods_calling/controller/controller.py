import json
from pyramid.response import Response
from app.base.api.main import Resource
from app.utils import CommonUtils
from methods_calling.models import session, Jobs
from sqlalchemy import insert

class CreateJob(Resource):

    def put(self):

        payload = self.escaped_json
        response = {"message": "Successfully created", "status": 201}
        try:
            name = payload['name']
            import pdb;pdb.set_trace()
        except KeyError as e:
            response['status'] = 400
            response['message'] = "No name found in the payload"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")
        else:
            # put name in RAM
            random_id = CommonUtils.get_uuid_with_timestamp()
            try:
                insert_json = {"job_id": random_id, "job_name": name}
                ins = insert(Jobs)
                ins = ins.values([insert_json])
                session.execute(ins)
                return Response(body=json.dumps(response), status=response['status'], content_type="application/json")
            except Exception as e:
                session.rollback()
                response['status'] = 500
                response['message'] = "Internal Server Error"
                return Response(body=json.dumps(response), status=response['status'], content_type="application/json")

class DetailGetter(Resource):

    def get(self):
        response = {"message": "", "status": 200, "payload": ""}
        try:
            query_string  = self.escaped_params
            job_id = query_string.get('job_id')
            job = session.query(Jobs).filter(Jobs.job_id == job_id).all()
            if job is not None and job.job_name is not None:
                response['payload'] = {"name": job.job_name, "id": job_id}
            else:
                response['status'] = 404
                response['message'] = "No Job Found"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")

        except Exception as e:
            response['status'] = 500
            response['message'] = "Internal Server Error"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")


    def delete(self):
        response = {"message": "SuccessFully Deleted", "status": 200, "payload": ""}
        try:
            query_string = self.escaped_params
            job_id = query_string.get('job_id')
            job = session.query(Jobs).filter(Jobs.job_id == job_id).all()
            if job is not None and job.job_name is not None:
                job.delete()
            else:
                response['status'] = 404
                response['message'] = "No Job Found"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")

        except Exception as e:
            response['status'] = 500
            response['message'] = "Internal Server Error"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")


class UpdateJob(Resource):

    def post(self):
        response = {"message": "SuccessFully Updated", "status": 200, "payload": ""}
        try:
            query_string = self.escaped_params
            job_id = query_string.get('job_id')
            job_name = query_string.get('job_name')
            job = session.query(Jobs).filter(Jobs.job_id == job_id).all()
            if job is not None and job.job_name is not None:
                job.update({"job_name":job_name})
                session.commit()
            else:
                response['status'] = 404
                response['message'] = "No Job Found"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")

        except Exception as e:
            response['status'] = 500
            response['message'] = "Internal Server Error"
            return Response(body=json.dumps(response), status=response['status'], content_type="application/json")