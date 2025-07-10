from flask import Flask, render_template, url_for, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)


# Модели
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))


# Маршруты
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events')
def show_events():
    events = Event.query.order_by(Event.start_time.asc()).all()
    return render_template('events.html', events=events)


@app.route('/events/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event = Event(
            title=request.form['title'],
            description=request.form['description'],
            start_time=datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M'),
            end_time=datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M'),
            location=request.form['location']
        )
        db.session.add(event)
        db.session.commit()
        flash('Мероприятие успешно создано!')
        return redirect(url_for('show_events'))

    return render_template('create_event.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)