from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
socketio = SocketIO(app)
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    content = data['content']
    message = Message(content=content)
    db.session.add(message)
    db.session.commit()
    socketio.emit('message', {'content': content}, broadcast=True)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0')