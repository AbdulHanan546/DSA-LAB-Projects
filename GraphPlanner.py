import heapq
from flask import Flask, request, jsonify
import os

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, from_node, to_node, weight):
        self.graph[from_node].append((to_node, weight))
        self.graph[to_node].append((from_node, weight))  # For undirected graph

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        predecessors = {node: None for node in self.graph}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = end
        while current:
            path.insert(0, current)
            current = predecessors[current]

        return {
            "distance": distances[end],
            "path": path
        }

# Flask Application
app = Flask(__name__)
graph = Graph()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Travel Planner</title>
    </head>
    <body>
        <h1>Travel Planner</h1>
        <form action="/add-node" method="post">
            <label for="node">Add Location:</label><br>
            <input type="text" name="node" id="node" required><br><br>
            <button type="submit">Add Location</button>
        </form>
        <br>
        <form action="/add-edge" method="post">
            <label for="from_node">From Location:</label><br>
            <input type="text" name="from_node" id="from_node" required><br>
            <label for="to_node">To Location:</label><br>
            <input type="text" name="to_node" id="to_node" required><br>
            <label for="weight">Distance (km):</label><br>
            <input type="number" name="weight" id="weight" required><br><br>
            <button type="submit">Add Route</button>
        </form>
        <br>
        <form action="/plan-route" method="post">
            <label for="start">Start Location:</label><br>
            <input type="text" name="start" id="start" required><br>
            <label for="end">End Location:</label><br>
            <input type="text" name="end" id="end" required><br><br>
            <button type="submit">Plan Route</button>
        </form>
    </body>
    </html>
    '''

@app.route('/add-node', methods=['POST'])
def add_node():
    node = request.form['node']
    graph.add_node(node)
    return f"Location '{node}' added successfully!"

@app.route('/add-edge', methods=['POST'])
def add_edge():
    from_node = request.form['from_node']
    to_node = request.form['to_node']
    weight = float(request.form['weight'])
    graph.add_edge(from_node, to_node, weight)
    return f"Route from '{from_node}' to '{to_node}' with distance {weight} km added successfully!"

@app.route('/plan-route', methods=['POST'])
def plan_route():
    start = request.form['start']
    end = request.form['end']

    if start not in graph.graph or end not in graph.graph:
        return f"One or both locations ('{start}', '{end}') do not exist in the graph!", 400

    result = graph.dijkstra(start, end)
    if result["distance"] == float('inf'):
        return f"No route exists between '{start}' and '{end}'!"

    return jsonify({
        "distance": result["distance"],
        "path": result["path"]
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
