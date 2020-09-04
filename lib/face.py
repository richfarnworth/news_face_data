
class face:
    def __init__(self,json):
        self.json = json
        self.left = json['faceRectangle']['left']
        self.top = json['faceRectangle']['top']
        self.width = json['faceRectangle']['width']
        self.height = json['faceRectangle']['height']
        self.age = json['faceAttributes']['age']
        self.gender = json['faceAttributes']['gender']
        self.smile = json['faceAttributes']['smile']
        self.emotion_all = json['faceAttributes']['emotion']
        self.resolve_emotion()
    def resolve_emotion(self):
        max_value = ''
        max_score = 0
        for k,v in self.emotion_all.items():
            if v > max_score:
                max_value = k
                max_score = v
        self.emotion = max_value