# blog/routes.py

from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)

@app.route("/edit-entry/<int:entry_id>", methods=["GET", "POST"])
@app.route("/edit-entry", methods=["GET", "POST"])
def edit_entry(entry_id=None):
    errors = None
    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
            else:
                errors = form.errors
    else:
        form = EntryForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
                )
            db.session.add(entry)
            db.session.commit()
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)