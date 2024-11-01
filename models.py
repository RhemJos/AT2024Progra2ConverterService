from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class FilePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
