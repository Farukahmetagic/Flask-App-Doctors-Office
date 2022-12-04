from main import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)
    appointment = db.relationship('Pacijenti', backref='user_termin', lazy=True)
    doctor = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') 
    

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Pacijenti(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    ime = db.Column(db.Integer(), db.ForeignKey('user.id'))
    termin = db.Column(db.String(), nullable=False)
