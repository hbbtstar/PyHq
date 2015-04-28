from django.shortcuts import render
from yaml import load, dump


def main(request, blueprint="blank", job="blank"):

    return render(request, 'industry.html')
