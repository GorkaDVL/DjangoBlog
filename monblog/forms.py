from django import forms
from .models import Post, Category, Comment, Profile

#choices = [('Comics', 'Comics'), ('Ciné', 'Ciné'), ('Série', 'Série'),]
choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'author', 'category', 'body', 'snippet', 'header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        
        self.fields['title'].label = "Titre"
        self.fields['title_tag'].label = "Tag"
        self.fields['category'].label = "Catégorie"
        self.fields['body'].label = "Contenu"
        self.fields['snippet'].label = "Extrait"
        self.fields['header_image'].label = "Image d'en-tête"
          

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'body', 'snippet','header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'This is title placeholder stuff'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
             #'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        
        self.fields['title'].label = "Titre"
        self.fields['title_tag'].label = "Tag"
      
        self.fields['body'].label = "Contenu"
        self.fields['snippet'].label = "Extrait"
        self.fields['header_image'].label = "Image d'en-tête"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        

        widgets = {
            
            'body': forms.Textarea(attrs={'class': 'form-control'}),
           
            
        } 