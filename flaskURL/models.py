from datetime import datetime
from flaskURL import db

class URL(db.Model):
    short = db.Column(db.String, primary_key=True)
    req_ip = db.Column(db.String(120), nullable=False)
    targ_url = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"shortened url: '{self.short}', Target: '{self.targ_url}', Date: '{self.date}', IP Origin: '{self.req_ip}'"