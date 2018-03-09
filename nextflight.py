from flask import Flask
import flight_info
app = Flask(__name__)

@app.route("/nextflight", methods = ['GET', 'POST'])
def nextflight():
    if request.method == 'POST' and request.form and request.form.text:
        return nextflightoffset(request.form.text)
    ret = ""
    for line in flight_info.get_launch():
        ret += line + "\n"
    return ret

@app.route("/nextflight/<offset>", methods = ['GET', 'POST'])
def nextflightoffset(offset):
    hasnumbers = False
    for letter in offset:
        if letter in "0123456789":
            hasnumbers = True
        elif letter != "-":
            return "Invalid offset\n"
    if not hasnumbers:
        return "Invalid offset\n"

    ret = ""
    for line in flight_info.get_launch(int(offset)):
        ret += line + "\n"
    return ret

if __name__ == "__main__":
    app.run()
