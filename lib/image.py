
from config.config import face_api_key, face_api_url
import requests

from .face import *

#Represents an image
class image:
    def __init__(self,image_url):
        self.url = image_url
    
    #Calls Azure Face API to extract face data from image.
    def get_image_faces(self):
        headers = {
            'Content-Type'                  :   'application/json',
            'Ocp-Apim-Subscription-Key'     :   face_api_key,
        }
        params = {
            'returnFaceId'                  :   'true',
            'returnFaceLandmarks'           :   'false',
            'returnFaceAttributes'          :   'age,gender,smile,emotion',
            'recognitionModel'              :   'recognition_01',
            'returnRecognitionModel'        :   'false',
            'detectionModel'                :   'detection_01'
        }
        body = {
            "url": self.url
        }
        self.response = requests.post(face_api_url, headers=headers, params=params, json=body)
        self.face_json = self.response.json()
        
        self.faces = []   
        if self.response.status_code == 200:
            for f in self.face_json:
                self.faces += [face(f)]
        return self.faces