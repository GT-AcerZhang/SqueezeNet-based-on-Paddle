# ��ѵ�����ϲ��Խ��
import paddle
import paddle.fluid as fluid
import numpy as np
import os
import random
import shutil
from PIL import Image

def Img_val_predeal(img):# ͼƬԤ�⴦��
    im = np.array(img).astype(np.float32)
    # ����ת��
    im = im.transpose((2, 0, 1))     
    im = im / 255.0
    im = np.expand_dims(im, axis=0)  
    return im

error = 0 #ʶ����������
class_dict ={'gre':'�̵�','red':'���'}
label_list = ['gre','red']
place = fluid.CPUPlace()
infer_exe = fluid.Executor(place)
inference_scope = fluid.core.Scope()
f=open('result.txt','w')
with fluid.scope_guard(inference_scope):
    # ��ָ��Ŀ¼�м��� ����model(inference model)
    [inference_program,  # Ԥ���õ�program
     feed_target_names,  
     fetch_targets] = fluid.io.load_inference_model("Red_Green.inference.model",infer_exe)  


    testfile = os.listdir('/home/aistudio/work/���Լ�')
    for path in testfile:
        ipath = os.path.join('/home/aistudio/work/���Լ�',path)
        img = Image.open(ipath)
        img = img.resize((224, 224))  #ѹ��Ϊ224x224����
        im = Img_val_predeal(img)
        results = infer_exe.run(inference_program,  # ����Ԥ�����
                                feed={feed_target_names[0]: im},  # ι��ҪԤ���img
                                fetch_list=fetch_targets)  # �õ��Ʋ���
        #print('results', results)
        index = np.argmax(results[0])
        mat = "{:^15}\t{:^4}\t{:^10}\t{:^4}\t{:^10}\n"
        #print(mat.format(path,class_dict[path[:3]],"Ԥ����:  %s" % class_dict[label_list[index]],'�÷֣�',results[0][0][index]))
        f.write(mat.format(path,class_dict[path[:3]],"Ԥ����:  %s" % class_dict[label_list[index]],'�÷֣�',results[0][0][index]))
        if path[:3] != label_list[np.argmax(results[0])]:
            error += 1
    f.close()
    print('�ڲ��Լ���Ԥ���׼ȷ��Ϊ:',(400-error)/400.)