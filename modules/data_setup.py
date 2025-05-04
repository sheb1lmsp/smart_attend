
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

def data_setup(train_dir, transform, batch_size=32):

    train_data = ImageFolder(
        root = train_dir,
        transform = transform,
        target_transform = None
    )

    class_names = train_data.classes

    train_dataloader = DataLoader(
        dataset=train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=1
    )

    return train_dataloader, class_names
