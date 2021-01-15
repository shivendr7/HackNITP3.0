from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os


app=Flask(__name__)
app.secret_key="FarmPlus"
#app.permanent_session_lifetime=timedelta(hours=5)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['UPLOAD_FOLDER']="B:/python/Flask/proj3/static/uploads"
#Path to your app folder/static/uploads

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('name',db.String(100),nullable=False)
    email=db.Column('email',db.String(100),nullable=False,unique=True)
    residence=db.Column('residence',db.String(100),nullable=False)
    password=db.Column('password',db.String(100),nullable=False)

    def __init__(self, name, email,residence, password):
        self.name=name
        self.email=email
        self.residence=residence
        self.password=password

class Story(db.Model):
    id=db.Column('storyid',db.Integer,primary_key=True)
    img=db.Column('storyimg',db.String(100),nullable=True)
    title=db.Column('title',db.String(150),nullable=False)
    content=db.Column('content',db.String(1000),nullable=False)
    time=db.Column('storytime',db.String(50),nullable=False)
    user=db.Column('storyuser',db.String(100),nullable=False)

    def __init__(self,img,title,content,time,user):
        self.img=img
        self.title=title
        self.content=content
        self.time=time
        self.user=user

class News(db.Model):
    id=db.Column('newsid',db.Integer,primary_key=True)
    img=db.Column('newsimg',db.String(100),nullable=True)
    title=db.Column('newstitle',db.String(150),nullable=False)
    content=db.Column('newscontent',db.String(1000),nullable=False)
    time=db.Column('newstime',db.String(50),nullable=False)

    def __init__(self,img,title,content,time):
        self.img=img
        self.title=title
        self.content=content
        self.time=time

class Facility(db.Model):
    id=db.Column('facid',db.Integer,primary_key=True)
    img=db.Column('facimg',db.String(100),nullable=True)
    title=db.Column('factitle',db.String(150),nullable=False)
    content=db.Column('facontent',db.String(1000),nullable=False)
    time=db.Column('factime',db.String(50),nullable=False)

    def __init__(self,img,title,content,time):
        self.img=img
        self.title=title
        self.content=content
        self.time=time 

class Harvest(db.Model):
    id=db.Column('harid',db.Integer,primary_key=True)
    img=db.Column('harimg',db.String(100),nullable=True)
    title=db.Column('hartitle',db.String(150),nullable=False)
    content=db.Column('harcontent',db.String(1000),nullable=False)
    time=db.Column('hartime',db.String(50),nullable=False)

    def __init__(self,img,title,content,time):
        self.img=img
        self.title=title
        self.content=content
        self.time=time 


@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        if email=='admin@farmplus.com':
            session['email']=email
            return redirect(url_for('adash'))
        residence=request.form['farm']
        password=request.form['password']
        #session.permanent=True
        find_user=User.query.filter_by(email=email).first()
        if find_user:
            if password==find_user.password:
                session['email']=find_user.email
                return redirect(url_for('dash'))
            else:
                flash('Invalid login')
                return render_template('index.html',LorD='Login')
        user=User(name=name, email=email, residence=residence, password=password)
        db.session.add(user)
        db.session.commit()
        session['email']=user.email
        return redirect(url_for('dash'))

    else:
        if 'email' in session:
            return render_template('index.html',LorD='Dashboard')
        return render_template('index.html',LorD='Login')

@app.route('/dash')
def dash():
    if 'email' in session:
        email=session['email']
        if email=='admin@farmplus.com':
            return redirect(url_for('home'))
        user=User.query.filter_by(email=email).first()
        return render_template('dash.html',name=user.name,email=user.email,storysentival=0.0,onstorysentival=0.0,laststorysentival=0.0,onlaststorysentival=0.0)
    else :
        return redirect(url_for('home'))

@app.route('/history')
def hist():
    return render_template('history.html')

@app.route('/story',methods=['GET','POST'])
def story():
    img=None
    if request.method=='POST':
        if 'file' in request.files:
            file=request.files['file']
            if file : 
                if validateImg(file):
                    img=dumpImg(file)
        title=request.form['title']
        content=request.form['content']
        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        email=session['email']
        user=User.query.filter_by(email=email).first()
        story=Story(img=img,title=title,content=content,time=time,user=user.name)
        db.session.add(story)
        db.session.commit()
        stories=Story.query.filter_by(user=user.name)
        return render_template('stories.html',stories=stories)
    else:
        email=session['email']
        user=User.query.filter_by(email=email).first()
        stories=Story.query.filter_by(user=user.name)
        return render_template('stories.html',stories=stories)

@app.route('/account')
def account():
    email=session['email']
    user=User.query.filter_by(email=email).first()
    return render_template('account.html',user=user)

@app.route('/adash')
def adash():
    return render_template('adash.html')

@app.route('/aharvest',methods=['GET','POST'])
def aharvest():
    img=None
    if request.method=='POST':
        if 'file' in request.files:
            file=request.files['file']
            if file : 
                if validateImg(file):
                    img=dumpImg(file)
        title=request.form['title']
        content=request.form['content']
        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        harvest=Harvest(img=img,title=title,content=content,time=time)
        db.session.add(harvest)
        db.session.commit()
    harvests=Harvest.query.all()
    return render_template('aharvest.html', harvests=harvests)

@app.route('/afacilities',methods=['GET','POST'])
def afacilities():
    img=None
    if request.method=='POST':
        if 'file' in request.files:
            file=request.files['file']
            if file : 
                if validateImg(file):
                    img=dumpImg(file)
        title=request.form['title']
        content=request.form['content']
        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        fac=Facility(img=img,title=title,content=content,time=time)
        db.session.add(fac)
        db.session.commit()
    facs=Facility.query.all()
    return render_template('afacilities.html',facilities=facs)

@app.route('/anews',methods=['GET','POST'])
def anews():
    img=None
    if request.method=='POST':
        if 'file' in request.files:
            file=request.files['file']
            if file : 
                if validateImg(file):
                    img=dumpImg(file)
        title=request.form['title']
        content=request.form['content']
        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        news=News(img=img,title=title,content=content,time=time)
        db.session.add(news)
        db.session.commit()
    news_all=News.query.all()
    return render_template('anews.html',news=news_all)

@app.route('/feed',methods=['POST','GET'])
def feed():
    img=None
    if request.method=='POST':
        if 'file' in request.files:
            file=request.files['file']
            if file : 
                if validateImg(file):
                    img=dumpImg(file)
        title=request.form['title']
        content=request.form['content']
        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        email=session['email']
        user=User.query.filter_by(email=email).first()
        story=Story(img=img,title=title,content=content,time=time,user=user.name)
        db.session.add(story)
        db.session.commit()
    stories=Story.query.all()
    return render_template('infeed.html',stories=stories)

@app.route('/harvest')
def harvest():
    harvests=Harvest.query.all()
    return render_template('inharvest.html',harvests=harvests)

@app.route('/newsletter')
def newsletter():
    news_all=News.query.all()
    return render_template('innewsletter.html',news=news_all)

@app.route('/facilities')
def facilities():
    facs=Facility.query.all()
    return render_template('infacilities.html',facilities=facs)

@app.route('/fullstory')
def fullstory():
    return render_template('fullstory.html')

@app.route('/upload',methods=['POST','GET'])
def uploadtest():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('no file')
            return render_template('home.html',filename='',ext='')
        else:
            file=request.files['file']
            if not file:
                return render_template('home.html',filename='',ext='')
            filename = secure_filename(file.filename)
            fname=filename[:filename.index('.')]
            ext=filename[filename.index('.')+1:]
            fname+=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname+'.'+ext))
            if 'textarea' in request.form:
                flash(request.form['textarea'])
            return render_template('home.html',filename=fname,ext=ext)
    else:       
        return render_template('home.html',filename='',ext='')

def validateImg(file):
    filename=secure_filename(file.filename)
    if '.' not in filename:
        return False
    #fname=filename[:filename.index('.')]
    ext=filename[filename.index('.')+1:]
    return ext.lower() in ['png','jpg','jpeg']

def dumpImg(file):
    filename=secure_filename(file.filename)
    fname=filename[:filename.index('.')]
    ext=filename[filename.index('.')+1:]
    fname+=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname+'.'+ext))
    return fname+'.'+ext

db.create_all()
app.run(use_reloader=False, port='800')
