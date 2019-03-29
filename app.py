from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import sys, os
from EasyReply import EasyReply
from json import dumps
from flask import make_response

app = Flask(__name__)
api = Api(app)


er = EasyReply
train_data = pd.read_csv('singtel_qna.csv',header=None)
train_data.columns = ['Question','Answer']
faq_qns = pd.DataFrame({'FAQ Question':train_data['Question'], 'FAQ Answer':train_data['Answer']})
er = EasyReply(faq_qns)

def jsonify(status=200, indent=4, sort_keys=False, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

class Helper(Resource):
    def get(self, params):
        qn = params
        result = er.answer(qn)
        output_dict = {"Question": qn, "Answer": result}
        #### OUTPUT DICT ####
        return jsonify(**output_dict)
        

api.add_resource(Helper, '/question/<params>') # Help Route


if __name__ == '__main__':
     # For actual
    app.run(host="0.0.0.0")
    # app.run()


# Example:
# http://18.222.104.191/api/brand=Coca-cola&company=Coca-cola&category=None&competitors=None&country=us&startYear=2016&endYear=2017&API_Key=bapentagons