from django.shortcuts import render
from .models import ArticlePost, Category, Tag,Banner,Link
from comment.models import Comment
import markdown
from .forms import ArticlePostForm

def index(request):
    allcategory = Category.objects.all()
    banner = Banner.objects.filter(is_active=True)[0:3]
    index_tui = ArticlePost.objects.filter(recommend__id=1)[:3]
    allarticle = ArticlePost.objects.all().order_by('-id')[0:10]
    links = Link.objects.all()
    # hots = ArticlePost.objects.all().order_by('?')[:10]#随机推荐
    # hots = ArticlePost.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hots = ArticlePost.objects.all().order_by('views')[:9]  # 通过浏览数进行排序
    context = {
        'allcategory':allcategory,
        'banner':banner,
        'index_tui':index_tui,
        'allarticle':allarticle,
        'hots':hots,
        'links':links,
    }
    return render(request, 'article/index.html',context)


def article_list(request):
    return render(request, 'list.html')


def article_detail(request, aid):
    article = ArticlePost.objects.get(id=aid)
    allcategory = Category.objects.all()  # 导航上的分类

    tags = Tag.objects.all()  # 右侧所有标签
    remen = ArticlePost.objects.filter(recommend__id=2)[:6]  # 右侧热门推荐
    hots = ArticlePost.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = ArticlePost.objects.filter(created_time__gt=article.created_time,
                                               category=article.category.id).first()
    netx_blog = ArticlePost.objects.filter(created_time__lt=article.created_time, category=article.category.id).last()
    article.views = article.views + 1
    article.save()

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])

    # 取出文章评论
    comments = Comment.objects.filter(article=aid)
    # context = {
    #     'article': article,
    #     'comments': comments,
    #     'hots':hots,
    # }
    return render(request, 'article/article.html', locals())


def article_search(request):
    return render(request, 'search.html')


def article_taglist(request):
    return render(request, 'taglist.html')

# 发布文章
def article_create(request):
    # 已有代码
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)

            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()