from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

# 文章评论

class Comment(MPTTModel):
    # 被评论的文章
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    # 评论的发布者
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # body = models.TextField()
    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # mptt 树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    # 记录二级评论回复给谁 str
    reply_to = models.ForeignKey(User, null=True, blank=True,
                                 on_delete=models.CASCADE, related_name='replyers')

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]

# class Comment(models.Model):
#     # 被评论的文章
#     article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments')
#     # 评论的发布者
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
#     body = models.TextField()
#     created_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('created_time',)
#
#     def __str__(self):
#         return self.body[:20]
