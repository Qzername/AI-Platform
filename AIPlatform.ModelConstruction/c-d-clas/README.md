# c-d-clas
**C**at/**D**og **Clas**sifier

### Definitions
- `DefaultConv2D` is Convoluted layer 2D with `kernel_size=3, padding="same", activation="relu", kernel_initializer="he_normal"`

### Structure
1. `DefaultConv2D` with `filters=64, kernel_size=7, input_shape=[160,90,3]`
2. Max Pooling 2D
3. `DefaultConv2D` with `filters=128`
4. Max Pooling 2D
5. Flatten
6. `Dense` with `units=64, activation="relu", kernel_initializer="he_normal"`
7. `Dense` with `units=1, activation="sigmoid"`

Output is 0.0-1.0 float value with 0 meaning cat is more likely to be on the picture, and 1 meaning dog is more likely to be on the picture

### Dataset and training

Trained 10 epoches on microsoft/cats_vs_dogs dataset

Model is compiled with parameters: `loss="binary_crossentropy", optimizer="nadam", metrics=["accuracy"]`

### Statistics

Total params: 14,584,836 (55.64 MB)

Trainable params: 7,292,417 (27.82 MB)

Non-trainable params: 0 (0.00 B)

Optimizer params: 7,292,419 (27.82 MB)
