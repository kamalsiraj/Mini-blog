from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ganti dengan key yang aman
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/soal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Soal
class Soal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topik = db.Column(db.String(100), nullable=False)
    soal = db.Column(db.String(200), nullable=False)
    jawaban = db.Column(db.String(100), nullable=False)

# Form untuk menjawab soal
class AnswerForm(FlaskForm):
    jawaban = StringField('Jawaban', validators=[DataRequired()])
    submit = SubmitField('Kirim Jawaban')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    topic = request.form['topic']
    difficulty = request.form['difficulty']
    
    soal = Soal.query.filter_by(topik=topic).first()  # Ambil soal pertama berdasarkan topik
    form = AnswerForm()
    return render_template('quiz.html', soal=soal, form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = AnswerForm()
    if form.validate_on_submit():
        jawaban = form.jawaban.data
        soal_id = request.form['soal_id']
        soal = Soal.query.get(soal_id)
        
        if jawaban.lower() == soal.jawaban.lower():
            feedback = "Jawaban Anda Benar!"
        else:
            feedback = f"Jawaban Anda Salah. Jawaban yang benar adalah: {soal.jawaban}"
        
        return render_template('result.html', feedback=feedback, soal=soal)

# Create the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
