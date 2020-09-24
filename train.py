all_train_iter=0
all_train_iters=[]
all_train_costs=[]
all_train_accs=[]

train_reader = data_loader(DATADIR,10,'train')

data_shape = [3, 224, 224]
images = fluid.layers.data(name='images', shape=data_shape, dtype='float32')
label = fluid.layers.data(name='label', shape=[1], dtype='int64')

#��SqueezeNet������з��࣬�����Ϊ2
net = SqueezeNet(images,2)
predict =  net.prediction

# ��ȡ��ʧ������׼ȷ��
cost = fluid.layers.cross_entropy(input=predict, label=label) # ������
avg_cost = fluid.layers.mean(cost)                            # ����cost������Ԫ�ص�ƽ��ֵ
acc = fluid.layers.accuracy(input=predict, label=label)       #ʹ������ͱ�ǩ����׼ȷ��

test_program = fluid.default_main_program().clone(for_test=True)

# �����Ż�����
optimizer =fluid.optimizer.Adam(learning_rate=0.0001)
optimizer.minimize(avg_cost)
print("���")
place = fluid.CPUPlace()

# ����ִ��������ʼ������

exe = fluid.Executor(place)
exe.run(fluid.default_startup_program())

EPOCH_NUM = 5 #ѵ��5��
model_save_dir = "/home/aistudio/Red_Green.inference.model"

for pass_id in range(EPOCH_NUM):
    # ��ʼѵ��
    for batch_id, data in enumerate(train_reader()):  # ����train_reader�ĵ���������Ϊ���ݼ�������batch_id
        train_cost, train_acc = exe.run(program=fluid.default_main_program(),  # ����������
                                        feed={'images':data[0], 'label':data[1]},  # ι��һ��batch������
                                        fetch_list=[avg_cost, acc])  # fetch��������׼ȷ��

        # ÿ5��batch��ӡһ��ѵ�����
        if batch_id % 5 == 0:
            print('Pass:%d, Batch:%d, Cost:%0.5f, Accuracy:%0.5f' %
                  (pass_id, batch_id, train_cost[0], train_acc[0]))

    all_train_iter=all_train_iter+10
    all_train_iters.append(all_train_iter)
    all_train_costs.append(train_cost[0])
    all_train_accs.append(train_acc[0])

# ����ģ��
# �������·�������ھʹ���
if not os.path.exists(model_save_dir):
    os.makedirs(model_save_dir)
print('save models to %s' % (model_save_dir))
fluid.io.save_inference_model(model_save_dir,
                              ['images'],
                              [predict],
                              exe)
print('ѵ��ģ�ͱ�����ɣ�')
draw_train_process("training",all_train_iters,all_train_costs,all_train_accs,"trainning cost","trainning acc")