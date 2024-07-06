import numpy as np
from keras.utils import np_utils
from keras.datasets import mnist
import matplotlib.pyplot as plt
import random

def display_imgs(imgs, titles, rows, cols):
    for i in range( len(imgs) ):
        plt.subplot(rows, cols, i+1)
        plt.imshow(imgs[i], cmap="gray")
        plt.title(titles[i])
        plt.xticks([]) , plt.yticks([]) # 不显示横纵坐标轴
    plt.show()

class NerualNetwork:
    def __init__(self, input_dim, output_dim, hidde_units):
        # 初始化模型参数
        self.w_ih = np.random.normal(loc=0.0, scale=0.01, size=[input_dim, hidde_units])
        self.b_ih = np.zeros(shape=[1,hidde_units], dtype=np.float32)
        self.w_ho = np.random.normal(loc=0.0, scale=0.01, size=[hidde_units, output_dim])
        self.b_ho = np.zeros(shape=[1,output_dim], dtype=np.float32)

        # 隐藏层激活函数使用sigmoid
        self.activate = lambda x:1.0/(1.0+np.exp(-x))

        # 训练过程用到的变量
        self.y_hidde = None # 隐藏层输出
        self.y_hat = None   # 正向传播输出结果

    def _next_batch(self, x, y, batch_size):
        num_examples = len(y)
        indices = list(range(num_examples))
        random.shuffle(x=indices)

        for i in range(0, num_examples, batch_size):
            batch = indices[i:min(num_examples, i + batch_size)]
            yield x[batch], y[batch]

    def _forward(self,x):
        self.y_hidde = self.activate(np.dot(x, self.w_ih) + self.b_ih)
        self.y_hat = self.activate(np.dot(self.y_hidde, self.w_ho) + self.b_ho)

    def _backword(self, x, y, lr):
        # 计算各层误差
        error_pred = y - self.y_hat
        error_hidde = np.dot( error_pred * self.y_hat * (1 - self.y_hat), self.w_ho.T )

        # 计算梯度
        grad_w_ho = np.dot( self.y_hidde.T, error_pred * self.y_hat * (1-self.y_hat) )
        grad_w_ih = np.dot( x.T, error_hidde * self.y_hidde * (1 - self.y_hidde) )

        # 更新参数
        self.w_ho -= lr * grad_w_ho
        self.w_ih -= lr * grad_w_ih

    def train(self, x , y, learning_rate, num_epoch, batch_size):
        for epoch in range(num_epoch):
            for x_batch, y_batch in self._next_batch(x, y, batch_size):
                # 前向传播
                self._forward(x_batch)

                # 反向传播
                self._backword(x_batch, y_batch, learning_rate)

            # 计算损失
            self._forward(x)
            train_loss = -np.sum(y * np.log(self.y_hat))
            print(f"epoch {epoch+1} loss:{train_loss}")

if __name__ == "__main__":
    # 加载测试数据
    (imgs_train, labels_train), (imgs_test, labels_test) = mnist.load_data()

    # 将2维图片数据调整为1维,并做归一化处理
    num_pixels = imgs_train.shape[1] * imgs_train.shape[2]
    x_train = imgs_train.reshape(imgs_train.shape[0], num_pixels).astype('float32') / 255.0
    x_test = imgs_test.reshape(imgs_test.shape[0], num_pixels).astype('float32') / 255.0

    # 将labels转化为one-hot编码
    y_train = np_utils.to_categorical(labels_train)
    y_test = np_utils.to_categorical(labels_test)
    num_classes = y_train.shape[1]

    # 创建模型
    model = NerualNetwork(input_dim=num_pixels, output_dim=num_classes, hidde_units=16)

    # 训练模型
    model.train(x=x_train, y=y_train, learning_rate=0.01, num_epoch=10, batch_size=600)
