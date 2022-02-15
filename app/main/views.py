from crypt import methods
from flask import render_template,request,redirect,url_for,abort
from ..models import User,Quote,Upvote,Downvote,Comment
from . import main
from flask_login import login_required,current_user
from .forms import QuoteForm, UpdateProfile,CommentForm
from .. import db,photos

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')
@main.route('/login')
def login():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('login.html')
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/new_quote', methods=['GET','POST'])
@login_required
def new_quotes():
    form=QuoteForm()
    if form.validate_on_submit():
        quote=form.my_quotes.data
        new_quote=Quote(quote=quote,user_id=current_user.id)
        new_quote.save_quote()

    return render_template('new_quote.html',quote_form=form)

@main.route('/quotes')
def quote_page():    
    user = User.query.all()
    quotes = Quote.query.all()
    user=current_user
    return render_template('quotes.html',quotes=quotes,user=user)
@main.route('/quotes/comments/<int:quote_id>', methods=['GET','POST'])
@login_required
def leave_comment(quote_id):
    comment_form = CommentForm()
    quotes= Quote.query.get(quote_id)
    comment = Comment.query.filter_by(quote_id=quote_id).all()
    if comment_form.validate_on_submit():
        comments = comment_form.comment.data
        
        quote_id= quote_id
        user_id = current_user._get_current_object().id
        new_comment= Comment(comments=comments,quote_id=quote_id, user_id=user_id)
        new_comment.save_comment()      
        
        return redirect(url_for('main.pitch_page',comment_form=comment_form,quote_id=quote_id))
        
    return render_template('comments.html',comment_form=comment_form, comment=comment,quote_id=quote_id)

#likes count

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_quotes = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for quote in get_quotes:
        to_str = f'{quote}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.quote_page'))
        else:
            continue
    new_vote = Upvote(user = current_user, quote_id=id)
    new_vote.save()
    return redirect(url_for('main.quote_page'))
#downvote
@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    quote = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in quote:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.quote_page'))
        else:
            continue
    new_downvote = Downvote(user = current_user, quote_id=id)
    new_downvote.save()
    return redirect(url_for('main.quote_page'))