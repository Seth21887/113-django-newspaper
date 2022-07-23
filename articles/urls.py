from django.urls import path
from .views import ArticleCreateView, ArticleDeleteView, ArticleDetailView, ArticleListView, ArticleUpdateView, ArticleDraftListView
#we can also import the views like this: from articles import views

urlpatterns = [
    path('', ArticleListView.as_view(), {"section": 1, "status": 1}, name="home"),
    path('<int:section>/<int:status>/', ArticleListView.as_view(), name='articles_list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='articles_edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),
    path('new/', ArticleCreateView.as_view(), name='articles_new'),
    path('drafts/', ArticleDraftListView.as_view(), name='draft_post_list'),
]