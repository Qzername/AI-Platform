import tensorflow as tf
import tf2onnx

model = tf.keras.models.load_model('discriminator.h5')

tf2onnx.convert.from_keras(model, output_path='discriminator.onnx')