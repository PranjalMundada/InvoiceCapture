# -*- coding: utf-8 -*-

import easyocr


class OCR:
    
    def recognize(self, IMAGE_PATH):
        
       # IMAGE_PATH = 'attachments/invoice.png'
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH, detail=0, )
        #paragraph="False"
        return result
    
