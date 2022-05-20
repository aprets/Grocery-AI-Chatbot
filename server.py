from flask import Flask, request

app = Flask(__name__)

from dialogue.manager import DialogueManager

global dm
dm = None

@app.route('/')
def root():
    return '<h1>👨🏻‍💻</h1>'

@app.route('/47GMLwf7jfmesjwnQAKC/start', methods = ['POST'])
def start():
    global dm
    print(dm)
    dm = DialogueManager()
    dm.start_dialogue()
    return 'Started', 200

@app.route('/47GMLwf7jfmesjwnQAKC/utter', methods = ['POST'])
def utter():
    global dm
    print(dm)
    return dm.run_state(request.data.decode())


if __name__ == "__main__":
    app.run(debug=True)