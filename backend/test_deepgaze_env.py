import torch
import torchvision
import timm
import scipy
import matplotlib


print("PyTorch:", torch.__version__)
print("TorchVision:", torchvision.__version__)
print("timm:", timm.__version__)
print("SciPy:", scipy.__version__)
print("Matplotlib:", matplotlib.__version__)

print("CUDA:", torch.cuda.is_available())
