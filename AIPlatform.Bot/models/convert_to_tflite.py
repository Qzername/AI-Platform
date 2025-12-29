import tensorflow as tf

name = "c-d-clas.mk1"

model = tf.keras.models.load_model(name + '.keras')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open(name+'.tflite', 'wb') as f:
    f.write(tflite_model)