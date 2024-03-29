from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method =='GET':
        messages = Message.query.all()
        message_list = [message.to_dict() for message in messages]
        return make_response(message_list,200)
    elif request.method =='POST':
       # ipdb.set_trace()
        incoming = request.json
        new_message = Message(**incoming)
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(),201)

@app.route('/messages/<int:id>', methods=['GET','PATCH','POST','DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'GET':
        return make_response(message.to_dict(),200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response({},204)
    elif request.method =='PATCH':
        try:
            incoming = request.json
            print(incoming)
            for attr in incoming:
                setattr(message,attr,incoming[attr])
                db.session.commit()
                return make_response(message.to_dict(),202)
        except:
                return make_response({"errors": ["validation errors"]},400)
        else:
            return make_response({ "error": "Power not found"},404)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
