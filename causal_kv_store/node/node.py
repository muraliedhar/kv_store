
from flask import Flask, request, jsonify
from vector_clock import VectorClock
import threading
import requests
import time

app = Flask(__name__)
store = {}
buffer = []
node_id = None
all_nodes = []
vector_clock = None

@app.route('/init', methods=['POST'])
def init():
    global node_id, all_nodes, vector_clock
    data = request.json
    node_id = data['node_id']
    all_nodes = data['all_nodes']
    vector_clock = VectorClock(node_id, all_nodes)
    return "Initialized", 200

@app.route('/put', methods=['POST'])
def put():
    data = request.json
    key, value = data['key'], data['value']
    vector_clock.increment()
    store[key] = value
    propagate_write(key, value, vector_clock.get_clock())
    return jsonify(clock=vector_clock.get_clock()), 200

@app.route('/propagate', methods=['POST'])
def propagate():
    data = request.json
    key, value, sender_clock = data['key'], data['value'], data['clock']
    if vector_clock.is_causally_ready(sender_clock):
        vector_clock.update(sender_clock)
        store[key] = value
    else:
        buffer.append(data)
    return '', 200

def propagate_write(key, value, clock):
    for node in all_nodes:
        if node != node_id:
            try:
                requests.post(f'http://{node}:5000/propagate', json={
                    'key': key, 'value': value, 'clock': clock
                })
            except Exception:
                pass

def buffer_checker():
    while True:
        for msg in buffer[:]:
            if vector_clock.is_causally_ready(msg['clock']):
                vector_clock.update(msg['clock'])
                store[msg['key']] = msg['value']
                buffer.remove(msg)
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=buffer_checker, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
