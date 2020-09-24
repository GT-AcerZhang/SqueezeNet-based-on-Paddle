import paddle
import paddle.fluid as fluid
import numpy as np
import os
import random
import shutil
from PIL import Image
import matplotlib.pyplot as plt

DATADIR = '/home/aistudio/work/ѵ����'

def Img_predeal(img):# ͼƬԤ����
    im = np.array(img).astype(np.float32)
    # ����ת��
    im = im.transpose((2, 0, 1))      #0��1��2 ��ͨ����˵�ĵ�һά���ڶ�ά������ά�������CSDN
    im = im / 255.0
    #im = np.expand_dims(im, axis=0)  #�ڵ�axisά�������,Ԥ��ʱ�����˾���루��֤Ԥ������ݺ�ѵ��������ά����ͬ����ѵ��ʱ���ܼӴ˾�
    return im

def data_loader(datadir, batch_size=10, mode = 'train'):
    filenames = []
    # ��datadirĿ¼�µ��ļ��г�����ÿ���ļ���Ҫ���룬�޳�.xml�ļ�������ȡ.jpg�ļ�
    old_filenames = os.listdir(datadir)
    for of in old_filenames:# �޳�.xml�ļ�������ȡ.jpg�ļ�
        if of[-3:] == 'jpg':
            filenames.append(of)
        else:
            continue# �����.xml�ļ�������
    def reader():
        if mode == 'train':
            # ѵ��ʱ�����������˳��
            random.shuffle(filenames)
        batch_imgs = []
        batch_labels = []
        for name in filenames:
            filepath = os.path.join(datadir, name)
            img = Image.open(filepath)   #424x240����
            img = img.resize((224, 224)) #ѹ��Ϊ224x224����
            im = Img_predeal(img)
            if name[:3] == 'red':
                label = 1
            else:
                label = 0
            # ÿ��ȡһ�����������ݣ��ͽ�����������б���
            batch_imgs.append(im)
            batch_labels.append(label)
            if len(batch_imgs) == batch_size:
                # �������б�ĳ��ȵ���batch_size��ʱ��
                # ����Щ���ݵ���һ��mini-batch������Ϊ������������һ�����
                imgs_array = np.array(batch_imgs).astype('float32').reshape(-1, 3, 224, 224)
                labels_array = np.array(batch_labels).astype('int64').reshape(-1, 1)
                yield imgs_array, labels_array
                batch_imgs = []
                batch_labels = []

        if len(batch_imgs) > 0:
            # ʣ��������Ŀ����һ��batch_size�����ݣ�һ������һ��mini-batch
            imgs_array = np.array(batch_imgs).astype('float32').reshape(-1, 3, 224, 224)
            labels_array = np.array(batch_labels).astype('int64').reshape(-1, 1)
            yield imgs_array, labels_array

    return reader

def draw_train_process(title,iters,costs,accs,label_cost,lable_acc):
    plt.title(title, fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel("cost/acc", fontsize=20)
    plt.plot(iters, costs,color='red',label=label_cost) 
    plt.plot(iters, accs,color='green',label=lable_acc) 
    plt.legend()
    plt.grid()
    plt.show()