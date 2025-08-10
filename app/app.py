from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow your HTML file to make requests
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    """
    API endpoint to receive a sentence and return the word count.
    """
    if request.method == "GET":
        # Serve the index.html file from the templates folder
        return render_template("index.html")
    
    elif request.method == "POST":
        try:
            # Get the JSON data from the request
            data = request.json
            sentence = data.get('sentence', '')
            
            # Simple word counting logic
            word_list = sentence.split()
            word_count = len(word_list)
            
            # Return the result as a JSON response
            return jsonify({'word_count': word_count})

        except Exception as e:
            # Return an error message if something goes wrong
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)