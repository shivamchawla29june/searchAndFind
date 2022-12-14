from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRIAGLIST_URL='https://atlanta.craigslist.org/search/cto?query={}'
#BASE_CRIAGLIST_URL='https://losangeles.craigslist.org/d/housing/search/sss?query={}'
#BASE_CRIAGLIST_URL='https://losangeles.craigslist.org/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request) :
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    
    final_url= BASE_CRIAGLIST_URL.format(quote_plus(search))
    #print(final_url)
    response = requests.get(final_url)
    data=response.text
    soup = BeautifulSoup(data, features= 'html.parser')
    post_title = soup.find_all('a', {'class': 'result-title'})
    #print(post_title[0])
    #print(data)
    
    post_listings = soup.find_all('li', {'class': 'result-row'})
    
    final_posting=[]
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if(post.find(class_='result-price')):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        
        if(post.find(class_ = 'result-image').get('data-ids')):
            post_image_id = post.find(class_ = 'result-image').get('data-ids').split(',')[0].split(':')[-1]
            post_image_url= BASE_IMAGE_URL.format(post_image_id)
            #print(post_image_url)
        else:
            post_image_url= 'https://craigslist.org/images/peace.jpg'
            



        final_posting.append((post_title,post_url,post_price,post_image_url))
        
    stuff_for_frontend ={
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'my_app/new_search.html',stuff_for_frontend)