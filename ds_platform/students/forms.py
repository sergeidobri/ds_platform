from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label="Ответ", max_length=255)
