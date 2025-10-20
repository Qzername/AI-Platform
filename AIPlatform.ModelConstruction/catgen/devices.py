import torch

def get_current():
    #default is cpu
    device = torch.device("cpu")

    #intel
    if torch.xpu.is_available():
        device = torch.device("xpu")
    #nvidia (obviously)
    elif torch.cuda.is_available():
        device = torch.device("cuda")

    return device
