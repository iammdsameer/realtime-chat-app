from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/room', methods=['POST'])
def room():
    username = request.form['username']
    room = request.form['room']
    if username and room:
        return render_template('room.html', username=username, room=room)
    else:
        return redirect(url_for('index'))


@socketio.on('join_room')
def on_join(data):
    join_room(data['room'])
    socketio.emit('broadcast', data)


@socketio.on('send')
def on_send(data):
    socketio.emit('receive', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
