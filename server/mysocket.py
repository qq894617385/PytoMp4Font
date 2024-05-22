from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import uuid

client_sessions = {}
socketio = None


def init_webSocket(app):
    app.config['SECRET_KEY'] = 'your_secret_key'

    global socketio

    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    @socketio.on('connect')
    def handle_connect():
        custom_sid = str(uuid.uuid4())  # 生成一个唯一的SID
        client_sessions[custom_sid] = {"username": "User's identifier"}
        emit('assign sid', {'custom_sid': custom_sid})  # 将这个SID发送给客户端

    @socketio.on('disconnect')
    def handle_disconnect():
        # 从会话池中移除SID
        for sid, session in client_sessions.items():
            if session["socket_sid"] == request.sid:
                client_sessions.pop(sid)
                break

    @socketio.on('register sid')
    def register_sid(data):
        print(data['custom_sid'])
        custom_sid = data['custom_sid']
        print(client_sessions)
        if custom_sid in client_sessions:
            client_sessions[custom_sid]["socket_sid"] = request.sid  # 关联Socket.IO的自动SID


def get_socketio():
    return socketio
