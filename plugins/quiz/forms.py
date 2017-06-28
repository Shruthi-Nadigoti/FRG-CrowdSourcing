from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, RadioField,SelectField
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileRequired
from flask.ext.babel import lazy_gettext

#Form for adding questions to a quiz
class Create_quiz(Form):
	question_text = TextAreaField('Question Text', [validators.Required("Field Required")]) # Input for question text
	file_field = FileField(lazy_gettext('Avatar'))
	oA = StringField('Option A', [validators.Required("Field Required")]) # Input for option A
	oB = StringField('Option B', [validators.Required("Field Required")]) # Input for option B
	oC = StringField('Option C', [validators.Required("Field Required")]) # Input for option C
	oD = StringField('Option D', [validators.Required("Field Required")]) # Input for option D
	#file_path=StringField('file_path',[validators.Required("Field Required")])
	correct_answer = RadioField('Correct Answer', choices = [('A','A'), ('B','B'), ('C','C'), ('D','D')]) # Radio Button to select the correct answer
	category = SelectField("Media Category",choices=[('Image','Image'),('Video','Video'), ('Audio','Audio'), ('Pdf','Pdf'), ('No Files Uploaded','No Files Uploaded')]) # Input for question category

# Form for taking response for a question
class Display_question(Form):
	submission = RadioField('submission')
# form for creating a quiz
class Add_quiz(Form):
	name=StringField('Quiz Name', [validators.Required("Field Required")])

class Display_quiz(Form):
	name = RadioField('name')
