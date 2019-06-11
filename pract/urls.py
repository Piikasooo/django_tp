from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from pract.views import  base_view,\
    category_view,\
    petition_view,\
    petition_create_view,\
    save_petition_to_base_view,\
    account_view,\
    registration_view,\
    login_view,\
    pop_view,\
    notPop_view,\
    save_vote_to_base_view,\
    search_view

urlpatterns = [
    url(r'^petition/(?P<petition_slug>[-\w]+)/$', petition_view, name='petition_detail'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    url(r'create_petition/$', petition_create_view, name='create_petition'),
    url(r'^save_vote/$', save_vote_to_base_view, name='save_vote'),
    url(r'^save_petition/$', save_petition_to_base_view, name='save_pet'),
    url(r'^account/$', account_view, name='account'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    url(r'^pop/$', pop_view, name='pop'),
    url(r'^notPop/$', notPop_view, name='notPop'),
    url(r'^search/$', search_view, name='search'),
    url(r'^$', base_view, name='base'),
]