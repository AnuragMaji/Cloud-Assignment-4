from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask import Flask, request, jsonify, send_file, send_from_directory
from json import dumps
import random
import datetime as datetime
from datetime import timedelta
from flask_restful.utils import cors

e = create_engine('sqlite:///weatherdata.db')

app = Flask(__name__)
weather = Api(app)
weather.decorators=[cors.crossdomain(origin='*')]


class Historical(Resource):
    def get(self):
        connection = e.connect()
        query = connection.execute("select * from weather")
        outputlist = []
        for i in query.cursor.fetchall():
            entry = {}
            entry["DATE"] = str(i[0])
            outputlist.append(entry)

        return outputlist

    def post(self):
        date = request.json['DATE']
        maxtemp = request.json['TMAX']
        mintemp = request.json['TMIN']
        connection = e.connect()
        query = connection.execute("insert into weather values('%s', '%s', %s)" %(date, str(maxtemp), str(mintemp)))

        return {'DATE': date, 'TMAX':maxtemp, 'TMIN':mintemp}


class Date(Resource):
    def get(self, date_id):
        connection = e.connect()
        query = connection.execute("select * from weather where DATE='%s'" % date_id)
        outputlist = {}
        for i in query.cursor.fetchall():
            outputlist["DATE"] = str(i[0])
            outputlist["TMAX"] = float(i[1])
            outputlist["TMIN"] = float(i[2])
        return outputlist


    def delete(self,date_id):
        connection = e.connect()
        query = connection.execute("delete from weather where DATE='%s'" % date_id)


class Forecast(Resource):
    def get(self, date_id):
        ok = []
        for i in range (0,7):
            date = datetime.datetime.strptime(date_id, '%Y%m%d') + timedelta(days=i)
            date = date.replace(year = 2014)
            m = int(date_id)
            m = m + i

            date = date.strftime('%Y%m%d')
            connection = e.connect()
            query = connection.execute("select * from weather where DATE='%s'" % date)
            outputlist = {}
            for i in query.cursor.fetchall():
                outputlist["DATE"] = m
                outputlist["TMAX"] = float(i[1])
                outputlist["TMIN"] = float(i[2])
            #return outputlist
            ok.append(outputlist)
            return ok



weather.add_resource(Historical, '/historical/')
weather.add_resource(Date, '/historical/<string:date_id>')
weather.add_resource(Forecast, '/forecast/<string:date_id>')

@app.route("/")
def main():
    return send_file('./static/index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()