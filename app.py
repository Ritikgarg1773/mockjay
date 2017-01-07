from flask import Flask, render_template, g, request, jsonify, redirect
import sqlite3

app = Flask(__name__)
app.database = "mocker.db"

@app.route('/')
def home():
    g.db = connect_db()
    mocks = g.db.execute('select * from mockjay order by (likes - dis) DESC').fetchall()
    g.db.close()
    return render_template('home.html', mocks = mocks)

@app.route('/mock')
def mock():
    return render_template('mock.html')

@app.route('/mocked', methods=['POST'])
def mocked():
    name = request.form['name']
    sub = request.form['sub']
    mockery = request.form['mockery']
    #print (name + " mocked on " + sub + " that " + mockery)
    g.db = connect_db()
    cur = g.db.execute("INSERT INTO mockjay (name, sub, mockery, likes, dis) VALUES (? , ? , ?, 0, 0)", (name, sub, mockery))
    g.db.commit()
    g.db.close()
    return redirect('/')

@app.route('/liked')
def liked():
    a = request.args.get('a', type=int)
    updateDatabase_like(a)
    return jsonify(result = a)

def updateDatabase_like(y):
    g.db = connect_db()
    cur = g.db.execute("UPDATE mockjay SET likes = likes + 1 WHERE id = ?", (str(y), ))
    g.db.commit()
    g.db.close()


def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
    app.run(debug = True)
