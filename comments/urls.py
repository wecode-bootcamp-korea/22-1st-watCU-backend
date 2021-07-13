from django.urls    import path

from comments.views import CommentView, NestedCommentView
from likes.views    import LikeView

urlpatterns = [
    path('', CommentView.as_view()),
    path('/<int:comment_id>', CommentView.as_view()),
    path('/<int:comment_id>/comments', NestedCommentView.as_view()),
    path('/<int:comment_id>/like', LikeView.as_view()),
]