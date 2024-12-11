from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Sample word list
word_list = ['python', 'flask', 'html', 'css', 'javascript', 'web', 'flask', 'backend', 'frontend']

# Crossword grid dimensions
GRID_SIZE = 10

# Create a simple 2D grid with empty cells
def create_grid():
    return [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to check if a word can be placed horizontally
def can_place_word_horizontally(grid, word, row, col):
    if col + len(word) > GRID_SIZE:
        return False
    for i in range(len(word)):
        if grid[row][col + i] != '' and grid[row][col + i] != word[i]:
            return False
    return True

# Function to place a word horizontally
def place_word_horizontally(grid, word, row, col):
    for i in range(len(word)):
        grid[row][col + i] = word[i]

# Function to check if a word can be placed vertically
def can_place_word_vertically(grid, word, row, col):
    if row + len(word) > GRID_SIZE:
        return False
    for i in range(len(word)):
        if grid[row + i][col] != '' and grid[row + i][col] != word[i]:
            return False
    return True

# Function to place a word vertically
def place_word_vertically(grid, word, row, col):
    for i in range(len(word)):
        grid[row + i][col] = word[i]

# Function to generate a crossword puzzle
def generate_crossword(word_list):
    grid = create_grid()
    for word in word_list:
        placed = False
        while not placed:
            direction = random.choice(['horizontal', 'vertical'])
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if direction == 'horizontal' and can_place_word_horizontally(grid, word, row, col):
                place_word_horizontally(grid, word, row, col)
                placed = True
            elif direction == 'vertical' and can_place_word_vertically(grid, word, row, col):
                place_word_vertically(grid, word, row, col)
                placed = True
    return grid

# Route to generate a new crossword puzzle
@app.route('/new_puzzle', methods=['GET'])
def new_puzzle():
    grid = generate_crossword(word_list)
    return jsonify(grid)

# Route to serve the main game page
@app.route('/')
def index():
    return render_template('base.html')

# Route to submit answers (for validation)
@app.route('/submit', methods=['POST'])
def submit():
    answers = request.json['answers']
    # Add answer validation logic here
    return jsonify({"message": "Answers submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
