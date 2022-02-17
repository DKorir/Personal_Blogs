from crypt import methods
from flask import flash, render_template,request,redirect,url_for,abort
from ..models import User,Quote,Upvote,Downvote,Comment
from . import main
from flask_login import login_required,current_user
from .forms import QuoteForm, UpdateProfile,CommentForm
from .. import db,photos
from ..request import get_quotes_api

# Views
@main.route('/')
def index():
    quotes=get_quotes_api()

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html', quotes=quotes)
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
@main.route("/main/<int:quote_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(quote_id):
    Quote = Quote.query.get_or_404(quote_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, fullname=form.name.data, author=current_user, quote_id = quote_id )
        db.session.add(comment)
        db.session.commit()
        # comments = Comment.query.all()
        flash('You comment has been created!', 'success')
        return redirect(url_for('posts.post', quote_id=quote_id))
    myquotes = Quote.query.order_by(Quote.posted_date.desc())
    return render_template('new-comment.html', title='New Comment', form=form, legend='New Comment', myquotes=myquotes)

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


#delete quote
@main.route('/quotes/delete/<int:id>')
@login_required
def delete_quote(quote_id):
    quote=Quote.query.get_or_404(quote_id)
    if quote.author != current_user:
        abort(403)
        db.session.delete(quote)
        db.session.commit()
        flash('Your Quote has been deleted!','success')
        return redirect(url_for('main.quote_page'))
#subscribe
@main.route("/subscribe")
def subscribe():
    return render_template('subscribe.html', title='Subscription')



#api quote
@main.route('/')
def index_api():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    quotes_api = get_quotes_api('popular')
    print(quotes_api)
    title = 'Welcome to Random Quotes'
    return render_template('index.html', title = title,popular = quotes_api)

