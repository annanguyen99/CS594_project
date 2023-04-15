import sys
sys.path.append("/content/gdrive/MyDrive/protein-env/lib/python3.9/site-packages")

import os
import pickle
from utils import convert_pygraph
import random

import torch
from torch.nn import Linear
import torch.nn.functional as F

from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool

import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
dir = os.path.dirname(dir_path)

networkx_graphs_path = dir + "/data/torch_graphs_040523.pkl"

if os.path.isfile(networkx_graphs_path):
    with open(networkx_graphs_path, "rb") as handle:
        print("Retrieve the pickle!")
        dataset = pickle.load(handle)

# data = dataset[1]
# print(data)
# print(type(dataset))
# print(type(dataset[0]))
print(len(dataset))

'''
NUM_CLASSES = 7
NUM_NODE_FEATURES = 33

torch.manual_seed(12345)
#shuffle the dataset
random.shuffle(dataset)

train_dataset = dataset[:1050]
test_dataset = dataset[1050:]

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

for step, data in enumerate(train_loader):
    print(f'Step {step + 1}:')
    print('=======')
    print(f'Number of graphs in the current batch: {data.num_graphs}')
    print(data)
    print()

# a simple GCN model
class GCN(torch.nn.Module):
    def __init__(self, hidden):
        super(GCN, self).__init__()
        torch.manual_seed(12345)
        self.conv1 = GCNConv(NUM_NODE_FEATURES, hidden)
        self.conv2 = GCNConv(hidden, hidden)
        self.lin = Linear(hidden, NUM_CLASSES)

    def forward(self, x, edge_index, batch):
        # 1. Obtain node embeddings
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)

        # 2. Readout layer
        x = global_mean_pool(x, batch)

        # 3. Apply a final classifier
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)

        return x


model = GCN(hidden=64)
model = model.to(torch.float64)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

def train():
    model.train()

    for data in train_loader:
        out = model(data.x, data.edge_index, data.batch)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()


def test(loader):
    model.eval()

    correct = 0
    y_pred_list = []
    y_label_list = []

    for data in loader:
        out = model(data.x, data.edge_index, data.batch)
        pred = out.argmax(dim=1)
        correct += int((pred == data.y).sum())
        y_pred_list += list(pred.data.cpu().numpy())
        y_label_list += list(data.y.data.cpu().numpy())
    accuracy = correct / len(loader.dataset)
    return accuracy, y_pred_list, y_label_list


for epoch in range(1, 30):
    train()
    train_acc, train_pred, train_label = test(train_loader)
    test_acc, test_pred, test_label = test(test_loader)

    print(f'Epoch: {epoch:03d}, Train Acc: {train_acc:.4f}, Test Acc: {test_acc}')


# constant for classes
classes = (0,1,2,3,4,5,6)

# Build confusion matrix
cf_matrix = confusion_matrix(test_label, test_pred)
df_cm = pd.DataFrame(cf_matrix / np.sum(cf_matrix, axis=1)[:, None], index=[i for i in classes],
                     columns=[i for i in classes])
plt.figure(figsize=(12, 7))
sns.heatmap(df_cm, annot=True)
plt.savefig(dir + '/data/confusion_matrix.png')
'''
