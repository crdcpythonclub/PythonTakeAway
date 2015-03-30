#!/usr/bin/python

from PIL import Image
from PIL import ImageFilter
import urllib
import urllib2
import re
import json

import os 
import uuid

pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"
temp_dir_root = './temp'

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"

def get_temp_dir_for_image(dir_root):
    if not os.path.exists(dir_root):
        os.mkdir(dir_root)
    temp_dir = os.path.join(dir_root,str(uuid.uuid4()))
    os.mkdir(temp_dir)
    
    return temp_dir    

def get_image(url):
    resp = urllib.urlopen(url)
    raw = resp.read()
    with open('./tmp.jpg', 'wb') as fp:
        fp.write(raw)

    return Image.open('./tmp.jpg')

def pre_ocr_processing(im):
    im = im.convert("RGB")
    width, height = im.size

    white = im.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
    grey = im.convert('L')
    impix = im.load()
    whitepix = white.load()
    greypix = grey.load()

    for y in range(height):
        for x in range(width):
            greypix[x,y] = min(255, max(255 + impix[x,y][0] - whitepix[x,y][0],
                                        255 + impix[x,y][1] - whitepix[x,y][1],
                                        255 + impix[x,y][2] - whitepix[x,y][2]))

    new_im = grey.copy()
    binarize(new_im, 150)
    return new_im

def binarize(im, thresh=120):
    assert 0 < thresh < 255
    assert im.mode == 'L'
    w, h = im.size
    for y in xrange(0, h):
        for x in xrange(0, w):
            if im.getpixel((x,y)) < thresh:
                im.putpixel((x,y), 0)
            else:
                im.putpixel((x,y), 255)
                

def get_text_img(image):
    im = image.crop((125, 2, 260, 25))
    im = pre_ocr_processing(im)
    return im
    
def ocr_question_extract(im):
    # git@github.com:crdcpythonclub/pytesseract.git
    global pytesseract
    try:
        import pytesseract
    except:
        print "[ERROR] pytesseract not installed"
        return
    return pytesseract.image_to_string(im, lang='chi_sim').strip()


def get_sub_img(im, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    left = 5 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67

    return im.crop((left, top, right, bottom))


def baidu_stu_lookup(im):
    url = "http://stu.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="
    im.save("./query_temp_img.png")
    raw = open("./query_temp_img.png", 'rb').read()
    url = url + str(len(raw))
    req = urllib2.Request(url, raw, {'Content-Type':'image/png', 'User-Agent':UA})
    resp = urllib2.urlopen(req)

    resp_url = resp.read()      # return a pure url


    url = "http://stu.baidu.com/n/searchpc?queryImageUrl=" + urllib.quote(resp_url)

    req = urllib2.Request(url, headers={'User-Agent':UA})
    resp = urllib2.urlopen(req)

    html = resp.read()

    return baidu_stu_html_extract(html)


def baidu_stu_html_extract(html):
    #pattern = re.compile(r'<script type="text/javascript">(.*?)</script>', re.DOTALL | re.MULTILINE)
    pattern = re.compile(r"keywords:'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        return '[UNKOWN]'
    json_str = matches[0]

    json_str = json_str.replace('\\x22', '"').replace('\\\\', '\\')

    #print json_str

    result = [item['keyword'] for item in json.loads(json_str)]

    return '|'.join(result) if result else '[UNKOWN]'



import unittest

class test_image_process(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        global pic_url,temp_dir_root
        self.temp_dir = get_temp_dir_for_image(temp_dir_root)
        self.image = get_image(pic_url)
        self.image.show()
        self.image.save(os.path.join(self.temp_dir,'orig.jpg'))
        
    def test1(self):
        im = get_text_img(self.image)
        im.show()
        im.save(os.path.join(self.temp_dir,'txt.jpg'))
        print ocr_question_extract(im)
    
    def test2(self):
        for y in range(2):
            for x in range(4):
                im2 = get_sub_img(self.image, x, y)
                im2.show()
                im2.save(os.path.join(self.temp_dir,'sub_%s_%s.jpg'%(x,y)))
                result = baidu_stu_lookup(im2)
                print (y,x), result
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    