# Existing imports remain the same

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create a list to store the tasks
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=enumerate(tasks))

# @app.route('/')
# def index():
#    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    tasks.append(task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    if request.method == 'POST':
        new_task = request.form.get('task')
        tasks[index] = new_task
        return redirect(url_for('index'))
    return render_template('edit.html', task=tasks[index])

@app.route('/delete/<int:index>')
def delete_task(index):
    del tasks[index]
    return redirect(url_for('index'))

# Existing routes remain the same

if __name__ == '__main__':
    app.run(debug=True)
 
