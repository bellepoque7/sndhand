from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.
def post_list(request):

    
    qs = Post.objects.all()
    #발행날짜가 현재 시간보다 작거나 같은것만
    qs = qs.filter(published_date__lte = timezone.now())
    #발행일에 대한 오름차순 정렬로 가져오라
    qs = qs.order_by('published_date') 
    
    return render(request, 'blog/post_list.html', {
        'post_list':qs,
    })


#url.py가 처리하는 정규표현식을 받아서 처리할것이다.
def post_detail(request, pk):

    #예외처리문을 추가하는 대신 메소드로 변경    
    post = get_object_or_404(Post, pk = pk)

    return render(request, 'blog/post_detail.html', {
        'post': post,
    })

def post_new(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        #유효성검사항목
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.pk)
        
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {
        'form' :form
    })


#수정하는 기능 삽입하기
def post_edit(request, pk):    
    post = get_object_or_404(Post, pk = pk)

    if request.method == "POST":

        #위의 post_new와 동일하지만 instance 파라미터가 들어간다. 수정할 대상만 정하는것
        form = PostForm(request.POST, request.FILES, instance = post)
        #유효성검사항목
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.pk)
        
    else:
        form = PostForm(instance = post)

    return render(request, 'blog/post_edit.html', {
        
    })