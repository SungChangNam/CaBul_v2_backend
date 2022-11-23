from articles.models import Feed
import torch
import cv2
import uuid
from PIL import Image
import numpy as np

def upload_category(img, serializer):    # 게시글 업로드 시 자동 카테고리 분류
    feed = Feed.objects.get(id=serializer['id'])
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        imgs = [(f'.{img}')] # batch of images
        results = model(imgs)
        category_name = results.pandas().xyxy[0]['name'][0]
        feed.category = category_name
        feed.save()
    except(IndexError):
        category_name = '카테고리 없음'
        feed.category = category_name
        feed.save()



def transform(img, net, serializer): # 사진 업로드 시 유화 스타일로 변경
    feed = Feed.objects.get(id=serializer['id'])
    now = uuid.uuid4()
    
    data = cv2.imread((f'.{img}'))
    
    #인코딩
    encoded_img = np.fromstring(data, dtype = np.uint8)
    
    #다시 디코딩
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    
    h, w, c = data.shape
    #500x500으로 크기조정
    img = cv2.resize(data, dsize=(500, int(h / w * 500)))
    #모델: 명화로 바꾸는 부분
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
    
    #어떤 명화로 바꿀지
    net.setInput(blob)
    output = net.forward()
    #아웃풋 크기 조정
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE
    #크기에 맞게 자르고 type을 바꿔줌
    output = np.clip(output, 0, 255)
    output = output.astype('uint8')
    output = Image.fromarray(output)

    transfer_image = f"transfer_feed_images/{feed.user.nickname}_{now}.jpg"
    output.save(f"./media/{transfer_image}", "JPEG")
    feed.transfer_image = transfer_image
    feed.save()