import inspect
from requests_html import HTMLSession


#define our URL
url = 'https://abbotsford.craigslist.org/search/sss?query=vr%20quest%202#search=1~gallery~0~82'

#use the session to get the data
s = HTMLSession().get(url)

#Render the page, up the number on scrolldown to page down multiple times on a page
s.html.render(sleep=1, keep_page=True, scrolldown=2)

#take the rendered html and find the element that we are interested in
results_array = s.html.find('.cl-search-result')
results = results_array.copy()

bad_categories = [
    "clo", #clothing
    "ctd", #cars and trucks
    "cto",
    "wtd", #auto wheels & tires
]

good_categories = [
    "tag", #toys and games
    "ele", #electronics
    "vgm", #video gaming
    

]
bad_cities = [
    "seattle",
]

#loop through those elements extracting the text and link
for result in results[:1]:
    try: 
        link = result.absolute_links.pop()
        if link.split("//")[1].split(".")[0] not in bad_cities and not set(link.split("//")[1].split("/")[1:3]).isdisjoint(good_categories):
            title = result.find('.titlestring',first=True).text
            price = result.find('.priceinfo',first=True).full_text
            print("\n","---------------------------------------------","\n","---------------------------------------------","\n")
            print(price,title,link)
            url = link

            #use the session to get the data
            s = HTMLSession().get(url)

            #Render the page, up the number on scrolldown to page down multiple times on a page
            s.html.render(sleep=1, keep_page=True, scrolldown=2)

            #take the rendered html and find the element that we are interested in
            results_array = s.html.find(".page-container",first=True).find('.body',first=True).find('.dateReplyBar',first=True).find('.actions-combo')
            results = results_array.copy()
            print(results)
            for result in results:
                for each in inspect.getmembers(result):
                    print("\n",each)
    except:
        pass
    #video = {
    #    'title': item.text,
    #    'link': item.absolute_links
    #}
    #print(video)
    