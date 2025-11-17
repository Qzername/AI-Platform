import torch

def get_current():
    #default is cpu
    device = torch.device("cpu")

    #intel
    if torch.xpu.is_available():
        device = torch.device("xpu")
        print("Using XPU")
    #nvidia (obviously)
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using CUDA")
    else:
        print("Using CPU")

    return device