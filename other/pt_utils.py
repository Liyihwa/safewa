import torch
def get_device(cuda_id):
    return torch.device("cuda:"+str(cuda_id) if torch.cuda.is_available() else "cpu")
