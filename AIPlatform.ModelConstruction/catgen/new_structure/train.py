import torch
import torch.nn as nn
import torch.optim as optimizers
import time 

def dcgan(generator, discriminator, dataset, batch_size, codings_size, n_epoches, device):
    generator.to(device)
    discriminator.to(device)
    
    # most of information i found on internet used Adam as an optimizer
    # however RMSprop is sometimes used as well
    # maybe in future it will be worth checking out

    generator_optimizer = optimizers.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    discriminator_optimizer = optimizers.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

    loss_function = nn.BCELoss()

    for epoch in range(n_epoches):
        start = time.time()

        for X_batch, _ in dataset:
            X_batch = X_batch.to(device)

            # === Phase 1: Train Discriminator ===
            noise = torch.randn(batch_size, codings_size, device=device)
            fake_images = generator(noise).detach()  

            # label smoothing is being used here
            # real = 0.9 
            # fake = 0.1
            real_labels = torch.full((batch_size, 1), 0.9, device=device)  
            fake_labels = torch.full((batch_size, 1), 0.1, device=device)  

            all_images = torch.cat([fake_images, X_batch])
            all_labels = torch.cat([fake_labels, real_labels])

            discriminator_optimizer.zero_grad()
            predictions = discriminator(all_images)
            d_loss = loss_function(predictions, all_labels)
            d_loss.backward()
            discriminator_optimizer.step()

            # === Phase 2: Train Generator ===
            noise = torch.randn(batch_size, codings_size, device=device)
            generator_optimizer.zero_grad()
            fake_images = generator(noise)
            predictions = discriminator(fake_images)
            g_loss = loss_function(predictions, torch.ones((batch_size, 1), device=device))  # wants to fool D
            g_loss.backward()
            generator_optimizer.step()

        
        print(f"Epoch {epoch+1}/{n_epoches} | "
              f"Discriminator loss: {d_loss.item():.4f} | Generator loss: {g_loss.item():.4f} | "
              f"time: {time.time()-start:.2f}s")

