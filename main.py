from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
Bootstrap(app)
app.secret_key = "very-secret-key"

# ------------------------------------ Database Configuration ------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# TODO Change if statements for has_sockets/has_wifi etc.

# ------------------------------------------ Flask Form for adding new cafe ---------------------------------------
class NewCafeForm(FlaskForm):
    name = StringField(label='Cafe Name', validators=[DataRequired()])
    map_url = StringField(label='Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField(label='Image URL', validators=[DataRequired(), URL()])
    location = StringField(label='City', validators=[DataRequired()])
    has_sockets = BooleanField(label='Do you have sockets for visitors?')
    has_toilet = BooleanField(label='Do you have WC for visitors?')
    has_wifi = BooleanField(label='Do you have WiFi?')
    can_take_calls = BooleanField(label='Can you take calls?')
    seats = StringField(label='How many seats do you have?', validators=[DataRequired()])
    coffee_price = StringField(label='What is the price for the coffee?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# --------------------------------- Flask Form for deleting cafe from database --------------------------------
class DeleteCafe(FlaskForm):
    name = StringField(label='Cafe Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# ------------------------------------------ Database ------------------------------------------
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    has_sockets = db.Column(db.Boolean, false_values=None)
    has_toilet = db.Column(db.Boolean, false_values=None)
    has_wifi = db.Column(db.Boolean, false_values=None)
    can_take_calls = db.Column(db.Boolean, false_values=None)
    seats = db.Column(db.String(30), nullable=True)
    coffee_price = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Cafe %r>' % self.name


db.create_all()

# ------------------------------------------ Flask Routes ------------------------------------------
@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=all_cafes)


@app.route("/add", methods=["POST", "GET"])
def add_new_cafe():
    new_cafe_form = NewCafeForm()
    if new_cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name=new_cafe_form.name.data,
            map_url=new_cafe_form.map_url.data,
            img_url=new_cafe_form.img_url.data,
            location=new_cafe_form.location.data,
            has_sockets=new_cafe_form.has_sockets.data,
            has_toilet=new_cafe_form.has_toilet.data,
            has_wifi=new_cafe_form.has_wifi.data,
            can_take_calls=new_cafe_form.can_take_calls.data,
            seats=new_cafe_form.seats.data,
            coffee_price=f"€{new_cafe_form.coffee_price.data}"
        )
        print(new_cafe)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html', form=new_cafe_form)


@app.route("/delete", methods=["POST", "GET"])
def delete_cafe():
    delete_cafe_form = DeleteCafe()
    if delete_cafe_form.validate_on_submit():
        cafe_name_to_delete = delete_cafe_form.name.data
        cafe_to_delete = Cafe.query.filter_by(name=cafe_name_to_delete).first()
        print(cafe_to_delete)

        db.session.delete(cafe_to_delete)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('delete.html', form=delete_cafe_form)


if __name__ == '__main__':
    app.run(debug=True)