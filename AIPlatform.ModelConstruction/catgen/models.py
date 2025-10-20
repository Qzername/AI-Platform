import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, coddings_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(coddings_size, 4 * 4 * 512),
            nn.Unflatten(1, (512, 4, 4)),
            nn.BatchNorm2d(512),
            
            nn.ConvTranspose2d(512, 256, kernel_size=7, stride=2, padding=3, output_padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(256),
              
            nn.ConvTranspose2d(256, 128, kernel_size=7, stride=2, padding=3, output_padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            
            nn.ConvTranspose2d(128, 64, kernel_size=5, stride=2, padding=2, output_padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
            
            nn.ConvTranspose2d(64, 3, kernel_size=5, stride=2, padding=2, output_padding=1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x)
    
############################################

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            # Input: [B, 3, 48, 64]
            nn.Conv2d(3, 64, kernel_size=5, stride=2, padding=2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout(0.3),

            nn.Conv2d(64, 128, kernel_size=5, stride=2, padding=2),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(128, 256, kernel_size=7, stride=2, padding=3),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Flatten(),
            nn.Linear(16384, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)