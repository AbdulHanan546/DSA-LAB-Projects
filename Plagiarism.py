import os
import re
from collections import Counter
from flask import Flask, request, jsonify

# Preprocessing functions
def clean_text(text):
    """
    Preprocess the text by removing special characters, converting to lowercase, and normalizing.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

def tokenize(text):
    """
    Tokenize the text into words.
    """
    return text.split()

# Similarity Measures
def jaccard_similarity(text1, text2):
    """
    Compute Jaccard similarity between two tokenized texts.
    """
    set1 = set(text1)
    set2 = set(text2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

def cosine_similarity(text1, text2):
    """
    Compute Cosine similarity between two tokenized texts.
    """
    counter1 = Counter(text1)
    counter2 = Counter(text2)
    all_items = set(counter1.keys()).union(counter2.keys())
    dot_product = sum(counter1[item] * counter2[item] for item in all_items)
    norm1 = sum(value ** 2 for value in counter1.values()) ** 0.5
    norm2 = sum(value ** 2 for value in counter2.values()) ** 0.5
    return dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0

# File comparison
def compare_files(file1, file2):
    """
    Compare two files and return similarity metrics.
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        text1 = clean_text(f1.read())
        text2 = clean_text(f2.read())
        tokens1 = tokenize(text1)
        tokens2 = tokenize(text2)
        return {
            "jaccard_similarity": jaccard_similarity(tokens1, tokens2),
            "cosine_similarity": cosine_similarity(tokens1, tokens2),
        }

# Flask Application
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plagiarism Detection System</title>
    </head>
    <body>
        <h1>Plagiarism Detection System</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="file1">Upload File 1:</label><br>
            <input type="file" name="file1" id="file1" required><br><br>
            <label for="file2">Upload File 2:</label><br>
            <input type="file" name="file2" id="file2" required><br><br>
            <button type="submit">Check Plagiarism</button>
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'Both files are required!', 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    file1_path = os.path.join('uploads', file1.filename)
    file2_path = os.path.join('uploads', file2.filename)

    os.makedirs('uploads', exist_ok=True)
    file1.save(file1_path)
    file2.save(file2_path)

    # Compare files
    result = compare_files(file1_path, file2_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
