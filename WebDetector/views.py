import os
from django.shortcuts import render
from django.http import HttpResponse
from . import img_path_reader as reader
import json


def img_all(request):
    """
    get all detected faces
    :param request: http request
    :return:img all url formatted with JSon
    """
    print(os.path.abspath('.'))
    result_list = reader.get_all()
    print(result_list)
    return HttpResponse(json.dumps(result_list))


def index(request):
    """
    setting default page
    :param request:
    :return: render of default page
    """
    return render(request, "index.html")


def img_one_day(request, date):
    """
    get one-day detected faces
    :param request:http request
    :param date: the day client chose
    :return:url list of one-day detected faces, formatted with JSon
    """
    result_list = reader.get_one_day_img(date)
    return HttpResponse(json.dumps(result_list))
