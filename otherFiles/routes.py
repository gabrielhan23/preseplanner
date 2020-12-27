from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from random import randint

from otherFiles.setup import *
from otherFiles.databases import *
from otherFiles.forms import *
from otherFiles.functions import *

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template("main.html", title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("groups"))
  form = LoginForm()
  if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        flash('Login Success!', 'success')
        return redirect(url_for('groups'))
      else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        print("login failed")
        return render_template('login.html', title='Login', form=form)
  return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for("groups"))
  form = RegistrationForm()
  if form.validate_on_submit():
      #make user
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, password=hashed_password)
      db.session.add(user)
      db.session.commit()

      #return
      login_user(user, remember="False")
      flash('Your account has been created! Login Success!', 'success')
      return redirect(url_for('groups'))
  return render_template("signup.html", title='Sign Up', form=form)

@app.route('/group/<int:groupID>', methods=['GET', 'POST'])
@login_required
def group(groupID):
  group = Group.query.filter_by(hashID=groupID).first()
  if group:
    for x in current_user.groups:
      if int(x.hashID) == int(groupID):
        people = group.users
        return render_template("group.html", title='Group', group=group, people=people, me=current_user)
  return redirect('groups')

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
  groups = current_user.groups
  print(groups)
  return render_template("groups.html", title='Groups', groups=groups)

@app.route('/person/<int:groupID>/<int:personID>', methods=['GET', 'POST'])
@login_required
def person(groupID, personID):
  wish = Wish.query.filter(Wish.user_id==personID, Wish.group_id==groupID).all()
  get = Get.query.filter(Get.user_id==personID, Get.group_id==groupID).all()
  group = Group.query.filter_by(hashID=groupID).first()
  person = User.query.filter_by(id=personID).first()
  if group:
    for x in current_user.groups:
      if int(x.hashID) == int(groupID) and personID != current_user.id:
        print(get)
        return render_template("person.html", title='Group', group=group, wishes=wish, gets=get, person=person, userid=personID, groupID=groupID, current_user_id=current_user.id)
      elif int(x.hashID) == int(groupID):
        return render_template("person.html", title='Group', group=group, wishes=wish, userid=personID, groupID=groupID)
  return redirect(url_for('groups'))

@app.route('/wishlist/<int:groupID>', methods=['GET', 'POST'])
@login_required
def wishlist(groupID):
  flash('Group Added!', 'success')
  group = Group.query.filter_by(hashID=groupID).first()
  return render_template("wishlist.html", title='Wishlist', group=group)

@app.route('/joingroup', methods=['POST'])
@login_required
def joinGroup():
  if request.form.get("joinID"):
    group = Group.query.filter_by(hashID=request.form.get("joinID")).first()
    group.users.append(current_user)
    db.session.add(group)
    db.session.commit()
    print(group)
    return jsonify([group.name, group.hashID])
  else:
    return jsonify(False)

@app.route('/creategroup', methods=['POST'])
@login_required
def createGroup():
  if request.form.get("createName"):
    hashID = randint(1000, 9999)
    group = Group(name=request.form.get("createName"), hashID=hashID)
    group.users.append(current_user)
    db.session.add(group)
    db.session.commit()
    print(group)
    return jsonify(hashID)
  else:
    return jsonify(False)

@app.route('/wishlist/addwish', methods=['POST'])
@login_required
def addWish():
  if request.form.get("wishName"):
    wish = Wish(name=request.form.get("wishName"), user_id=current_user.id, group_id=request.form.get("groupID"))
    db.session.add(wish)
    db.session.commit()
    print("sucessful wish adding")
    return jsonify(True)
  else:
    return jsonify(False)

@app.route('/wishlist/deletewish', methods=['POST'])
@login_required
def deleteWish():
  if request.form.get("groupID"):
    wishes = Wish.query.filter(Wish.user_id==current_user.id, Wish.group_id==request.form.get("groupID")).all()
    print(wishes)
    for wish in wishes:
      db.session.delete(wish)
    db.session.commit()
    print("sucessful wish deleting")
    return jsonify(True)
  else:
    return jsonify(False)

@app.route('/person/<int:group>/addget', methods=['POST'])
@login_required
def addGet(group):
  if request.form.get("getName"):
    print(request.form.get("wishChecked"))
    if request.form.get("wishChecked") != "false":
      print("i ran anyways oops")
      user = User.query.filter_by(id=request.form.get("userid")).first()
      print(user.id)
      get = Get(name=request.form.get("getName"), user_id=user.id, group_id=request.form.get("groupID"), user_getting_for_id=current_user.id)
      db.session.add(get)
      db.session.commit()
      if request.form.get("wishID"):
        wish = Wish.query.filter_by(id=request.form.get("wishID")).first()
        wish.get_id = get.id
        wish.get_user_id = current_user.id
        print("testing")
        print(wish.get_user_id)
      print(get.id)
      db.session.commit()
      return jsonify(get.id)
    else:
      print("REMOVINGGGGGGG")
      get = Get.query.filter_by(id=request.form.get("getID")).first()
      db.session.delete(get)
      wish = Wish.query.filter_by(id=request.form.get("wishID")).first()
      wish.get_id = None
      wish.get_user_id = None
      db.session.commit()
    return jsonify(True)
  else:
    return jsonify(False)

@app.route('/delete', methods=['POST'])
@login_required
def deleteGroup():
  if request.form.get("group"):
    group = Group.query.filter_by(hashID=request.form.get("group")).first()
    group.users.remove(current_user)
    db.session.add(group)
    db.session.commit()
    return jsonify(True)
  else:
    return jsonify(False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
