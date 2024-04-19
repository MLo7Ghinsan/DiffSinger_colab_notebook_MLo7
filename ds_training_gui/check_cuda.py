import torch

def check_cuda():
    if torch.cuda.is_available():
        return True
    else:
        return False
