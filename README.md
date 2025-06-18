# kv_store
A Python-based distributed key-value store using vector clocks to ensure causal consistency. Nodes sync updates in order, even with delays, using Docker and Flask microservices.
This project demonstrates a distributed key-value store that ensures causal consistency using Vector Clocks. Built entirely in Python and containerized with Docker and Docker Compose, the system simulates a network of three nodes that coordinate to maintain the causal order of operations across distributed state.

Each node runs an HTTP server using Flask, maintaining its own local key-value store and a vector clock that tracks the partial ordering of events. When a write operation occurs, the node updates its clock, stores the data, and propagates the write along with the updated vector clock to other nodes. Upon receiving a message, a node checks if it has all the causal dependencies needed to apply that operation. If not, the message is buffered until its dependencies are fulfilled.

The system includes a client script that initializes all nodes and runs a test scenario where one node writes a value, another node reads and then writes a dependent value. This setup validates the causal consistency by ensuring dependent operations are applied only after their prerequisites.

This project highlights fundamental distributed systems concepts like event ordering, vector clocks, and causal message delivery, providing a solid foundation for building more complex distributed applications.
