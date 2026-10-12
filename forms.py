from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError

OBLIGATORIO = 'Este campo es obligatorio.'


def integer_check(form, field):
    if type(field.data) != int:
        raise ValidationError('Ingresa un valor numérico.')
    if field.data < 0:
        raise ValidationError('Ingresa un valor positivo.')


def negativ_check(form, field):
    if field.data < 0:
        raise ValidationError('Ingresa un valor positivo.')


class BaseForm(FlaskForm):
    class Meta:
        # mensajes de error de WTForms en español
        locales = ['es']


class PositionsForm(BaseForm):
    amount = FloatField('Cantidad', validators=[DataRequired(OBLIGATORIO), negativ_check])
    unit = SelectField('Unidad', choices=[('', '...'), ('Conversión', 'Conversión'), ('Hora', 'Hora')], validators=[DataRequired(OBLIGATORIO)])
    price = FloatField('Precio/Unidad', validators=[DataRequired(OBLIGATORIO), negativ_check])
    description = StringField('Descripción', validators=[DataRequired(OBLIGATORIO), Length(max=500, message='Máximo 500 caracteres.')])


class InvoiceForm(BaseForm):
    start_date = DateField('Inicio', validators=[DataRequired(OBLIGATORIO)])
    end_date = DateField('Fin', validators=[DataRequired(OBLIGATORIO)])
    invoice_number = StringField('Factura n.º', validators=[DataRequired(OBLIGATORIO)])
    company_name = StringField('Empresa', validators=[DataRequired(OBLIGATORIO)])
    firstname = StringField('Nombre', validators=[DataRequired(OBLIGATORIO)])
    lastname = StringField('Apellido', validators=[DataRequired(OBLIGATORIO)])
    street = StringField('Calle', validators=[DataRequired(OBLIGATORIO)])
    house_number = StringField('Número', validators=[DataRequired(OBLIGATORIO)])
    city = StringField('Ciudad', validators=[DataRequired(OBLIGATORIO)])
    zip_code = IntegerField('Código postal', validators=[DataRequired(OBLIGATORIO), integer_check])
