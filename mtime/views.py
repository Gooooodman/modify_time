#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from markdown import markdown  
import subprocess
from django.utils import timezone
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext,render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.template import RequestContext, loader
from .models import Question,Choice,Post
from django.core.urlresolvers import reverse

from django.views import generic
from django.views.generic import TemplateView

from .models import *
from .forms import PostForm,ContactForm,HostsListForm

import time


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now())
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('mtime:post_detail', pk=post.pk)
            #return HttpResponseRedirect(reverse('mtime:post_detail', args=(post.pk,)))
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('mtime:post_detail', pk=post.pk)
            #return HttpResponseRedirect(reverse('mtime:post_detail', args=(post.pk,)))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


########### FORM    ################
@csrf_exempt
def contact_author(request):
    if request.method == 'POST':#提交请求时才会访问这一段，首次访问页面时不会执行
        form = ContactForm(request.POST)
        if form.is_valid():#说明各个字段的输入值都符合要求
            cd = form.cleaned_data#只有各个字段都符合要求时才有对应的cleaned_data
            print form.clean_message()
            # print cd['subject']
            # print cd['email']
            # print cd['message']
            return HttpResponseRedirect(reverse('mtime:thanks'))
            #第二种方式
            #return HttpResponseRedirect('/mtime/thanks')
        #else:#有部分字段不符合要求，会有error相关信息给加到form中去，需要覆盖掉
            # print form
            # print '数据不符合要求'
            # print form['subject'].errors
            # print form['email'].errors
            # print form['message'].errors
    else:#首次访问该url时没有post任何表单
        form = ContactForm()#第一次生成的form里面内容的格式
        # print form
        # print form.is_valid()

    #“首次访问”和“提交的信息不符合要求”时被调用
    return render_to_response('contact_author.html', {'form': form})


def thanks(request):

    return render_to_response('thanks.html')



########### FORM    ################

# def HostsList(request):
#     all_host= HostList.objects.all()
#     return render_to_response('host_list.html', {'all_host_list': all_host})


#使用通用视图
class HostsList(generic.ListView):
    template_name = 'host_list.html'
    context_object_name = 'all_host_list'
    def get_queryset(self):
        return HostList.objects.all()






@csrf_exempt
def create_host(request):
    if request.method == 'POST':
        form = HostsListForm(request.POST)
        if form.is_valid:
            form.save()
            cd = form.cleaned_data
            print cd
            return HttpResponseRedirect(reverse('mtime:HostsList'))
        else:
            print '数据不符合要求'
    else:
        form = HostsListForm()
    #return render(request, 'create_host.html', locals())
    #print form
    return render_to_response('create_host.html', {'form': form})


# def index(request):
#     #return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]    
#     #context = RequestContext(request, {
#     #    'latest_question_list': latest_question_list,
#     #})
#     #template = loader.get_template('index_1.html')
#     #return HttpResponse(template.render(context))
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'index_1.html', context)



# def detail(request, question_id):
# 	#one
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'detail.html', {'question': question})
#     #two
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'detail.html', {'question': question})    

#def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'results.html', {'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mtime:results', args=(p.id,)))

#generic views
class IndexView(generic.ListView):
    template_name = 'index_1.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


# def get_queryset(self):
#     """
#     Return the last five published questions (not including those set to be
#     published in the future).
#     """
#     return Question.objects.filter(
#         pub_date__lte=timezone.now()
#     ).order_by('-pub_date')[:5] 





# tem view
class AboutView(TemplateView):
    template_name = "about.html"





@csrf_exempt
def index2(request):
    if request.method=='POST':
        lang=request.POST["lang"]
        version=request.POST["version"]
        mtime=request.POST["mtime"]
        if version == "test":
            ch="最新服"
            #cmd="python mtime/modify_time.py --lang %s --time '%s' --new"%(lang,mtime)
            cmd="python mtime/modify_time2.py --lang %s --time '%s' --new"%(lang,mtime)
        else:
            ch="线上服"
            #cmd="python mtime/modify_time.py --lang %s --time '%s' --online"%(lang,mtime)
            cmd="python mtime/modify_time2.py --lang %s --time '%s' --online"%(lang,mtime)
        print cmd
        ret=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        stdout,stderr = ret.communicate()
        if ret.returncode != 0:
            ret = "修改%s时间失败!!!..请联系运维进行更改..\n失败信息如下:%s,%s"%(lang,stdout,stderr)
        else:
            ret = "修改%s时间[ %s ]成功!请进行测试..."%(lang,mtime)
        message="修改%s %s,时间为: %s"%(lang,ch,mtime)
        kwvars= {"lang":lang,"version":version,"mtime":mtime,"message":message,"ret":ret,}
        #print kwvars
        #return render_to_response('index.html',kwvars)
        import json
        return HttpResponse(json.dumps(kwvars),content_type='application/json')

    else:
        #台湾区域
        #tw_cmd = "python mtime/modify_time.py --lang tw --nowtime"
        tw_cmd = "python mtime/modify_time2.py --lang tw --nowtime"
        print time.strftime("%Y-%m-%d %X", time.localtime())+":"+tw_cmd
        tw_ret=subprocess.Popen(tw_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        tw_stdout,tw_stderr = tw_ret.communicate()
        if tw_ret.returncode != 0:
            twret = "查看tw当前时间失败!!!..请联系运维护..\n失败信息如下:"+tw_stdout+tw_stderr
        else:
            twret = "查看tw当前时间成功!!!..请进行选择测试."
        tw_time=tw_stdout.strip("\n")
        #英语区域
        #en_cmd = "python mtime/modify_time.py --lang en --nowtime"
        en_cmd = "python mtime/modify_time2.py --lang en --nowtime"
        print time.strftime("%Y-%m-%d %X", time.localtime())+":"+en_cmd
        en_ret=subprocess.Popen(en_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        en_stdout,en_stderr = en_ret.communicate()
        if en_ret.returncode != 0:
            enret = "查看en当前时间失败!!!..请联系运维护..\n失败信息如下:"+en_stdout+en_stderr
        else:
            enret = "查看en当前时间成功!!!..请进行选择测试."
        en_time=en_stdout.strip("\n")
        #泰语区域
        #tl_cmd = "python mtime/modify_time.py --lang tl --nowtime"
        tl_cmd = "python mtime/modify_time2.py --lang tl --nowtime"
        print time.strftime("%Y-%m-%d %X", time.localtime())+":"+tl_cmd
        tl_ret=subprocess.Popen(tl_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        tl_stdout,tl_stderr = tl_ret.communicate()
        if tl_ret.returncode != 0:
            tlret = "查看en当前时间失败!!!..请联系运维护..\n失败信息如下:"+tl_stdout+tl_stderr
        else:
            tlret = "查看en当前时间成功!!!..请进行选择测试."
        tl_time=tl_stdout.strip("\n")

        stdout = 'en测试服当前时间:%s \ntw测试服当前时间:%s \ntl测试服当前时间:%s'%(en_time,tw_time,tl_time)
        kwvars = {
            'enret':enret,
            'twret':twret,
            'tlret':tlret,
            'stdout':stdout,
            'request':request,
        }  
        #print request.META['HTTP_USER_AGENT']
        return render_to_response('index_css.html',kwvars)		




def back_time(request):
    lang=request.GET.get("lang")
    version=request.GET.get("version")
    if version == "test":
        server="最新服"
        cmd = "python mtime/modify_time2.py --lang %s --new --backnow"%lang
    elif version == "online":
        server="线上服"
        cmd = "python mtime/modify_time2.py --lang %s --online --backnow"%lang
    #mtime=request.GET["mtime"]
    #print lang,version
    print time.strftime("%Y-%m-%d %X", time.localtime())+":"+cmd
    ret=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    stdout,stderr = ret.communicate()
    if ret.returncode != 0:
        ret = "恢复%s - %s 时间失败!!!..请联系运维进行更改..\n失败信息如下:%s,%s"%(lang,version,stdout,stderr)
        print ret
        message = "恢复%s - %s 时间失败!!!..请联系运维查看.."%(lang,server)
    else:
        message = "恢复%s - %s 时间成功!!!"%(lang,server)
    return HttpResponse(message)









