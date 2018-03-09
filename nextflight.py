from flask import Flask, request
import flight_info
app = Flask(__name__)

@app.route("/nextflight", methods = ['GET', 'POST'])
def nextflight():
    print(request.values)
    print(request.data)
    if request.method == 'POST' and request.values and request.values["text"]:
        return inchannel(nextflightoffset(request.values["text"]))
    ret = ""
    for line in flight_info.get_launch():
        ret += line + "\n"
    return inchannel(ret)

@app.route("/nextflight/<offset>", methods = ['GET', 'POST'])
def nextflightoffset(offset):
    hasnumbers = False
    for letter in offset:
        if letter in "0123456789":
            hasnumbers = True
        elif letter != "-":
            return f"Invalid character '{letter}' in offset, offset can only contain numbers or a '-'\n"
    if not hasnumbers:
        return "Invalid offset, offset must be a number\n"

    ret = ""
    for line in flight_info.get_launch(int(offset)):
        ret += line + "\n"
    return ret

def inchannel(text):
    return '{"response_type": "in_channel","text":"' + text + '"}'

if __name__ == "__main__":
    app.run()
