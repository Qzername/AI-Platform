import tensorflow as tf
import tf2onnx

model = tf.keras.models.load_model('model.h5')

tf2onnx.convert.from_keras(model, output_path='model.onnx')