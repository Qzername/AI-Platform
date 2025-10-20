# Catgen

Catgen is a model that generates cat images.

# Why PyTorch

Due to the fact that my GPU (Intel Arc B580) is not well supported in tensorflow especially on Windows 11 machines, I was forced to move to PyTorch. 

# MK1

Since training and debugging DCGANs is a time-consuming process, I ultimately created a model that I am not fully satisfied with, but in the end, it at least generates cat-like figures.

### Structure

batch_size = 256
coddings_size = 256

**Generator**

```py
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
```

**Discriminator**
```py
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
```

Adam optimizer was used for both models, although RMSprop may be worth checking out
```py
generator_optimizer = optimizers.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
discriminator_optimizer = optimizers.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))
```

### Dataset and training

Trained 50 epoches on cat dataset 
source: https://av9.dev/cat-dataset/