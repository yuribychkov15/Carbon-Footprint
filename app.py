from flask import Flask, render_template, request
import carbon_data_generator
import datetime

app = Flask(__name__, template_folder="templates")

database = []
history_db = []

def store_data(filename, data):
    with open(filename, 'a') as file:
        file.write(data)

def retrieve_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
        return data

@app.route("/")
def hello():
    global database
    database = []
    return render_template('index.html')

@app.route("/tips")
def tips():
    return render_template('tips.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/get_history", methods=['POST'])
def get_history():
    retrieved_data = retrieve_data('data.txt')
    print(retrieved_data)
    return retrieved_data

@app.route('/process', methods=['POST'])
def process():
    name = request.form.get('name')
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    transit = request.form.get('transit')
    frequency = request.form.get('freq')

    # process the data using Python code
    todo_item = [name, origin, destination, transit, frequency]
    database.append(todo_item)
    print(database)

    return '200'

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form.get('name')
    print(name)
    for item in database:
        if item[0] == name:
            database.remove(item)
    print(database)
    return '200'

@app.route('/generate', methods=['POST'])
def generate():
    if database == []:
        return 'Add some routes to continue!'

    data = carbon_data_generator.calculate_results(database)
    #history_db.append(f"| {datetime.datetime.now().strftime('%y-%m-%d')} Carbon Used: {data[1]} |")
    store_data('data.txt', f"Date: {datetime.datetime.now().strftime('%m-%d-%y')} Carbon Used: {data[1]}<br>\n")
    return data[0]

if __name__ == '__main__':
    app.run(debug=True)
