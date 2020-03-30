from django import forms

from .models import RoomBook

class RoomBookForm(forms.ModelForm):
    target_time = forms.DecimalField(label = 'Start Time')

    target_room = forms.DecimalField(label = 'Room Number')

    class Meta:
        model = RoomBook
        fields = [
            'target_time',
            'target_room'
        ]
    
    # def clean_target_time(self, *args, **kwargs):
    #     target_time = self.cleaned_data.get("target_time")
    #     if isinstance(target_time, int):
    #         raise forms.ValidationError("This is not a valid UCSB email")
    #     else:
    #         return email
