from flask import Flask, render_template, jsonify, request
import random
import string
import os
app = Flask(__name__)
# Game state - stored in memory
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
    """Generate a new food position and letter"""
    attempts = 0
    while attempts < 100:  # Prevent infinite loop
        pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if pos not in game_state['snake']:
            break
        attempts += 1
    if attempts >= 100:
        # If we can't find a free position, game over
        pos = (0, 0)
    letter = random.choice(string.ascii_uppercase)
    return pos, letter
def reset_game():
    """Reset the game to initial state"""
    global game_state
    game_state = {
        'snake': [(5, 5)],
        'direction': 'RIGHT',
        'food_pos': (10, 10),
        'food_letter': 'A',
        'collected_letters': [],
        'game_over': False,
        'score': 0
    }
    # Generate first food
    game_state['food_pos'], game_state['food_letter'] = get_new_letter()
@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')
@app.route('/api/game_state')
def get_game_state():
    """Get current game state"""
    return jsonify(game_state)
@app.route('/api/move', methods=['POST'])
def move():
    """Move the snake"""
    if game_state['game_over']:
        return jsonify(game_state)
    try:
        data = request.get_json()
        new_direction = data.get('direction') if data else None
        # Prevent reverse direction
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction and new_direction in DIRECTIONS and new_direction != opposite.get(game_state['direction']):
            game_state['direction'] = new_direction
        # Move snake
        dx, dy = DIRECTIONS[game_state['direction']]
        head_x, head_y = game_state['snake'][0]
        new_head = (head_x + dx, head_y + dy)
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            game_state['game_over'] = True
            return jsonify(game_state)
        # Check self collision
        if new_head in game_state['snake']:
            game_state['game_over'] = True
            return jsonify(game_state)
        game_state['snake'].insert(0, new_head)
        # Check food collision
        if new_head == game_state['food_pos']:
            game_state['collected_letters'].append(game_state['food_letter'])
            game_state['score'] += 10
            game_state['food_pos'], game_state['food_letter'] = get_new_letter()
        else:
            game_state['snake'].pop()  # Remove tail
    except Exception as e:
        print(f"Error in move: {e}")
    return jsonify(game_state)
@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the game"""
    reset_game()
    return jsonify(game_state)
@app.route('/health')
def health():
    """Health check endpoint"""
    return "OK"
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return "Page not found. Go to the main page: <a href='/'>Play Snake Game</a>", 404
if __name__ == '__main__':
    # Initialize the game
    reset_game()
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 10000))
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
