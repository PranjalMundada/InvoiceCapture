# -*- coding: utf-8 -*-
from html2image import Html2Image
#import aspose.words as aw
#import requests
# https://blog.aspose.com/words/convert-html-to-image-in-python/
    
#res = requests.get("https://google.com", headers={'Accept': 'image/png'})

#print(res.status_code)
#print(res.headers)

class MyHTMLToImage:
    
    def url2Image( self, url, image_filename):
        hti = Html2Image()
        hti.screenshot(url='https://www.python.org', save_as='python_org.png')

