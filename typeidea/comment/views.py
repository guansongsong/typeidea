from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from .forms import CommentForm
# Create your views here.


class CommentView(TemplateView):
    http_method_names = ['post', ]    # 只写了post请求，那么就只接受post请求，不会接受其他请求
    template_name = 'comment/result.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse(123)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            # return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context)
