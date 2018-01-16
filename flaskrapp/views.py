from flask import g, render_template, request, session, abort, flash, url_for, redirect, jsonify, make_response
from flask_login import login_required, login_user, logout_user, current_user
from flask_httpauth import HTTPBasicAuth
from flaskrapp import app, loginManager
from .models import User, Post
from . import db

auth = HTTPBasicAuth()

@loginManager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
@login_required
def show_entries():
    posts = Post.query.all()
    # cur = db.execute('select title, text from entries order by id desc')
    entries = [dict(title=p.title, text=p.body, id=p.id) for p in posts]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    p = Post(title=request.form['title'], body=request.form['text'], author=current_user)
    db.session.add(p)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/delete/<int:post_id>')
def delete_entry(post_id):
    if not session.get('logged_in'):
        abort(401)

    p = Post.query.filter_by(id=post_id).first()
    db.session.delete(p)
    db.session.commit()
    flash('Entry was successfully removed')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            error = 'Invalid username'
        elif not user.verify_password(request.form['password']):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            login_user(user)
            flash('You were logged in as {}'.format(current_user))
            
            # next = request.args.get('next')
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            # if not next_is_valid(next):
            #     return abort(400)

            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    logout_user()
    return redirect(url_for('show_entries'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.route('/api/postlist')
@auth.login_required
def get_postlist():
    posts = Post.query.filter_by(user_id=g.user.id).all()
    if not posts:
        abort(404)
    postdic = [{'id':p.id,'title':p.title,'body':p.body,'pub_date':p.pub_date} for p in posts]
    return jsonify({ 'posts': postdic })


@app.route('/api/post/<int:post_id>', methods = ['GET'])
@auth.login_required
def get_post(post_id):
    post = Post.query.filter_by(user_id=g.user.id,id=post_id).first()
    if not post:
        abort(404)
    postdic = {'id':post.id,'title':post.title,'body':post.body,'pub_date':post.pub_date}
    return jsonify({ 'post': postdic })


@app.route('/api/postlist', methods = ['POST'])
@auth.login_required
def create_post():
    if not request.json or not 'title' in request.json or not 'body' in request.json:
        abort(400)
    
    newpost = Post(title=request.json['title'],body=request.json['body'],user_id=g.user.id) 
    db.session.add(newpost)
    db.session.commit()
    return url_for('get_postlist')

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods = ['POST'])
@auth.login_required
def new_user():
    if g.user.username != 'admin':
        return make_response(jsonify({'error': 'Not administrator'}), 404)

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing email
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201


@app.route('/api/users')
@auth.login_required
def get_userlist():
    if g.user.username != 'admin':
        return make_response(jsonify({'error': 'Not administrator'}), 404)

    userlist = User.query.filter_by(id!=1).all()
    if not userlist:
        # abort(404)
        make_response(jsonify({'error': 'Not administrator'}), 404)

    userlistdic = [{'id':u.id,'name':u.username,'email':u.email} for u in userlist]
    return jsonify({ 'user list': userlistdic })


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })