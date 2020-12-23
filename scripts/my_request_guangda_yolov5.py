
import os,sys
import json
import base64
import codecs
# import chardet
import requests

def main(imgpath,frame_id):
    #img = cv2.imread(imgpath)
    #img_list = img.tolist()
    #print (img_list)
    #with open(imgpath,'rb') as f:
    image_data = open(imgpath,'rb').read()
    f_str=base64.b64encode(image_data)
    #print (type(f_str))
    #print (chardet.detect(image_data))
    # data = {'imgpath' : image_data.decode('ascii', errors='ignore') ,'frame_id' : int(frame_id)}
    data = {'img' : None ,'frame_idx' : int(frame_id)}
    print (type(data))
    data['img'] =f_str 
    #f.close()
    json_str = json.dumps(data)
    #print (type(json_str))
    #json_data = json.loads(json_str)
    #comd = 'curl -i -X POST -H \'Content-type\':\'application/json\' http://k8s-deploy-yfhg5b-1605680519300-58fd9d75d7-qgmwk:8045/v0/model/pytorch/predict -d '
    #comd += '\''
    #comd += json_str 
    #comd += '\''
    ##print (comd)
    #os.system(comd)
     
    url = "http://10.187.7.53:8080/v0/model/pytorch/predict"
    #url = "http://10.186.1.125:8045/v0/model/pytorch/predict"
    headers = {"Content-Type":"application/json"}
    res = requests.post(url=url,headers=headers,
        data=json_str,timeout=(3.05,15))
    print(res.text)



if __name__ == "__main__":
    imgpath = '/nfs/volume-95-7/temporal-shift-module/Yolov5_DeepSort_Pytorch/inference/kebo_test/20201127104912_781877826285486080_242_316009_/003.jpg'
    frame_id = 3
    main(imgpath,frame_id)
