# 从人脸图像文件中提取人脸特征存入 CSV
# Features extraction from images and save into features_all.csv
# return_128d_features()          获取某张图像的128D特征
# compute_the_mean()              计算128D特征均值
from cv2 import cv2 as cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
# 要读取人脸图像文件的路径
path_images_from_camera = "E:/PictureTest/PeopleFaceData/person/"
# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()
# Dlib 人脸预测器
predictor = dlib.shape_predictor("E:/PycharmProjects/FaceRecognition/libfile/shape_predictor_68_face_landmarks.dat")
# Dlib 人脸识别模型
face_rec = dlib.face_recognition_model_v1("E:/PycharmProjects/FaceRecognition/libfile/dlib_face_recognition_resnet_model_v1.dat")
# 返回单张图像的 128D 特征
def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)
    print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')
    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")
    return face_descriptor
# 将文件夹中照片特征提取出来, 写入 CSV
def return_features_mean_personX(path_faces_personX):
    features_list_personX = []
    photos_list = os.listdir(path_faces_personX)
    if photos_list:
        for i in range(len(photos_list)):
            # 调用return_128d_features()得到128d特征
            print("%-40s %-20s" % ("正在读的人脸图像 / image to read:", path_faces_personX + "/" + photos_list[i]))
            features_128d = return_128d_features(path_faces_personX + "/" + photos_list[i])
            #  print(features_128d)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
                i1=str(i+1)
                add="E:/PictureTest/PeopleFaceData/PersonCsv/"+"face_features"+i1+".csv"
                print(add)
                with open(add, "w", newline="") as csvfile:
                    writer1 = csv.writer(csvfile)
                    writer1.writerow(features_128d)
    else:
        print("文件夹内图像文件为空 / Warning: No images in " + path_faces_personX + '/', '\n')
    # 计算 128D 特征的均值
    # N x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
    else:
        features_mean_personX = '0'
    return features_mean_personX
# 读取某人所有的人脸图像的数据
people = os.listdir(path_images_from_camera)
people.sort()

with open("E:/PictureTest/PeopleFaceData/PersonCsv/face_feature_mean.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for person in people:
        print("##### " + person + " #####")
        # Get the mean/average features of face/personX, it will be a list with a length of 128D
        features_mean_personX = return_features_mean_personX(path_images_from_camera + person)
        writer.writerow(features_mean_personX)
        print("特征均值:\n", list(features_mean_personX))
        print('\n')
    print("所有录入人脸数据存入 E:/PictureTest/PeopleFaceData/PersonCsv/face_feature_mean.csv")

