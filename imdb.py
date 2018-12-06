from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import csv
from halo import Halo
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import pandas as pd
from pandas import ExcelWriter

movie_title_list = ['Yomeddine','Shoplifters','Capernaum','Cold War','Dogman','Aga','El Angel','A Twelve-Year Night','In the Aisles','Tel Aviv on Fire',
'Birds of passage','The Third Wife','Pity','Volcano','Rona, Azim’s Mother', 'Tale of the Sea','A Family Tour','Donbass','Dovlatov','Foxtrot','Jumpman',
'One Step Behind the Seraphim','Rojo','Suleiman Mountain','The House that Jack Built','The Interpreter','The Man who bought the moon',
'The Sisters Brothers','The Reports on Sarah and Saleem','Woman at War','Yuli','The Heiresses','Our Time','Namme','Everybody Knows',
'MUHAMMAD: THE MESSENGER OF GOD','Border','The Ballad of Buster Scruggs']

# movie_title_list = ['Rona, Azim’s Mother']

pd_data = []
failed_movie_requests = []
multiple_search_result = []
base_url = 'https://www.imdb.com'
for movie_title in movie_title_list:
    # url = 'https://www.imdb.com/find?q={0}&s=tt&exact=true&ref_=fn_al_tt_ex'    
    encoded = urlencode(dict(q=movie_title,s='tt',exact='true',ref_='fn_al_tt_ex'))
    full_url =  f"https://www.imdb.com/find?{encoded}"
    # print(full_url)
    r  = requests.get(full_url)
    data = r.text
    search_list_soup = BeautifulSoup(data,"html.parser")
    tables = search_list_soup.findChildren('table')
    search_list_table = tables[0]    
    rows = search_list_table.findChildren('tr')
    
    if len(rows) > 0:
        row_tr_a = search_list_soup.tr.a
        if row_tr_a:
            movie_url = row_tr_a.get('href')            
            movie_fullurl = base_url + movie_url        
            movie_text = requests.get(movie_fullurl).text
            movie_soup = BeautifulSoup(movie_text,"html.parser")
            rating_div = movie_soup.find('div', class_='ratingValue')
        
            if rating_div:
                rating = rating_div.span.text            
            else:
                rating = '0'
            # print(movie_title + ' - ', rating)
        
            if len(rows) > 1:
                mul_search_req = (full_url,movie_title)
                multiple_search_result.append(mul_search_req) 
            movie_data = [movie_title, rating,movie_fullurl]    
            pd_data.append(movie_data)
    else:    
        # print('search result count for ' + movie_title + ' = '  + str(len(rows)))
        failed_req =(full_url,movie_title)
        failed_movie_requests.append(failed_req)

# print('Movies failed to get rating ---------------------')            
# print(failed_movie_requests)    

# print('Multiple search result ---------------------')            
# print(multiple_search_result)    

df = pd.DataFrame(pd_data,columns=['Title','Rating', 'Url'])
sorted_df = df.sort_values(by='Rating',ascending=[False])
print(sorted_df)

writer = ExcelWriter('Imdb.xlsx')
sorted_df.to_excel(writer,'Sheet5')
writer.save()

