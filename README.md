# FaceRecognition
注意：一定要修改好自己本地存储路径以及创建对应的文件夹！！！  

录入人脸数据文件：  SaveFaceData.py  （一共录入脸部图片二十张）  

构建数据集后处理数据集：   CalculateCharacter.py  

采集对应20张图片的68个特征点数组，以 face_features.txt (i为01到20的数字）文件保存到同一目录下。  

通过20个特征，计算出平均（mean）特征数组 face_feature_mean.csv。  

人脸识别： main.py  

利用dlib和opencv编程，打开摄像头，对捕获到的人脸进行特征提取，与平均特征进行误差计算（欧几里得距离），当误差小于一定阈值时，判断为同一个人，否则判断为 unknown。  

