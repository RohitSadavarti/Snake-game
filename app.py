from flask import Flask, render_template, jsonify, request
import random
import string

app = Flask(__name__)

# Game state
game_state = {
    'snake': [(5, 5)],
    'direction': 'RIGHT',
    'food_pos': (10, 10),
    'food_letter': 'A',
    'collected_letters': [],
    'game_over': False,
    'score': 0
}

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

WIDTH, HEIGHT = 32, 24  # Grid size (32x24 cells)

def get_new_letter():
    while True:
        pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if pos not in game_state['snake']:
            break
    letter = random.choice(string.ascii_uppercase)
    return pos, letter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def get_game_state():
    return jsonify(game_state)

@app.route('/move', methods=['POST'])
def move():
    if game_state['game_over']:
        return jsonify(game_state)
    
    data = request.json
    new_direction = data.get('direction')
    
    # Prevent reverse direction
    opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
    if new_direction and new_direction != opposite.get(game_state['direction']):
        game_state['direction'] = new_direction
    
    # Move snake
    dx, dy = DIRECTIONS[game_state['direction']]
    head_x, head_y = game_state['snake'][0]
    new_head = (head_x + dx, head_y + dy)
    
    # Check collision
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in game_state['snake']):
        game_state['game_over'] = True
        return jsonify(game_state)
    
    game_state['snake'].insert(0, new_head)
    
    # Check food collision
    if new_head == game_state['food_pos']:
        game_state['collected_letters'].append(game_state['food_letter'])
        game_state['score'] += 10
        game_state['food_pos'], game_state['food_letter'] = get_new_letter()
    else:
        game_state['snake'].pop()
    
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = {
        'snake': [(5, 5)],
        'direction': 'RIGHT',
        'food_pos': (10, 10),
        'food_letter': random.choice(string.ascii_uppercase),
        'collected_letters': [],
        'game_over': False,
        'score': 0
    }
    game_state['food_pos'], game_state['food_letter'] = get_new_letter()
    return jsonify(game_state)

if __name__ == '__main__':
    # Initialize first food
    game_state['food_pos'], game_state['food_letter'] = get_new_letter()
    app.run(host='0.0.0.0', port=10000)
