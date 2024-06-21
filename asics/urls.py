from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path("login/", views.login_users, name="login"),
    path("logout/", views.logout_users, name="logout"),
    path("getschemas", views.getschemas, name="schemas"),
    path("gettablebyschema", views.gettablesbyschema, name="tables"),
    path("getcolumns", views.getcolumnsoftable, name="columns"),
    path("fetchdata", views.fetchdata, name="fetch"),
    path("getrelatedtables", views.get_related_tables, name="related_tables"),
    path("populate", views.populate_relation, name="populate")
]