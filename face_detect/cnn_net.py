import tensorflow as tf
from sklearn.model_selection import train_test_split
import random
import numpy as np
from getimgdata import GetImgData

path = "./small_img_gray"  # 灰度图路径
imgs, labels, number_name = GetImgData(dir=path).readimg()
train_x, test_x, train_y, test_y = train_test_split(imgs, labels, test_size=0.2, random_state=10)


class CnnNet:
    def __init__(self, imgs=train_x, labels=train_y, keep_prob_5=0.5, keep_prob_75=0.75,
                 modelfile='./temp/train-model'):
        tf.reset_default_graph()  # 将计算图清零，以免出现代码多次运行时tensor叠加
        self.imgs = imgs  # 训练集自变量
        self.labels = labels  # 训练集目标变量
        self.size = imgs.shape[1]  # 图片宽度
        self.outnode = labels.shape[1]  # 输出层神经元个数
        self.x = tf.placeholder(tf.float32, [None, self.size, self.size, 1],
                                name='x_data')  # 注意给Tensor起的名字"x_data"，后续找x就靠它了
        self.y_ = tf.placeholder(tf.float32, [None, self.outnode], name='y_data')
        self.modelfile = modelfile
        self.keep_prob_5 = np.float32(keep_prob_5)
        self.keep_prob_75 = np.float32(keep_prob_75)

    def weightVariable(self, shape):  # 权值数组W
        init = tf.random_normal(shape, stddev=0.01)
        return tf.Variable(init)

    def biasVariable(self, shape):  # 偏置项数组b
        init = tf.random_normal(shape)
        return tf.Variable(init)

    def conv2d(self, x, W):  # 卷积
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def maxPool(self, x):  # max池化
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def dropout(self, x, keep):  # 随机让某些权重不更新，保持某个数
        return tf.nn.dropout(x, keep)

    def cnnLayer(self):
        """
        cnn神经网络结构
        :return:
        """
        # ===第一次卷积====
        W1 = self.weightVariable([3, 3, 1, 32])  # 卷积核/filter大小(3,3,1)， 输入通道(1)，输出通道(32)
        b1 = self.biasVariable([32])  # 偏置项
        conv1 = tf.nn.relu(self.conv2d(self.x, W1) + b1)  # 卷积
        pool1 = self.maxPool(conv1)  # 池化
        drop1 = self.dropout(pool1, self.keep_prob_5)  # 减少过拟合，随机让某些权重不更新

        # ===第二次卷积====
        W2 = self.weightVariable([3, 3, 32, 64])
        b2 = self.biasVariable([64])
        conv2 = tf.nn.relu(self.conv2d(drop1, W2) + b2)
        pool2 = self.maxPool(conv2)
        drop2 = self.dropout(pool2, self.keep_prob_5)

        # ===第三次卷积====
        W3 = self.weightVariable([3, 3, 64, 64])
        b3 = self.biasVariable([64])
        conv3 = tf.nn.relu(self.conv2d(drop2, W3) + b3)
        pool3 = self.maxPool(conv3)
        drop3 = self.dropout(pool3, self.keep_prob_5)

        # ===全连接层====
        Wf = self.weightVariable([8 * 8 * 64, 512])
        bf = self.biasVariable([512])
        drop3_flat = tf.reshape(drop3, [-1, 8 * 8 * 64])
        dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
        dropf = self.dropout(dense, self.keep_prob_75)

        # ===全连接层====
        Wout = self.weightVariable([512, self.outnode])
        bout = self.weightVariable([self.outnode])
        out = tf.add(tf.matmul(dropf, Wout), bout, name='out')
        return out

    def cnnTrain(self, maxiter=1000, accu=0.99, batch_size=100):
        """
        依据训练样本的模型输出与样本实际值进行模型训练
        :param maxiter: 最大迭代次数
        :param accu: 精度阈值，当训练精度大于accu时则停止训练
        :param batch_size: 每轮训练的样本数
        :return: 无返回，但是当模型精度满足要求后会将模型保存
        """
        out = self.cnnLayer()  # 模型输出/预测
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=self.y_))
        train_step = tf.train.AdamOptimizer(0.01).minimize(cross_entropy)

        # 比较标签是否相等，再求的所有数的平均值，tf.cast(强制转换类型)
        accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(self.y_, 1)), tf.float32))

        # 将loss与accuracy保存以供tensorboard使用
        # tf.summary.scalar('loss', cross_entropy)
        # tf.summary.scalar('accuracy', accuracy)

        saver = tf.train.Saver()  # 数据保存器的初始化
        sess = tf.Session()  # 启动会话
        sess.run(tf.global_variables_initializer())
        for n in range(maxiter):
            ind = random.sample(range(len(self.imgs)), batch_size)  # 每次取batch_size张图片
            batch_x = self.imgs[ind]
            batch_y = self.labels[ind]
            _ = sess.run(train_step, feed_dict={self.x: batch_x, self.y_: batch_y})  # 正式训练
            # 打印损失
            # print(loss)
            if n % 100 == 0:  # 每训练100轮输出一次训练精度
                acc = sess.run(accuracy, feed_dict={self.x: batch_x, self.y_: batch_y})  # 获取训练精度
                process_log = '轮数:' + str(n) + ' 训练精度:' + str(acc)
                yield process_log
                print('轮数：', n, ' the train accuracy is :', acc)
                if acc > accu and n > 499:
                    saver.save(sess, self.modelfile)  # 保存模型
                    break
            elif n == (maxiter - 1):
                saver.save(sess, self.modelfile)
        sess.close()

    def predict(self, test_x=test_x):
        """
        预测函数，导入已训练好的模型后再将新样本数据放入，进行模型预测
        :param test_x: 测试样本的自变量
        :return: 模型对测试样本的预测结果
        1: 预测结果（数字标签：0,1,2,3,4,5,...）
        pre: 样本属于各类别的概率，形如：[[0.1, 0.1, 0.0, 0.0, 0.0, 0.8]]
        """
        out = self.cnnLayer()  # 网络输出
        with tf.Session() as sess:
            saver = tf.train.Saver()  # 启动模型保存类Saver
            saver.restore(sess, self.modelfile)  # 调用之前保存的模型
            graph = tf.get_default_graph()  # 获取计算图
            x = graph.get_tensor_by_name('x_data:0')  # 通过tensor的名称获取相应tensor，注意到底是 x_data 还是x_data_1
            pre = sess.run(out, feed_dict={x: test_x})  # 放入测试集样本
        return np.argmax(pre, 1), pre


if __name__ == '__main__':
    # cnnnet = CnnNet()
    # cnnnet.cnnTrain()  # 模型训练
    # pre, pro = cnnnet.predict()
    # acc_test = sum(np.argmax(test_y, axis=1) == pre) / len(pre)  # 测试集精度
    # print(acc_test)
    path = './small_img_gray'  # 灰度图路径
    imgs, labels, number_name = GetImgData(dir=path).readimg()
    x_train, x_test, y_train, y_test = train_test_split(imgs, labels, test_size=0.2)

    cnnNet = CnnNet(modelfile='./temp/train-model',
                    imgs=x_train, labels=y_train)
    cnnNet.cnnTrain(maxiter=1000,  # 最大迭代次数
                    accu=0.95, )  # 指定正确率（499次之后）
