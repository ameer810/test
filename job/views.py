from django.shortcuts import render, redirect, get_object_or_404, HttpResponsePermanentRedirect
from .models import Job, Apply, Comments
from django.core.paginator import Paginator
from .form import ApplyForm, JobForm, CommentsForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .filter import JobFilter
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import mixins
from . import serializers


# Create your views here.


def job_detail(request, slug):
    is_fav = False
    job_detail = Job.objects.get(slug=slug)
    if request.is_ajax():
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user
            job_detail.apply_count += 1
            myform.job = job_detail
            myform.save()
            job_detail.save()
            return JsonResponse()



    else:
        form = ApplyForm()

    k = job_detail.Vacancy - job_detail.apply_count
    comform = CommentsForm()
    if request.method == 'POST':
        comform = CommentsForm(request.POST)
        if comform.is_valid():
            myform = comform.save(commit=False)
            myform.user = request.user
            myform.job = job_detail
            myform.save()
    else:
        comform = CommentsForm()
    all_comments = Comments.objects.all()
    context = {'k': k, 'job': job_detail, 'form1': form, 'is_fav': is_fav,'comform':comform,'all_comments':all_comments}

    return render(request, 'job/job_detail.html', context)


def job_list(request):
    try:
        order = request.GET['order']
        if order == 'From Oldest':
            job_list = Job.objects.all().order_by('published_at')

        if order == 'Job Applied':
            job_list = Job.objects.all().order_by('-apply_count')


    except:
        job_list = Job.objects.all()

    myfilter = JobFilter(request.GET, queryset=job_list)
    job_list = myfilter.qs

    paginator = Paginator(job_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'jobs': page_obj, 'myfilter': myfilter, 'dd': job_list}  # template name
    return render(request, 'job/job_list.html', context)


def Apply_view(request):
    Apply_list = Apply.objects.filter(user=request.user).order_by('user')
    job_list = Job.objects.all()

    return render(request, 'job/exampl.html', {'Apply_list': Apply_list, 'dd': job_list})


def Apply_view_2(request):
    Apply_list = Apply.objects.all()

    return render(request, 'job/exampl_2.html', {'Apply_list': Apply_list})


def delete_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.delete()
    return redirect(reverse('jobs:job_list'))


@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()

            return redirect(reverse('jobs:job_list'))


    else:
        form = JobForm()

    return render(request, 'job/add_job.html', {'form': form})


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {'favourite_posts': favourite_posts}
    return render(request, 'job/fil.html', context)


def post_fav(request, slug):
    post = Job.objects.get(slug=slug)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return redirect(reverse('jobs:job_detail', kwargs={'slug': post.slug}))


'''def job_like(request, slug):
    post = Job.objects.get(slug=slug)
    if post.likee.filter(id=request.user.id).exists():
        post.likee.remove(request.user)
    else:

        post.likee.add(request.user)
    return redirect(reverse('jobs:job_detail', kwargs={'slug': post.slug}))'''


def job_edit(request, slug):
    job = Job.objects.get(slug=slug)
    l=job.owner

    if request.method == 'POST':

        formd = JobForm(request.POST, instance=job)
        if formd.is_valid():
            formd.job = job
            formd.save()
            job.save()



    else:
        formd = JobForm(instance=job)
    return render(request,'job/job_detail_edit.html',{'l':l,'formdel':formd})


class JobListApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = Job.objects.all()
    serializer_class = serializers

    def get(self, request):
        return self.list(request)

