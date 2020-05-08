from flask import url_for,Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cf14150cf9357da5553b4731f29fb23980a29f64"
app.debug = False
localdb = 'sqlite:///localDB'
herokudb = 'postgres://lhehasysqqwtyz:ff04c85afaedfb1a603b1cd10d90333e2ee5a7fcdf839c7e0525e07596ef013f@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d74sh0ulo06hlt'
app.config['SQLALCHEMY_DATABASE_URI'] = herokudb
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.String(30),nullable=False,default='text@text.com')
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

class Users(db.Model):
    userid = db.Column(db.String(30),nullable=False,primary_key=True)
    password = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    def __repr__(self):
        return '<Task %r>' % self.userid

@app.route('/')
def index():
    return redirect('/login/')

@app.route('/login/',methods=['POST','GET'])
def login():
    if "user" in session:
        return redirect('/tasks/')
    userid = ''
    paswd = ''
    if request.method == 'POST':
        userid = request.form['userid']
        paswd = request.form['password']
        if userid==None or paswd==None:
            flash("Userid and Password cannot be empty!")
            redirect('/')
        else:
            users = Users.query.filter_by(userid=userid).first()
        if(users.password == paswd):
            session["user"] = users.userid
            flash("Logged in successfully")
            return redirect('/tasks/')
        else :
            return redirect('/')         
    return render_template('login.html')

@app.route('/register/',methods=['POST','GET'])
def register():
    if "user" in session:
        return redirect('/tasks/')
    if request.method == 'POST':
        email = request.form['email']
        userid = request.form['userid']
        password = request.form['password']
        existcheck = Todo.query.filter_by(userid=userid).first()
        if(existcheck==None):
            new_registry = Users(userid=userid,email=email,password=password)
            try:
                db.session.add(new_registry)
                db.session.commit()
            except:
                flash('There was an internal issue creating a new user - Contact TechSupport')
            return redirect('/login/')
        else:
            pass
    return render_template('register.html')

@app.route('/tasks/',methods=['POST','GET'])
def tasks():
    if "user" in session:
        userid = session["user"]
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo(userid=userid,content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                flash("Task added successfully :)")
            except :
                flash('There was an issue adding that task, try again or try later')
            return redirect('/tasks/')
        else:
            tasks = Todo.query.filter_by(userid=userid).order_by(Todo.date_created).all()
            return render_template('tasks.html',tasks=tasks,userid=userid)
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if "user" in session:
        userid = session["user"]
    else:
        return redirect('/')
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully :)")
    except:
        flash('There was a problem deleting that task')
    return redirect('/tasks/')    

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    if "user" in session:
        userid = session["user"]
    else:
        return redirect('/')
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            flash("Task updated successfully :)")
        except:
            flash('There was an issue updating your task')
        return redirect('/tasks/')
    else:
        return render_template('update.html',task=task)

@app.route('/logout/')
def logout():
    flash("You have been logged out")
    session.pop("user",None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)