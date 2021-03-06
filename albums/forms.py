from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext as _
from models import *
from utils import admin_mode

import re, urllib2
from datetime import datetime

def cln_build_report(form):
    url = form.cleaned_data['build_report']
    if not url:
        return url
    match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
    if not match:
        raise forms.ValidationError(_("This link doesn't point to a valid forum topic. Please correct the error"))
    url = "http://www.%s" % match.group(0)
    return url

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('created', 'modified', 'last_upload', 'views', 'votes', 'order', 'trash', 'cover', 'clean_title')
        widgets = {
            'user': forms.HiddenInput(),
        }
        
    def clean_build_report(self):
        return cln_build_report(self)
    
    def __init__(self, *args, **kwargs):
        self.user = None
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        else:
            initial = kwargs.get('initial', None)
            if initial:
                self.user = initial.get('user', None)
        
        if 'admin_mode' in kwargs:
            admin = kwargs.pop('admin_mode')
        else:
            admin = admin_mode(self.user)
        
        super(AlbumForm, self).__init__(*args, **kwargs)
        # limit visible categories for regular users
        if not self.user or not admin:
            self.fields['category'].queryset = Category.objects.filter(public=True)

class EditAlbumForm(AlbumForm):
    class Meta:
        model = Album
        fields = ('title', 'description', 'build_report', 'category', 'cover', 'order', 'public', 'writable_to', 'trash')
        widgets = {
            'description': forms.Textarea(),
        }
    
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        album = kwargs.pop('instance')
        self.fields['cover'].queryset = Photo.objects.filter(album=album).select_related('user', 'album', 'album__cover')
    
    def save(self, *args, **kwargs):
        if self.instance.trash:
            self.instance.title = "trash_%s_%s" % (datetime.now().strftime('%d%m%Y_%H.%M.%s'), self.instance.title)
        super(EditAlbumForm, self).save(*args, **kwargs)
    
    def clean_build_report(self):
        return cln_build_report(self)

class EditAlbumFormAjax(EditAlbumForm):
    class Meta:
        model = Album
        fields = (
            'title', 'description', 'build_report', 
            'category', 'public', 'writable_to', 'cover',
            'user'
            )
        widgets = {
            'user': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = Photo.objects.none()

class AlbumGroupForm(forms.ModelForm):
    class Meta:
        model = AlbumGroup
        #widgets = {'users': forms.HiddenInput()}
    
    def __init__(self, *args, **kwargs):
        super(AlbumGroupForm, self).__init__(*args, **kwargs)
        queryset = self.fields['users'].queryset
        self.fields['users'].queryset = queryset.order_by('username')
    

class AmountForm(forms.Form):
    amount = forms.IntegerField(required=False, min_value=1, max_value=50)

def albums_as_choices(querysets, trash=False):
    albums = []
    for qs_dict in querysets:
        temp = []
        for album in qs_dict['qs']:
            label = album.__unicode__()
            temp.append([album.id, label])
        if temp:
            albums.append([qs_dict['optgroup'], temp])
    return albums

class PickAlbumForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)
    
    def __init__(self, user, *args, **kwargs):
        try:
            browse = kwargs.pop('browse')
        except KeyError: #key not suplied
            browse = False
        try:
            trash = kwargs.pop('trash')
        except KeyError: #key not suplied
            trash = False
        try:
            admin = kwargs.pop('admin_mode')
        except KeyError:
            admin = admin_mode(user)
        super(PickAlbumForm, self).__init__(*args, **kwargs)
        #own_albums = Album.objects.filter(user=user, writable_to="u", trash=False).order_by('order', 'title')
        
        if admin:
            q = Q(trash=trash)
        else:
            q = Q(user=user, trash=trash)
        
        own_albums = Album.objects.filter(q).order_by('order', 'title')
        group_albums = Album.objects.filter(
            writable_to = "g", 
            trash = trash, 
            albumgroup__in = user.albumgroup_set.all()
            ).order_by('order', 'title')
        public_albums = Album.objects.filter(writable_to="o", trash=trash).order_by('order', 'title')
        
        #order is important here
        querysets = [
            {'optgroup': _("Own albums"), 'qs': own_albums},
            {'optgroup': _("Group albums"), 'qs': group_albums},
            {'optgroup': _("Public albums"), 'qs': public_albums},
            ] 
        
        self.fields['album'].queryset = (own_albums | public_albums | group_albums).select_related('user')
        self.fields['album'].choices = albums_as_choices(querysets, trash=trash)
        if browse:
            self.fields['album'].required = False

class PickOwnAlbumForm(PickAlbumForm):
    def __init__(self, user, *args, **kwargs):
        super(PickOwnAlbumForm, self).__init__(user)
        
        own_albums = Album.objects.select_related('user').filter(user=user, trash=False).order_by('order', 'title')
        group_albums = Album.objects.filter(
            writable_to = "g", 
            trash = False, 
            albumgroup__in = user.albumgroup_set.all()
            ).order_by('order', 'title')
        
        querysets = [
            {'optgroup': _("Own albums"), 'qs': own_albums},
            {'optgroup': _("Group albums"), 'qs': group_albums},
            ]
        self.fields['album'].queryset = (own_albums | group_albums).select_related('user')
        self.fields['album'].choices = albums_as_choices(querysets, trash=False)

class OrderAlbumForm(PickAlbumForm):
    album_before = forms.ModelChoiceField(queryset=Album.objects.none(), required=False)
    album_after = forms.ModelChoiceField(queryset=Album.objects.none(), required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(OrderAlbumForm, self).__init__(user, *args, **kwargs)
        self.fields['album_before'].queryset = self.fields['album'].queryset
        self.fields['album_after'].queryset = self.fields['album'].queryset

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('id', 'description', 'order')
        widgets = {
            'description': forms.Textarea(),
        }

class EditPhotoForm(forms.ModelForm):
    set_as_cover_photo = forms.BooleanField(required=False)
    class Meta:
        model = Photo
        fields = ('album', 'description', 'order', 'set_as_cover_photo')
        widgets = {
            'description': forms.Textarea(),
        }
    
    def __init__(self, user, *args, **kwargs):
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        photo = kwargs['instance']
        
        if admin_mode(user):
            albums = Album.objects.all()
        else:
            albums = Album.objects.filter(Q(user=photo.user)|Q(public=True), trash=False)
        self.fields['album'].queryset = albums
        self.fields['album'].empty_label = None
    
    def save(self, *args, **kwargs):
        super(EditPhotoForm, self).save(*args, **kwargs)
        if self.fields['set_as_cover_photo']:
            self.instance.album.cover = self.instance
            self.instance.album.save()

class AddPhotoForm(forms.ModelForm):
    class Meta:
        fields = ('album', 'image')

class UploadFromURLForm(forms.Form):
    url = forms.URLField(required=False, label=_("link"), help_text=_("Upload a picture from url"))
    
    def clean_url(self):
        url = self.cleaned_data['url']
        if url != '':
            try:
                d = urllib2.urlopen(url)
                content_type = d.info()['Content-Type']
                valid = False
                for ext in settings.VALID_IMG_EXTENSIONS:
                    valid_content_type = "image/%s" % ext.replace('.', '')
                    if valid_content_type in content_type:
                        valid = True
                        break;
                if not valid:
                    raise forms.ValidationError(_("Make sure the link points to a jpg or png image."))
            except urllib2.HTTPError:
                raise forms.ValidationError(_("Could not download the image from the url"))
        return url

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        widgets = {
            'user': forms.HiddenInput(),
        }

class SearchForm(forms.Form):
    search = forms.CharField(max_length=256, label=_("Keywords"))

