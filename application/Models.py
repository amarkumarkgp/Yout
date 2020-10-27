from .extensions import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class ContactQuery(db.Model):
    __tablename__ = "contactus"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    message = Column(String(50))

    def __init__(self, name=None, email=None, message=None):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return "{}; {}; {}".format(self.id, self.name, self.name)


class SeachedSongsBucket(db.Model):
    __tablename__ = "searchedsongsbucket"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    song_id = Column(String(50))
    download = Column(Boolean)
    datetime = Column(DateTime())

    def __init__(self, title=None, song_id=None, download=None, dtime=None, ):
        self.title = title
        self.song_id = song_id
        self.download = download
        self.datetime = datetime.now()

    def __repr__(self):
        return "{}, {}; {}; {}, {}".format(self.id, self.title, self.song_id, self.datetime, self.download)
