from bs4 import BeautifulSoup

html_doc = """ <html>
<head><title>Birbs are pretty</title></head>
<body><p class="birb-food"><b>Birbs and their foods</b></p>
<p class="food">Birbs love:<a class="seed" href="http://seeds" id="seed">seed</a>
   and
   <a class="fruit" href="http://fruit" id="fruit">fruit</a></p>
 </body></html>
  """
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())

