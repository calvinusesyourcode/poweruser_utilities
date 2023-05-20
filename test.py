import inspect
from requests_html import HTMLSession

#define our URL
url = 'https://www.youtube.com/@hubermanlab/videos'

#use the session to get the data
s = HTMLSession().get(url)

#Render the page, up the number on scrolldown to page down multiple times on a page
s.html.render(sleep=1, keep_page=True, scrolldown=2)

#take the rendered html and find the element that we are interested in
results = s.html.find('.cl-search-result')[:1]

bad_categories = [
    "clo", #clothing
    "ctd", #cars and trucks
]

#loop through those elements extracting the text and link
for result in results:
    title = result.find('.titlestring',first=True).text
    link = result.absolute_links.pop()
    price = result.find('.priceinfo',first=True).full_text
    #pp.pprint(title, price, link, sep=" | ")
    print(inspect.getmembers(result))
    print(price,title, link)
    #video = {
    #    'title': item.text,
    #    'link': item.absolute_links
    #}
    #print(video)
    