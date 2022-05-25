from flask import Flask, request

app = Flask(__name__)

from dialogue.manager import DialogueManager

global dm
dm = None

header = "oooooooooo.             o8o               .oooooo..o                                                              o8o "+ \
"`888'   `Y8b            `\"'              d8P'    `Y8                                                              `YP "+ \
" 888     888  .oooo.   oooo  ooo. .oo.   Y88bo.      oooo  oooo  oooo d8b oooo d8b  .ooooo.  oooo    ooo  .oooo.o  '  "+ \
" 888oooo888' `P  )88b  `888  `888P\"Y88b   `\"Y8888o.  `888  `888  `888""8P `888\"\"8P d88' `88b  `88.  .8'  d88(  \"8     "+ \
" 888    `88b  .oP\"888   888   888   888       `\"Y88b  888   888   888      888     888ooo888   `88..8'   `\"Y88b.      "+ \
" 888    .88P d8(  888   888   888   888  oo     .d8P  888   888   888      888     888    .o    `888'    o.  )88b     "+ \
"o888bood8P'  `Y888""8o o888o o888o o888o 8""88888P'   `V88V\"V8P' d888b    d888b    `Y8bod8P'     .8'     8""888P'     "+ \
"                                                                                            .o..P'                   "+ \
"                                                                                            `Y8P'                    "+ \
"                                                                                                                  "

@app.route('/')
def root():
    return '<h1>👨🏻‍💻</h1>'

@app.route('/47GMLwf7jfmesjwnQAKC/start', methods = ['POST'])
def start():
    global dm
    print(dm)
    dm = DialogueManager()

    return header + "\n Welcome! How can we help you?"

@app.route('/47GMLwf7jfmesjwnQAKC/utter', methods = ['POST'])
def utter():
    global dm
    print(dm)
    return dm.run_state(request.data.decode())


if __name__ == "__main__":
    app.run(debug=True)