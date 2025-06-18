
class VectorClock:
    def __init__(self, node_id, all_nodes):
        self.clock = {node: 0 for node in all_nodes}
        self.node_id = node_id

    def increment(self):
        self.clock[self.node_id] += 1

    def update(self, received_clock):
        for node, timestamp in received_clock.items():
            self.clock[node] = max(self.clock[node], timestamp)
        self.increment()

    def is_causally_ready(self, received_clock):
        for node, timestamp in received_clock.items():
            if node == self.node_id:
                continue
            if timestamp > self.clock.get(node, 0):
                return False
        return True

    def get_clock(self):
        return self.clock.copy()
