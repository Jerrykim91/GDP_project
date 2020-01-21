from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# DB
from django.db import connection
from django.db.models import Sum,Min,Max,Count,Avg
# 크롤링
from bs4 import BeautifulSoup
from selenium import webdriver
# 그래프
from matplotlib import font_manager, rc 
import matplotlib.pyplot as plt 
import pandas as pd
# 모델 호출 
from .models import GDPTable
#
import urllib.request
import json
import io
# byte배열로 이미지를 변환
import base64

# 변수 
cursor = connection.cursor()

# Create your views here.




# plot_font - 그래프 폰트함수
def plot_font():
    pass


@csrf_exempt
# search_detail - 
def search_detail(request) :
    pass

@csrf_exempt
# search_show - 검색 결과 출력 창 
def search_show(request) :
    pass

@csrf_exempt
# sort_by_year  
def sort_by_year(request) :
    pass

# search_country - 나라 검색 
def search_country(request):
    pass


# search_country_graph - 나라 클릭하면 연도 그래프
def search_country_graph(request):
    pass