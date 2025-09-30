from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class FileUploadForm(FlaskForm):
    # We limit the allowed extensions to prevent malicious uploads
    file = FileField(
        'PDF or Text File',
        validators=[
            FileRequired(),
            FileAllowed(['pdf', 'txt'], 'Only PDF and TXT files are allowed!')
        ]
    )
    submit = SubmitField('Generate Podcast')