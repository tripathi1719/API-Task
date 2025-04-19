from flask import Flask, request, jsonify

app = Flask(__name__)

# Distance cost between centers and L1
distance_cost = {
    "C1": {"L1": 10, "C2": 10, "C3": 20},
    "C2": {"L1": 15, "C1": 10, "C3": 15},
    "C3": {"L1": 20, "C1": 20, "C2": 15},
    "L1": {"C1": 10, "C2": 15, "C3": 20},
}

# Inventory map for each center
inventory = {
    "C1": {"A", "B", "C", "G"},
    "C2": {"B", "C", "D", "F", "H"},
    "C3": {"C", "D", "E", "G", "H", "I"},
}

# All centers
centers = ["C1", "C2", "C3"]

def get_product_centers(product):
    return [center for center, items in inventory.items() if product in items]

def calculate_cost(order, start_center):
    from itertools import permutations

    # Determine what centers are needed to fulfill the order
    needed_centers = set()
    for product in order:
        for center in get_product_centers(product):
            needed_centers.add(center)

    if start_center not in needed_centers:
        needed_centers.add(start_center)

    needed_centers = list(needed_centers)
    needed_centers.remove(start_center)

    min_total_cost = float('inf')

    for path in permutations(needed_centers):
        route = [start_center] + list(path)
        total_cost = 0

        for i in range(len(route)):
            from_center = route[i]
            to = "L1" if i == len(route) - 1 else route[i + 1]
            total_cost += distance_cost[from_center][to]

        # Drop to L1 after each center
        total_cost += len(route) * distance_cost["L1"][route[-1]]

        if total_cost < min_total_cost:
            min_total_cost = total_cost

    return min_total_cost

@app.route('/calculate', methods=['POST'])
def calculate_delivery_cost():
    order = request.get_json()

    if not order:
        return jsonify({"error": "Invalid input format"}), 400

    min_cost = float('inf')

    for center in centers:
        cost = calculate_cost(order, center)
        if cost < min_cost:
            min_cost = cost

    return jsonify({"minimum_cost": min_cost})

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)

