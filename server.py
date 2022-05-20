from flask import Flask, request

app = Flask(__name__)

from dialogue.manager import DialogueManager

dm = None

@app.route('/')
def root():
    return '<h1>👨🏻‍💻</h1>'

@app.route('/47GMLwf7jfmesjwnQAKC/start')
def start():
    dm = DialogueManager()
    dm.start_dialogue()
    return 'Started', 200

@app.route('/47GMLwf7jfmesjwnQAKC/utter')
def utter():
    return dm.run_state(request.get_data())


if __name__ == "__main__":
    app.run(debug=True)