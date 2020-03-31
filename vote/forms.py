from django import forms


class CreateVoteForm(forms.Form):
    voterid = forms.IntegerField()
    age = forms.IntegerField()
    sex = forms.ChoiceField(choices=[('m', 'male'), ('f', 'female')])
    choice = forms.CharField(max_length=200)


class CreatePollForm(forms.Form):
    pollid = forms.IntegerField()
    name = forms.CharField(max_length=100)
    # end_date = forms.DateField()
