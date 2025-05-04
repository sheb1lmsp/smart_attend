import os
import torch
from django.conf import settings

def save_model(model, class_names, model_name):
    save_path = os.path.join(settings.MEDIA_ROOT, 'models')
    os.makedirs(os.path.join(save_path, model_name), exist_ok=True)
    model_path_name = os.path.join(save_path, model_name, f"{model_name}.pth")
    class_path_name = os.path.join(save_path, model_name, f"{model_name}_class_names.txt")

    torch.save(
        obj=model.state_dict(),
        f=model_path_name
    )

    with open(class_path_name, "w") as f:
        for name in class_names:
            f.write(name + "\n")