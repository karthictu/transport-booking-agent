import os

from signal import signal, SIGINT
from flask import Flask, render_template, request, jsonify
from agents import OrchestratorAgent

def handler(signal_received, frame):
    # SIGINT or  ctrl-C detected, exit without error
    exit(0)

app = Flask(__name__)
orchestrator = OrchestratorAgent()

@app.route('/')
def index():
    """Return the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the chat message from the user."""
    user_message = request.json.get("message")
    response = orchestrator.handle_message(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    signal(SIGINT, handler)
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
