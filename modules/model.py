
from torch import nn
from facenet_pytorch import InceptionResnetV1

def create_model(class_len, device):
    model = InceptionResnetV1(pretrained="vggface2")

    model.last_linear = nn.Linear(
        in_features=1792,
        out_features=class_len,
        bias=False
    )

    model.last_bn = nn.BatchNorm1d(
        num_features=model.last_linear.out_features,
        eps = 0.001,
        momentum=0.1,
        affine=True,
        track_running_stats=True
    )

    for param in model.parameters():
        param.requires_grad = False

    for param in model.last_linear.parameters():
        param.requires_grad = True

    return model.to(device)
