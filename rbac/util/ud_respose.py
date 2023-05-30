from django.template import loader
from django.http import HttpResponse
import time
from django.template import loader
from threading import Thread


# from django.shortcuts import render


# use custom response class to override HttpResponse.close()
class LogSuccessResponse(HttpResponse):

    def close(self):
        super(LogSuccessResponse, self).close()
        # do whatever you want, this is the last codepoint in request handling
        if self.status_code == 200:
            print('HttpResponse successful: %s' % self.status_code)
        time.sleep(5)
        print('5s last.')
        print('aa')


# this would be the view definition
def logging_view(request):
    response = LogSuccessResponse('Hello World', mimetype='text/plain')
    return response


class HttpResponseThen(HttpResponse):
    def __init__(self, data, *args, callargs=(), callkwargs={}, then_callback=None, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.then_callback = then_callback
        self.callargs = callargs
        self.callkwargs = callkwargs

    def close(self):
        super().close()
        t1 = Thread(target=self.then_callback, args=self.callargs, kwargs=self.callkwargs)
        t1.start()

        # self.then_callback()


def render(
        request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)


def renderThen(
        request, template_name, context=None, content_type=None, status=None, using=None, callback=None,
        callargs=(), callkwargs={}
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponseThen(content, content_type, status, callargs=callargs, callkwargs=callkwargs,
                            then_callback=callback)
    # return HttpResponse(content, content_type, status)
