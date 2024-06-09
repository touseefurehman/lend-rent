class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['note']
        widgets = {'note': forms.NumberInput(attrs={'class': 'Stars'})}
        labels = {'note': 'Note /5'}