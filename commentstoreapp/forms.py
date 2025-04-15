from django import forms


class InsertNewComment(forms.Form):
    name = forms.CharField(label="Insert a name:", max_length=100)
    visit_date = forms.DateField(label="Insert the date of visit:", input_formats=['%d/%m/%Y'])
    comment_str = forms.CharField(label="Insert a comment:", max_length=500)
