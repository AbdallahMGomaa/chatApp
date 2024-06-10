import threading
import time
import requests
import websocket
import argparse
import json
import signal
import sys


websocket_thread = None
send_message_thread = None


def on_message(ws, message):
    msg_json = json.loads(message)
    msg_content = msg_json['message']['content']
    msg_sender = msg_json['message']['sender_username']
    msg_timestamp = msg_json['message']['timestamp']
    print(f"{msg_timestamp}, {msg_sender}: {msg_content}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    if websocket_thread:
        websocket_thread.join()
    if send_message_thread:
        send_message_thread.join()
    print(f"Closed connection with status: {close_status_code}, message: {close_msg}")


def on_open(ws):
    print("Connection opened")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='user', action='store', type=str, help='Username')
    parser.add_argument('--password', dest='password', action='store', type=str, help='Password')
    args = parser.parse_args()
    response = requests.post(
        'http://localhost:8000/auth/token/',
        json={
            'username': args.user,
            'password': args.password
        }
    )
    token = response.json()['access']
    ws = websocket.WebSocketApp(
        'ws://localhost:8000/ws/chat/',
        header={'Authorization': 'Bearer ' + token},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )


    def run_websocket():
        ws.run_forever()


    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()


    def send_user_message():
        while True:
            receiver = input("Enter receiver username: ")
            message = input("Enter message: ")
            message = json.dumps({
                "receiver": receiver,
                "content": message
            })
            ws.send(message)

    time.sleep(2)

    send_message_thread = threading.Thread(target=send_user_message)
    send_message_thread.start()

    def signal_handler(sig, frame):
        print('inside signal handler')
        send_message_thread.join()
        websocket_thread.join()
        # ws.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('press Ctrl+C to exit')
