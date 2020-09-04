import time
import pandas as pd
from selenium import webdriver
driver = webdriver.Chrome()

from lib.image_scraper import *
from lib.image import *


urls = pd.read_csv('config/websites.csv')['url'].tolist()


def load_parquet_or_init(file_name,columns=[]):
    try:
        return pd.read_parquet("data/{file_name}.parquet".format(file_name=file_name))
    except:
        return pd.DataFrame({},columns=columns)

df_scan = load_parquet_or_init('scans')
df_img = load_parquet_or_init('images',columns=['image_url','scanned'])
df_appearance = load_parquet_or_init('appearances')
df_faces = load_parquet_or_init('faces')

for url in urls:
    img_list = image_scraper(url,driver).image_list()
    timestamp = pd.Timestamp.now().round('s')
    df_scan = df_scan.append({'url':url,'datetime':timestamp},ignore_index=True)
    df_new_images = pd.DataFrame({'image_url':img_list['url'],'scanned':False})
    df_img = df_img.append(df_new_images.loc[~(df_new_images.image_url.isin(df_img.image_url))],ignore_index=True)
    df_appearance = df_appearance.append(pd.DataFrame({'url':url,'datetime':timestamp,'image_url': img_list['url'],'x':img_list['x'],'y':img_list['y'],'height':img_list['height'],'width':img_list['width']}),ignore_index=True)


def scan_for_faces(img):
    print("Scanning " + img + " for faces.") 
    global df_faces
    try:
        time.sleep(3)
        this_image = image(img)
        faces = this_image.get_image_faces()
        print("Number of faces: " + str(len(faces)))
        df_faces = df_faces.append(pd.DataFrame({
            'img':img,
            'left':[f.left for f in faces],
            'top':[f.top for f in faces],
            'width':[f.width for f in faces],
            'height':[f.height for f in faces],
            'age':[f.age for f in faces],
            'gender':[f.gender for f in faces],
            'smile':[f.smile for f in faces],
            'emotion':[f.emotion for f in faces]            
        }))
        return True
    except:
        return False

df_img.loc[df_img.scanned == False,'scanned'] = df_img.loc[df_img.scanned == False,'image_url'].map(scan_for_faces)

df_scan.to_parquet('data/scans.parquet')
df_img.to_parquet('data/images.parquet')
df_appearance.to_parquet('data/appearances.parquet')
df_faces.to_parquet('data/faces.parquet')