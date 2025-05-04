
from sklearn.metrics import accuracy_score
import torch
from tqdm.auto import tqdm

def train_set(model, dataloader, loss_fn, optimizer, device):

    train_acc, train_loss = 0, 0

    model.train()

    for X, y in dataloader:
        X = X.to(device)
        y = y.to(device)

        y_logits = model(X)
        loss = loss_fn(y_logits, y)
        train_loss += loss.item()

        y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)
        acc = accuracy_score(y.cpu(), y_pred.cpu())

        train_acc += acc

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader) * 100

    return train_loss, train_acc


def train(model, train_dataloader, loss_fn, optimizer, device, epochs):

    best_train_acc = 0
    best_train_loss = 0

    for epoch in tqdm(range(epochs)):
        train_loss, train_acc = train_set(
            model = model,
            dataloader = train_dataloader,
            loss_fn = loss_fn,
            optimizer = optimizer,
            device = device,
        )

        if train_acc > best_train_acc:
            best_model = model
            best_train_acc = train_acc
            best_train_loss = train_loss


    return best_model, best_train_acc, best_train_loss      
