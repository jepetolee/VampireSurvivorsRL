import torch
import torch.nn as nn
import torch.nn.functional as func
import torch.optim as optim
from torch.distributions import Categorical
import torch.multiprocessing as mp
import numpy as np


class A2C(nn.Module):
    def __init__(self):
        super(A2C, self).__init__()
        self.conv1 = nn.Conv2d(1,4, 5, stride=1)
        self.max_pool1 = nn.MaxPool2d(kernel_size=5)
        self.conv2 = nn.Conv2d(4, 16, 10, stride=2)
        self.max_pool2 = nn.MaxPool2d(kernel_size=3)
        self.conv3 = nn.Conv2d(16, 32, 5, stride=2)
        self.max_pool3 = nn.MaxPool2d(kernel_size=2)
        self.p = nn.Linear(2912, 4)
        self.v = nn.Linear(2912, 1)

    def pi(self, x, softmax_dim=1):
        x = func.relu(self.max_pool1(self.conv1(x)))
        x = func.relu(self.max_pool2(self.conv2(x)))
        x = func.relu(self.max_pool3(self.conv3(x)))
        x = torch.flatten(x, 1)
        x = self.p(x)
        prob = func.softmax(x, softmax_dim)
        return prob

    def value(self, x):
        x = func.relu(self.max_pool1(self.conv1(x)))
        x = func.relu(self.max_pool2(self.conv2(x)))
        x = func.relu(self.max_pool3(self.conv3(x)))
        x = torch.flatten(x, 1)

        x = func.relu(self.v(x))
        return x