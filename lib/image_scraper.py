from urllib.parse import urlparse

#Extracts a list of images from a webpage
class image_scraper:
    def __init__(self,page_url,driver):
        self.page_url = page_url
        self.driver = driver
    def image_list(self):
        print("Collecting images for " + self.page_url)
        self.driver.get(self.page_url)
        elements = self.driver.find_elements_by_xpath("//img")
        img_list = {'url':[],'x':[],'y':[],'height':[],'width':[]}        
        for i in elements:
            img_list['x'] += [i.location['x']]
            img_list['y'] += [i.location['y']]
            try:
                img_list['height'] += [i.size['height']]
                img_list['width'] += [i.size['width']]
            except:
                img_list['height'] += [None]
                img_list['width'] += [None]
            src = i.get_attribute('src')
            if src != '' and src[:4] != 'data':
                img_list['url'] += [src]
            else:
                src = i.get_attribute('data-src').replace('{width}','820')
                if src[:4].lower() != 'http':
                    parsed_uri = urlparse(self.page_url)
                    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)[:-1]
                    src = (result + src)
                img_list['url'] += [src]
        return img_list