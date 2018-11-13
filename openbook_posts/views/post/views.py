from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from openbook_posts.views.post.serializers import GetPostCommentsSerializer, PostCommentSerializer, \
    CommentPostSerializer, DeletePostCommentSerializer


class PostComments(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, post_id):
        request_data = self._get_request_data(request, post_id)

        serializer = GetPostCommentsSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        max_id = data.get('max_id')
        limit = data.get('limit')
        user = request.user

        post_comments = user.get_comments_for_post_with_id(post_id, max_id=max_id, limit=limit)

        return CommentPostSerializer(data=post_comments, many=True)

    def put(self, request, post_id):
        request_data = self._get_request_data(request, post_id)

        serializer = PostCommentSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        comment_text = data.get('text')
        user = request.user

        with transaction.atomic():
            post_comment = user.comment_post_with_id(post_id=post_id, text=comment_text)

        return CommentPostSerializer(data=post_comment)

    def _get_request_data(self, request, post_id):
        request_data = request.data.dict()
        request_data['post_id'] = post_id
        return request_data


class PostCommentItem(APIView):
    def delete(self, request, post_id, post_comment_id):
        request_data = self._get_request_data(request, post_id, post_comment_id)

        serializer = DeletePostCommentSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        post_id = data.get('post_id')
        post_comment_id = data.get('post_comment_id')
        user = request.user

        with transaction.atomic():
            user.delete_comment_with_id_for_post_with_id(post_comment_id=post_comment_id, post_id=post_id, )

        return Response({
            'message': 'Done!'
        })

    def _get_request_data(self, request, post_id, post_comment_id):
        request_data = request.data.dict()
        request_data['post_id'] = post_id
        request_data['post_comment_id'] = post_comment_id
        return request_data
