from functools import wraps
from datetime import datetime
import traceback
import os
from threading import Thread
import django

from functools import wraps
from inspect import getattr_static

from math import ceil, floor


# from django.utils.html import format_html


def set_func_attr(attrs):
    # @wraps(f)
    def wrapper(f):
        for k, v in attrs.items():
            if hasattr(f, k):
                print(f"{f.__name__} already have attr:{k}")
                continue
            setattr(f, k, v)
        return f

    return wrapper


# @set_func_attr({"short_description": format_html('<a href="#">操作</a>')})
@set_func_attr({"short_description": '<a href="#">操作</a>'})
def test():
    print('aa')


def cls_method_register(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        if getattr_static(cls, func.__name__, None):
            msg = 'Error method name REPEAT, {} has exist'.format(func.__name__)
            raise NameError(msg)
        else:
            setattr(cls, func.__name__, wrapper)
        return func

    return decorator


def init_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmy.settings")  # project_name 项目名称
    django.setup()


def udprint(str_, align="left", width=100, fill_char='_'):
    str_list = str_.split("\n")
    for row in str_list:
        num = len(row)
        for i in range(int(num / width) + 1):
            _tmp = row[i * width: (i + 1) * width]
            cnt = len(_tmp)
            if len(_tmp) <= width:
                if align == "left":
                    print(_tmp + fill_char * (width - cnt))
                elif align == 'right':
                    print(fill_char * (width - cnt) + _tmp)
                elif align == 'center':
                    print(fill_char * (floor((width - cnt) / 2)) + _tmp +
                          fill_char * (ceil((width - cnt) / 2)))
                else:
                    raise Exception(f"align:{align} not config")


# 装饰器，计时函数执行时间。
def timer(func):
    """
    decorator for get the execute_time of a func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        time_a = datetime.now()
        result = func(*args, **kwargs)
        time_b = datetime.now()
        print('start time:' + time_a.strftime('%Y-%m-%d %H:%M:%S.%f'))
        print('end   time:' + time_b.strftime('%Y-%m-%d %H:%M:%S.%f'))
        info = ''
        if args:
            info = info + str(args)
        if kwargs:
            info = info + str(kwargs)
        if info:
            if len(info) < 100:
                # print(f'Execute time:{(time_b - time_a).total_seconds():0.4f}s.func[{func.__name__}({info})]')
                print(f'Execute time:{(time_b - time_a).total_seconds()}s.func[{func.__name__}({info})]')
            else:
                print(f'Execute time:{(time_b - time_a).total_seconds()}s.func[{func.__name__}({info[0:100]})]')
        else:
            print(f'Execute time:{(time_b - time_a).total_seconds()}s.func[{func.__name__}()]')
        return result

    return wrapper


def list_partition(a: list, num: int):
    re = []
    for i in range(ceil(len(a) / num)):
        re.append(a[i * num:(i + 1) * num])
        # print(a[i * num:(i + 1) * num])
    return re


# from django.utils.functional import curry
def curry(_curried_func, *args, **kwargs):
    @wraps(_curried_func)
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*args, *moreargs, **{**kwargs, **morekwargs})

    return _curried


# 线程池包裹函数。
def thread_pool_func(func):
    """
    decorator for get the execute_result of a func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return {'status': 1, 'result': func(*args, **kwargs)}
        except Exception as e:
            return {'status': 0, 'result': "error:{}\n{}".format(str(e), traceback.format_exc())}

    return wrapper


def api_url(base, url):
    print("add prefix {}".format(base))
    return "{}{}".format(base, url)


def response_then(callback_func, *args, **kwargs):
    def after_response(func):
        @wraps(func)
        def wrapper(*inargs, **inkwargs):
            result = func(*inargs, **inkwargs)
            t1 = Thread(target=callback_func, args=args, kwargs=kwargs)
            t1.start()
            # callback_func(*args,**kwargs)
            return result

        return wrapper

    return after_response

# def test():
#     print("tools_ud test.")
