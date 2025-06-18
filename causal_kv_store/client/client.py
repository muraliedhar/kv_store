
import requests
import time

nodes = ['localhost:5001', 'localhost:5002', 'localhost:5003']
node_ids = ['node1', 'node2', 'node3']

# Initialize all nodes
for i, node in enumerate(nodes):
    requests.post(f'http://{node}/init', json={
        'node_id': node_ids[i],
        'all_nodes': node_ids
    })

# Simulate causal write: node1 writes -> node2 reads -> node2 writes
print("Node1 writing key=a, value=1")
requests.post(f'http://{nodes[0]}/put', json={'key': 'a', 'value': '1'})

time.sleep(2)  # simulate delay

print("Node2 writing key=b, value=2 (causally depends on 'a')")
requests.post(f'http://{nodes[1]}/put', json={'key': 'b', 'value': '2'})
