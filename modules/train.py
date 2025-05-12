
import torch
from torch import nn
from pathlib import Path
from modules import data_setup, transform, model as create_model, engine, utils


def train(dep_batch, train_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    train_dataloader, class_names = data_setup.data_setup(
        train_dir = train_dir,
        transform = transform.create_transform(),
        batch_size = 32
    )

    model = create_model.create_model(len(class_names), device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        params = model.parameters(),
        lr = 0.001
    )

    model, train_acc, train_loss = engine.train(
        model = model,
        train_dataloader = train_dataloader,
        loss_fn = loss_fn,
        optimizer = optimizer,
        device = device,
        epochs = 100
    )

    utils.save_model(model, class_names, dep_batch)

    return train_acc, train_loss
