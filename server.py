from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/preorder', methods=['POST', 'GET'])
def preorder():
    print("Form submitted")
    result = request.form
    print(result)
    # your code
    # return a response
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
