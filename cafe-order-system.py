from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/<int:table_num>', methods=['GET', 'POST'])
def select_table(table_num):
    if request.method == 'POST':
        pass #order act
    else:
        return render_template('table.html', num=table_num) #table page
    #select table and order food
    return ""

@app.route('/management')
def management():
    #if not logined, login page, if logined management page

    return ""

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pass #Login act
    else:
        pass #login page

if __name__ == '__main__':
    app.run()
