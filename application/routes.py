import os

import pytube
from flask import render_template_string
from flask import Blueprint, make_response, request, Response, send_from_directory, abort
from flask import current_app, session, render_template, flash, stream_with_context
from sqlalchemy import update

from .Models import ContactQuery, SeachedSongsBucket
from .extensions import db
from .forms import ContactForm, SignUpForm

server = Blueprint("server", __name__, static_folder='static', template_folder='templates')


class YoutubeDownload:
    def __init__(self, link):
        self.link = link
        self.title = None
        self.views = None
        self.length = None
        self.rating = None
        self.video_id = pytube.extract.video_id(link)
        self.yt = pytube.YouTube(self.link)

    def get_info(self):
        self.title = self.yt.title
        self.views = self.yt.views
        self.length = str(self.yt.length) + " sec"
        self.rating = self.yt.rating

        return dict(Title=self.title,
                    Views=self.views,
                    Rating=self.rating,
                    Length=self.length)

    def get_streams(self):
        video_streams = self.yt.streams.filter(progressive=True)
        streams = [str(x).split(" ") for x in video_streams]
        stream_info = list()
        for stream in streams:
            itag = stream[1].split("=")[1].strip('"')
            mime_type = stream[2].split("=")[1].strip('"')
            res = stream[3].split("=")[1].strip('"')
            stream_info.append({"itag": itag,
                                "mime_type": mime_type,
                                "res": res})
        return stream_info

    def get_video(self, itag):
        ys = self.yt.streams.get_by_itag(itag)
        return ys


@server.route("/")
@server.route("/home")
@server.route("/index")
def home():
    return render_template('home.html')


@server.route('/video_detail', methods=["GET", "POST"])
def get_video_details():
    if request.method == "POST":
        link = request.form['video_link']
    elif request.method == "GET":
        link = session.get('link')
    else:
        abort(404)
    """
    regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(link)
    video_id = match.group('id')
    """
    session['link'] = link
    print(link)
    obj = YoutubeDownload(link)
    video_details = obj.get_info()
    stream_info = obj.get_streams()

    # adding in database
    songs = SeachedSongsBucket(video_details['Title'], obj.video_id, False)
    db.session.add(songs)
    db.session.commit()
    """
    return render_template("video_details.html", video_id="AGrl-H87pRU", video_link=link, video_details={},
                           video_streams={})
    """
    return render_template("video_details.html", video_id=obj.video_id, video_link=link, video_details=video_details,
                           video_streams=stream_info)


@server.route('/video_download/<itag>', methods=["GET", "POST"])
def get_video_download(itag):
    home_dir = os.path.expanduser('~')
    download_path = os.path.join(home_dir, 'Downloads')
    obj = YoutubeDownload(session.get('link'))
    ys = obj.get_video(itag)
    ys.download(download_path)

    update(SeachedSongsBucket).where(SeachedSongsBucket.song_id == obj.video_id).values(download=True)
    # db.session.add(stmt)
    db.session.commit()
    flash(f"You will find file at {download_path}")
    return render_template('home.html')


@server.route('/contactus', methods=['GET', "POST"])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        u = ContactQuery(name, email, message)
        db.session.add(u)
        db.session.commit()

        res = ContactQuery.query.filter(ContactQuery.email == email, ContactQuery.name == name).first()
        id = str(res).split(";")[0]

        flash(f"Your request id is {id}.\n Our team will contact you soon, Thanks.")
        return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)


@server.route('/submit', methods=('GET', 'POST'))
def submit():
    abort(404)
    return render_template('submit.html')


@server.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error_404.html'), 404


@server.route('/about')
def server_dabout():
    abort(404)
    return render_template('about.html')
