from flask import *
from flaskURL import app, db
from flaskURL.forms import formURL
from flaskURL.models import URL
from flaskURL.misc import randomizeKeyword
import string

SITE_ADDRESS='http://127.0.0.1:5000/' # Change to represent site address.

# Main Route #
##############
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = formURL()
    shorts = URL.query.all()

    # Validate Entry Form #
    #######################
    if form.validate_on_submit():
        
        # Get Required Information #
        ############################
        reqIP = str(request.headers.get('X-Forwarded-For', request.remote_addr)) # Client IP Addr.
        targURL = form.site.data                                                 # Target Address from Form
        shortURL = form.keyword.data                                             # Shortened URL Tag

        url = URL(short=shortURL, req_ip=reqIP, targ_url=targURL)                # Class object for DB entry

        # Validate a Full URL #
        #######################
        if targURL.find('https://') == -1 and targURL.find('http://') == -1:        # This does not appear to a a fullpath to a URL
            flash('This target url does not appear to be a full-path. Please provide a url that starts with https:// or http://', 'danger')

        else:
            # Validate Short #
            ##################
            existingEntry = URL.query.filter_by(short=shortURL).first()              # Query for an existing item w/ primary key.
            if existingEntry:                                                        # If the item already exists, lets add something unique to it.
                newShort = randomizeKeyword(shortURL)                                # Call our function for randomizing a keyword

                newUrl = URL(short=newShort, req_ip=reqIP, targ_url=targURL)

                db.session.add(newUrl)                                               # Adding instance of the URL class
                db.session.commit()                                                  # Commiting to sqlite database.

                session.pop('shortenedURL', None)                                    # Clear session variable for shortURL
                session['shortenedURL'] = SITE_ADDRESS + 'short/' + newShort         # Add to session variable
                return redirect(url_for('result'))                                   # Redirect to 'result' page.

            # Commit to DB #
            ################
            else:                                                                    # Short is unique. Lets commit to it.
                db.session.add(url)                                                  # Adding instance of the URL class
                db.session.commit()                                                  # Commiting to sqlite database.

                session.pop('shortenedURL', None)                                    # Clear session variable for shortURL
                session['shortenedURL'] = SITE_ADDRESS + 'short/' + shortURL         # Add to session variable
                return redirect(url_for('result'))                                   # Redirect to 'result' page.
    
    return render_template('home.html', form=form, shorts=shorts, site=SITE_ADDRESS)

# Form Result #
###############
@app.route("/result", methods=['GET', 'POST', 'PUT'])
def result():
    url = "INVALID"
    if 'shortenedURL' in session:
        url = session['shortenedURL']

    return render_template('result.html', url=url)

# About Page #
##############
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Redirect Page #
#################
@app.route("/short/<shortURL>")
def short(shortURL):
    shortRec = URL.query.filter_by(short=shortURL).first()
    if shortRec:
        targetURL = shortRec.targ_url
        return render_template('short.html', title='Redirecting!', targetURL=targetURL)

    else:
        flash('This shortcut, ' + shortURL + ', does not exist. Maybe you should create one!', 'danger')
        return redirect(url_for('home'))

    return shortURL
