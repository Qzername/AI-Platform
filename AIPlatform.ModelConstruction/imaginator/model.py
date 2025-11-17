import torch.nn as nn

class Imaginator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=5, stride=2, padding=2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout(0.3),

            nn.Conv2d(64, 128, kernel_size=5, stride=2, padding=2),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(128, 256, kernel_size=7, stride=2, padding=3),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Flatten(),
            nn.Linear(16384, 3),
        )

    def forward(self, x):
        return self.model(x)