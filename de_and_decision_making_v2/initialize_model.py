import torch

class InitializeModel:
    @staticmethod
    def initialize_model():
        option = int(input('Enter \'1\' for Default Model Type and Model Directory, else Enter \'0\': '))
        if option == 1:
            model_type= "MiDaS_small"
            model_dir = "intel-isl/MiDaS"
        else:
            model_type = input('Enter Model Type: ')
            model_dir  = input('Enter Model Directory: ')
        
        model = torch.hub.load(model_dir, model_type)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model.to(device)
        model.eval()
        return model, device