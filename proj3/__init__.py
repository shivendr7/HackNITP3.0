from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import taggify
import numpy as np 
import joblib


app=Flask(__name__)
app.secret_key="FarmPlus"
#app.permanent_session_lifetime=timedelta(hours=5)

app.jinja_env.filters['zip'] = zip

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['UPLOAD_FOLDER']="B:/python/Flask/proj3/static/uploads"
#Path to your app folder/static/uploads

db=SQLAlchemy(app)

District_list=["Bhagalpur","Chapra","Darbhanga","Dehri","Forbesganj","Gaya","Jamui","Motihari","Muzaffarpur","Patna","Purnea","Raxaul","Sabour","Supaul"]
district_list=["bhagalpur","chapra","darbhanga","dehri","forbesganj","gaya","jamui","motihari","muzaffarpur","patna","purnea","raxaul","sabour","supaul"]
month_list=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
Month_list=['January','February','March','April','May','June','July','August','September','October','November','December']
crop_dic={
    'redcabbage':[18,0,85,0,600,.328,4],
    'broccli':[21,0,93,0,900,0,8],
    'strawberry':[20.5,0,70,0,373,0,9],
    'kiwi':[7,0,90,0,1500,0,0],
    'dragonfruit':[25,0,87,0,1842.5,0,3],
    'pepino':[18,0,65,0,650,0,7]
}

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
    tag=db.Column('storytag',db.String(100),nullable=True)

    def __init__(self,img,title,content,time,user,tag):
        self.img=img
        self.title=title
        self.content=content
        self.time=time
        self.user=user
        self.tag=tag

class News(db.Model):
    id=db.Column('newsid',db.Integer,primary_key=True)
    img=db.Column('newsimg',db.String(100),nullable=True)
    title=db.Column('newstitle',db.String(150),nullable=False)
    content=db.Column('newscontent',db.String(1000),nullable=False)
    time=db.Column('newstime',db.String(50),nullable=False)
    tag=db.Column('newstag',db.String(100),nullable=True)

    def __init__(self,img,title,content,time,tag):
        self.img=img
        self.title=title
        self.content=content
        self.time=time
        self.tag=tag

class Facility(db.Model):
    id=db.Column('facid',db.Integer,primary_key=True)
    img=db.Column('facimg',db.String(100),nullable=True)
    title=db.Column('factitle',db.String(150),nullable=False)
    content=db.Column('facontent',db.String(1000),nullable=False)
    time=db.Column('factime',db.String(50),nullable=False)
    tag=db.Column('factag',db.String(100),nullable=True)

    def __init__(self,img,title,content,time,tag):
        self.img=img
        self.title=title
        self.content=content
        self.time=time 
        self.tag=tag

class Harvest(db.Model):
    id=db.Column('harid',db.Integer,primary_key=True)
    img=db.Column('harimg',db.String(100),nullable=True)
    title=db.Column('hartitle',db.String(150),nullable=False)
    content=db.Column('harcontent',db.String(1000),nullable=False)
    time=db.Column('hartime',db.String(50),nullable=False)
    tag=db.Column('hartag',db.String(100),nullable=True)

    def __init__(self,img,title,content,time,tag):
        self.img=img
        self.title=title
        self.content=content
        self.time=time 
        self.tag=tag

class Suggestions(db.Model):
    id=db.Column('seggestid',db.Integer,primary_key=True)
    val=db.Column('suggestval',db.String(20),nullable=False)
    postid=db.Column('Adminpostid',db.Integer,nullable=False)
    postTable=db.Column('AdminpostTable',db.String(1),nullable=False)

    def __init__(self,val,postid,postTable):
        self.val=val
        self.postid=postid
        self.postTable=postTable

"""
class StoryTags(db.Model):
    id=db.Column('tagid',db.Integer,primary_key=True)
    name=db.Column('tagname',db.String(50),nullable=False)
    storyid=db.Column('storyid',db.Integer,nullable=False)

    def __init__(self,name,storyid):
        self.name=name
        self.storyid=storyid
"""
def addSuggestion(value, postid, table):
    suggest=Suggestions(val=value,postid=postid,postTable=table)
    db.session.add(suggest)
    db.session.commit()

def getSuggestion(output):
    sugg=Suggestions.query.filter_by(val=output)
    out=[]
    if sugg:
        for suggestion in sugg:
            out.append(suggestion.postTable+str(suggestion.postid))
    return out


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

def modeldistrict(ar):
    for ele in ar:
        try :
            check=int(ele)
        except Exception as e:
            return None
    x=[ar]
    clf=joblib.load('district.csv')
    arr=np.array(x)
    p=clf.predict(arr)
    return p[0]

def modelmonth(ar):
    for ele in ar:
        try :
            check=int(ele)
        except Exception as e:
            return None
    x=[ar]
    clf=joblib.load('month_index.csv')
    arr=np.array(x)
    p=clf.predict(arr)
    return p[0]


@app.route('/cultivate',methods=['GET','POST'])
def cultivate():
    out1=None;out2=None;sugg=None
    if request.method=='POST':
        if 'crop1' in request.form:
            s=request.form['crop1']
            out=modelmonth(crop_dic[s])
            try:
                out=Month_list[out-1]
            except Exception as e:
                flash(e)
            #suggestion
            sugg=getSuggestion(out)
            if len(sugg)==0:
                sugg=None
            return render_template('cultivate.html',out1=out,out2=out2,suggestion=sugg)

        elif 'crop2' in request.form:
            s=request.form['crop2']
            out=modeldistrict(crop_dic[s])
            try:
                out=District_list[out]
            except Exception as e:
                flash(e)
            #suggestion
            sugg=getSuggestion(out)
            if len(sugg)==0:
                sugg=None
            return render_template('cultivate.html',out1=out1,out2=out,suggestion=sugg)

        elif 'temp1' in request.form or 'rain1' in request.form or 'humid1' in request.form or 'arain1' in request.form or 'wind1' in request.form or 'cloud1' in request.form or 'dist1' in request.form:
            ar=['temp1','wind1','humid1','cloud1','rain1','arain1','dist1']
            out=[]
            for inp in ar:
                s=request.form[inp]
                if inp=='dist1':
                    st=str(request.form[inp])
                    if st.lower() in district_list:
                        out.append(district_list.index(st.lower()))
                        continue
                    else :
                        flash('Please enter one of the following Districts:\n["Bhagalpur","Chapra","Darbhanga","Dehri","Forbesganj","Gaya","Jamui","Motihari","Muzaffarpur","Patna","Purnea","Raxaul","Sabour","Supaul"]')
                        return render_template('cultivate.html',out1=out1,out2=out2,suggestion=sugg)
                
                if request.form[inp]==None or request.form[inp]==0:
                    out.append(0)
                    continue
                out.append(request.form[inp])
            output=modelmonth(out)
            if output==None:
                flash('Invalid Input')
                return render_template('cultivate.html',out1=out1,out2=out2,suggestion=sugg)
            try:
                output=Month_list[output-1]
            except Exception as e:
                flash(e)
            #suggestions
            sugg=getSuggestion(output)
            if len(sugg)==0:
                sugg=None
            return render_template('cultivate.html',out1=output,out2=out2,suggestion=sugg)
            
        elif 'temp2' in request.form or 'rain2' in request.form or 'humid2' in request.form or 'arain2' in request.form or 'wind2' in request.form or 'cloud2' in request.form or 'month' in request.form:
            ar=['temp2','wind2','humid2','cloud2','rain2','arain2','month']
            out=[]
            for inp in ar:
                s=request.form[inp]
                try:
                    if input=='month':
                        st=str(request.form[inp])
                        st=s[:3]
                        st=st.lower()
                        if st in month_list:
                            out.append(month_list.index(st))
                            continue
                except Exception as e:
                    flash(e)
                
                if request.form[inp]==None or request.form[inp]==0:
                    out.append(0)
                    continue
                out.append(request.form[inp])
            output=modeldistrict(out)
            if output==None:
                flash('Invalid Input')
                return render_template('cultivate.html',out1=out1,out2=out2,suggestion=sugg)
            try:
                output=District_list[output]
            except Exception as e:
                flash(e)
            #suggestions
            sugg=getSuggestion(output)
            if len(sugg)==0:
                sugg=None
            return render_template('cultivate.html',out1=out1,out2=output,suggestion=sugg)
            
    else:
        return render_template('cultivate.html',out1=out1,out2=out2,suggestion=sugg)

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
        tag_list=taggify.tags(content)
        tag=None
        if len(tag_list)>0:
            tag=' #'.join(tag_list)
            tag='#'+tag

        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        email=session['email']
        user=User.query.filter_by(email=email).first()
        story=Story(img=img,title=title,content=content,time=time,user=user.name,tag=tag)
        db.session.add(story)
        db.session.commit()
        stories=Story.query.filter_by(user=user.name)
        revstories=(stories[::-1])
        time_list=getTimeList(revstories)
        return render_template('stories.html',stories=revstories,time_list=time_list)
    else:
        email=session['email']
        user=User.query.filter_by(email=email).first()
        stories=Story.query.filter_by(user=user.name)
        revstories=(stories[::-1])
        time_list=getTimeList(revstories)
        return render_template('stories.html',stories=revstories,time_list=time_list)

def getTimeList(revstories):
    time_list=[]
    U=[' days',' months',' years',' hours',' minutes',' seconds']
    for story in revstories:
        pasttime=story.time
        ctime=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        t1=[int(x) for x in pasttime.split('-')]
        t2=[int(x) for x in ctime.split('-')]
        for i in range(6):
            if not t1[i]==t2[i]:
                time_list.append(str(t2[i]-t1[i])+U[i]+' ago')
                break
            if i==5:
                time_list.append('Just now')
    return time_list
                

def putTags(s,id):
    tag_list=taggify.tags(s)
    for t in tag_list:
        tag=StoryTags(name=t,storyid=id)
        db.session.add(tag)
        db.session.commit()

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
        suggestType=request.form['suggestType']
        if len(title)==0 or len(content)==0:
            flash('******title or content cannot be null XD*******')
            harvests=Harvest.query.all()
            revharvests=(harvests[::-1])
            time_list=getTimeList(revharvests)
            return render_template('aharvest.html', harvests=revharvests,time_list=time_list)

        tag_list=taggify.tags(content)
        tag=None
        if len(tag_list)>0:
            tag=' #'.join(tag_list)
            tag='#'+tag

        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        harvest=Harvest(img=img,title=title,content=content,time=time,tag=tag)
        db.session.add(harvest)
        db.session.commit()

        if not suggestType=='None':
            addSuggestion(suggestType,harvest.id,'h')

    harvests=Harvest.query.all()
    revharvests=(harvests[::-1])
    time_list=getTimeList(revharvests)
    return render_template('aharvest.html', harvests=revharvests,time_list=time_list)

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
        suggestType=request.form['suggestType']
        if len(title)==0 or len(content)==0:
            flash('******title or content cannot be null XD*******')
            facs=Facility.query.all()
            revfacs=facs[::-1]
            time_list=getTimeList(revfacs)
            return render_template('afacilities.html',facilities=revfacs,time_list=time_list)


        tag_list=taggify.tags(content)
        tag=None
        if len(tag_list)>0:
            tag=' #'.join(tag_list)
            tag='#'+tag

        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        fac=Facility(img=img,title=title,content=content,time=time,tag=tag)
        db.session.add(fac)
        db.session.commit()

        if not suggestType=='None':
            addSuggestion(suggestType,fac.id,'f')
    facs=Facility.query.all()
    revfacs=facs[::-1]
    time_list=getTimeList(revfacs)
    return render_template('afacilities.html',facilities=revfacs,time_list=time_list)

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
        suggestType=request.form['suggestType']
        if len(title)==0 or len(content)==0:
            flash('******title or content cannot be null XD*******')
            news_all=News.query.all()
            revnews=(news_all[::-1])
            time_list=getTimeList(revnews)
            return render_template('anews.html',news=revnews,time_list=time_list)
        suggestType=request.form['suggestType']
        tag_list=taggify.tags(content)
        tag=None
        if len(tag_list)>0:
            tag=' #'.join(tag_list)
            tag='#'+tag

        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        news=News(img=img,title=title,content=content,time=time,tag=tag)
        db.session.add(news)
        db.session.commit()

        if not suggestType=='None':
            addSuggestion(suggestType,news.id,'n')

    news_all=News.query.all()
    revnews=(news_all[::-1])
    time_list=getTimeList(revnews)
    return render_template('anews.html',news=revnews,time_list=time_list)

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
        tag_list=taggify.tags(content)
        tag=None
        if len(tag_list)>0:
            tag='# '.join(tag_list)
            tag='#'+tag

        time=datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        email=session['email']
        user=User.query.filter_by(email=email).first()
        story=Story(img=img,title=title,content=content,time=time,user=user.name,tag=tag)
        db.session.add(story)
        db.session.commit()
    stories=Story.query.all()
    revstories=(stories[::-1])
    time_list=getTimeList(revstories)
    return render_template('infeed.html',stories=revstories,time_list=time_list)


@app.route('/harvest')
def harvest():
    harvests=Harvest.query.all()
    revharvests=(harvests[::-1])
    time_list=getTimeList(revharvests)
    return render_template('inharvest.html',harvests=revharvests,time_list=time_list)

@app.route('/newsletter')
def newsletter():
    news_all=News.query.all()
    revnews=(news_all[::-1])
    time_list=getTimeList(revnews)
    return render_template('innewsletter.html',news=revnews,time_list=time_list)

@app.route('/facilities')
def facilities():
    facs=Facility.query.all()
    revfacs=facs[::-1]
    time_list=getTimeList(revfacs)
    return render_template('infacilities.html',facilities=revfacs,time_list=time_list)
"""

def fullstory():
    
    return render_template('fullstory.html')
"""

@app.route('/fullstory/<s>')
def fullstory(s):
    if s[0]=='f':
        s=s[1:]
        facility=Facility.query.filter_by(id=int(s)).first()
        facs=[facility]
        t_l=getTimeList(facs)
        t=t_l[0]
        return render_template('fullstory.html',post=facility,time=t)
    elif s[0]=='n':
        s=s[1:]
        news=News.query.filter_by(id=int(s)).first()
        facs=[news]
        t_l=getTimeList(facs)
        t=t_l[0]
        return render_template('fullstory.html',post=news,time=t)
    elif s[0]=='h':
        s=s[1:]
        harvest=Harvest.query.filter_by(id=int(s)).first()
        facs=[harvest]
        t_l=getTimeList(facs)
        t=t_l[0]
        return render_template('fullstory.html',post=harvest,time=t)
    return 'No story'

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
