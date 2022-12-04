from main import app, db
from flask import render_template, redirect, url_for, flash, request
from main.models import User, Pacijenti
from main.form import TerminReservationForm, CreateUserForm, LoginForm, TerminDeleteForm
from flask_login import login_user, logout_user, current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    """ Funkcija provjerava da li je korisnki ulogovan, ako nije salje ga na login page. Zatim u ovisnoti da li je korisnik doktor ili ne
    funkcija uzima iz baze podataka podatke id termina. Ako je doktor svi termini, ako nije onda samo licni termini korisnika. Ako je request == 'POST'
    tada ce obrisati pronadjeni termin na osnovu korisnikovog id-a. Samo korisnik ima pravo da brise svoje licne termine."""
    if current_user.is_authenticated:
        user_appointments = Pacijenti.query.filter_by(ime=current_user.id)
        form = TerminDeleteForm()
        if current_user.doctor:
            user_appointments = Pacijenti.query.all()
        else:
            if request.method == 'POST':
                termin_id = request.form.get('termin_delete')
                Pacijenti.query.filter_by(id=termin_id).delete()
                db.session.commit()
                flash('Uspijesno ste otkazali termin.')
                return redirect(url_for('home_page'))
        return render_template('home_page.html', user_appointments=user_appointments, form=form)
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """ Funkcija provjerava da je request 'POST', ako nije salje korisnika na login page. U slucaju 'POST' request-a
    funkcija zatim provjerava da li je ispravan password i email, ako jeste uloguje korisnika preko login_mamager-a, zatim ga salje na home page."""
    form = LoginForm()
    if request.method == 'POST':
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcome {attempted_user.username}.', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Pogresan e-mail ili password', category='danger')
    if form.errors != {}:
        for errMsg in form.errors.values():
            flash(errMsg, category='danger')
    return render_template('login_page.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """ Funkcija provjerava da li je form-a submitovana, ako nije salje na register page. Ako jeste uzima podatke iz forme te preko njih pravi novog korisnika u bazi podataka.
    Takodjer, provjera da li ima error-a. Ako je sve uspjesno zavrseno, pravi cookie sa korisnickim podacima preko login_manager funkcije login_user(korisnik),
     zatim salje na home page"""
    form = CreateUserForm()
    if form.validate_on_submit():
        user_to_create = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password1.data
        )     

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! Welcome {user_to_create.username}.')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for errMsg in form.errors.values():
            flash(f'Error while creating user: {errMsg}', category='danger')
        
    return render_template('register_page.html', form=form)


@app.route('/logout')
def logout_page():
    """Funkcija brise korisnicki cookie iz browsera preko jednostavne 'logout_user()' funkcije iz login_manager-a"""
    logout_user()
    flash('You are logged out!')

    return redirect(url_for('home_page'))


@app.route('/rezervacija', methods=['GET', 'POST'])
def rezervacija_page():
    """ Funkcija salje formu za rezevraciju termina u front-end. U slucaju 'POST' request-a, uzima pristigle podatke iz forme, te pravi novog pacijenta.
    Iz frontenda mora biti korisnicki.id vracen da bi uspijesno napravili strani kljuc za Pacijent """
    form = TerminReservationForm()
    if request.method == 'POST':
        pacijent_to_create = Pacijenti(
            ime = current_user.id,
            termin = form.termin.data
        )
        db.session.add(pacijent_to_create)
        db.session.commit()
        flash('Termin uspijesno zakazan!', category='success')
        return redirect(url_for('home_page'))
    return render_template('rezervacija.html', form=form)