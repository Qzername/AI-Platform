import torch
import devices
import matplotlib.pyplot as plt

device = devices.get_current()

model = torch.load("./generator.pth", weights_only=False)

noise = torch.randn(16, 256, device=device)
generated_image = model(noise)

n = len(generated_image)
plt.figure(figsize=(n * 3, 3))  

for i in range(n):
    plt.subplot(1, n, i + 1)
    img = generated_image[i].detach().cpu().numpy()  # (C,H,W)
    img = img.transpose(1, 2, 0)  # -> (H,W,C)
    img = (img + 1) / 2  # normalize to [0,1]
    img = img.clip(0, 1)  # just in case
    plt.imshow(img)
    plt.axis("off")

plt.tight_layout()
plt.show()