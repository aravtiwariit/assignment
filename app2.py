from flask import Flask, request, jsonify
import math
from itertools import permutations

app = Flask(__name__)
@app.route('/')
def home():
    return "<h1> Hello it's me  'Arav Tiwari'  From PSIT Kanpur </h1>"
center_products = {
    'C1': {'A': 3, 'B': 2, 'C': 8},
    'C2': {'D': 12, 'E': 25, 'F': 15},
    'C3': {'G': 0.5, 'H': 1, 'I': 2}
}
center_distances = {'C1': 3, 'C2': 2.5, 'C3': 2}

def calculate_cost(weight, distance):
    if weight <= 5:
        return 10 * distance
    else:
        additional = math.ceil((weight - 5) / 5) * 8
        return (10 + additional) * distance

def minimal_cost(order):
    centers_needed = {}
    for product, qty in order.items():
        for center, products in center_products.items():
            if product in products:
                if center not in centers_needed:
                    centers_needed[center] = 0
                centers_needed[center] += products[product] * qty
                break

    if not centers_needed:
        return 0

    min_cost = float('inf')

   
    for perm in permutations(centers_needed.keys()):
        
        for i in range(len(perm)):
            total_cost = 0
            current_weight = 0
            current_location = perm[i]

            
            pickup_weight = centers_needed[current_location]
            current_weight += pickup_weight
            distance = center_distances[current_location]
            total_cost += calculate_cost(current_weight, distance)

            current_weight = 0
            for center in perm[:i] + perm[i+1:]:
                distance = center_distances[center]
                total_cost += calculate_cost(0, distance)

                pickup_weight = centers_needed[center]
                current_weight += pickup_weight

                distance = center_distances[center]
                total_cost += calculate_cost(current_weight, distance)

              
                current_weight = 0

           
            if total_cost < min_cost:
                min_cost = total_cost

    return min_cost

@app.route('/calculate', methods=['POST'])
def calculate():
    order = request.get_json()
   
    filtered_order = {k: int(v) for k, v in order.items() if v > 0}
    cost = minimal_cost(filtered_order)
    return jsonify({'cost': cost})

@app.route('/',methods = ['GET'])
def showMessage():
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)