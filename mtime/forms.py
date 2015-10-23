
# -*- coding: utf-8 -*-
from django import forms
from .models import Post,HostList

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)





########### FORM  1  ################

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=10,label='主题')#设置最大长度为10 label 可读
    email = forms.EmailField(required=False,label='Email')#非必要字段
    message = forms.CharField(widget=forms.Textarea,label='信息')#指定form中组件的类型

    #自定义校验规则，该方法在校验时被系统自动调用，次序在“字段约束”之后
    def clean_message(self):
        message = self.cleaned_data['message']#能到此处说明数据符合“字段约束”要求
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("单词个数低于4个!")
        return message

#自定义效验规则,无需其它地方指定,知道views 或者  html {{ form.subject.errors }}
    # def clean_subject(self):
    # 	subject = self.cleaned_data['subject']
    # 	if len(subject) == 5:
    # 		raise forms.ValidationError("单词等于5个!")
    #     return subject
#



################ Form ################

class HostsListForm(forms.ModelForm):
    class Meta:
        model = HostList
        fields = ['ip','hostname','product','application','idc_jg','status','remark']
        # widgets = {
        #   'ip': forms.TextInput(attrs={'class': 'form-control'}),
        #   'hostname': forms.TextInput(attrs={'class': 'form-control'}),
        #   'product': forms.TextInput(attrs={'class': 'form-control'}),
        #   'application': forms.TextInput(attrs={'class': 'form-control'}),
        #   'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
        #   'status': forms.TextInput(attrs={'class': 'form-control'}),
        #   'remark': forms.TextInput(attrs={'class': 'form-control'}),
        # }











