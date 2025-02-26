from django.urls import path
from .views import candidate_list, cast_vote

urlpatterns = [
    path('api/candidates/', candidate_list, name='candidate_list'),
    path('api/vote/', cast_vote, name='cast_vote'),
]
