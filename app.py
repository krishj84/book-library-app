from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# File to store the inventory
INVENTORY_FILE = 'inventory.json'

# Load inventory from file
def load_inventory():
    import os, json
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as file:
            return json.load(file)
    return []

# Save inventory to file
def save_inventory(inventory):
    import json
    with open(INVENTORY_FILE, 'w') as file:
        json.dump(inventory, file, indent=4)

# Initialize inventory list
inventory = load_inventory()

@app.route('/')
def home():
    """Home page with options."""
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """Add a book to the inventory."""
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        language = request.form['language']
        bookshelves = int(request.form['bookshelves'])

        # Add book to inventory
        inventory.append({
            'title': title,
            'author': author,
            'language': language,
            'bookshelves': bookshelves
        })

        # Save inventory to file
        save_inventory(inventory)

        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    """Search for books in the inventory."""
    results = []
    search_criteria = ''
    if request.method == 'POST':
        query = request.form['query'].lower()
        search_criteria = request.form['criteria']
        if search_criteria == 'title':
            results = [book for book in inventory if query in book['title'].lower()]
        elif search_criteria == 'author':
            results = [book for book in inventory if query in book['author'].lower()]
        elif search_criteria == 'language':
            results = [book for book in inventory if query in book['language'].lower()]
        elif search_criteria == 'bookshelves':
            results = [book for book in inventory if query in book['bookshelves'].lower()]

    return render_template('search_book.html', results=results, criteria=search_criteria)

@app.route('/delete/<isbn>', methods=['POST'])
def delete_book(isbn):
    """Delete a book by ISBN."""
    global inventory
    inventory = [book for book in inventory if book['isbn'] != isbn]
    save_inventory(inventory)
    return redirect(url_for('search_book'))

@app.route('/inventory', methods=['GET'])
def view_inventory():
    """View the entire inventory."""
    return jsonify(inventory)

if __name__ == '__main__':
    app.run(debug=True,port=8082)
