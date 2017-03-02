# encoding=utf8
from flask import Flask
from flask import request, redirect, url_for, send_file
from flask import render_template
from models import *
import StringIO


from flask import Flask, request, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/change_name', methods=['POST'])
def change_name():
    return redirect(url_for('hello', name=request.form['new_name']))

    # return render_template('hello.html', name=request.form['new_name'])
    

@app.route('/match_item')
def match_item():
    return render_template("match_item.html", 
        items= db.session.query(Item).filter_by(standard_item_id= None).limit(20), 
        standards= db.session.query(StandardItem).all())


@app.route('/submit_match', methods=['POST'])
def submit_match():
    for item_id in request.form.keys():
        if(request.form[item_id] and request.form[item_id].isdigit()):
            item = db.session.query(Item).filter_by(id=int(item_id)).first()
            item.standard_item_id = int(request.form[item_id])
    db.session.commit()
    return redirect(url_for('match_item'))



@app.route('/reports')
def reports():
    sql = "select s.id,s.name, s.price/100, sum( if(items.month_sale_num = -1 , 0 , if(items.month_sale_num = null, 0 , items.month_sale_num) ) ) as month_sale_num from `standard_items` s inner join items on items.standard_item_id = s.id group by s.id"
    result = db.engine.execute(sql)
    lines = ["id,name,价格,销量"]

    def to_str(obj):
        if type(obj) != unicode:
            return str(obj).encode('utf-8')
        return obj

    for item in result:
        line = u",".join([to_str(i) for i in item])
        lines.append(line)

    text = StringIO.StringIO()
    text.write(("\n".join(lines)).encode("utf-8"))
    text.seek(0)
    return send_file(text, as_attachment=True, attachment_filename= "reports.csv")
    # return render_template("reports.html", lines=lines)




