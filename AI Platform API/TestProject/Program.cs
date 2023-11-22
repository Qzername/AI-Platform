using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using Numpy;
using System.Diagnostics;
using System.Drawing;

float[,,] picture = new float[1, 28, 28];

float[] rawPicture = ReadFile("./8.png", 28, 28);

for (int x = 0; x < 28; x++)
    for (int y = 0; y < 28; y++)
        picture[0, x, y] = rawPicture[(x*28) + y];

NDarray array = np.array(picture);

Console.WriteLine(array.shape);

var model = Keras.Models.BaseModel.LoadModel("./detector.h5");
NDarray prediction = model.Predict(array);

Console.WriteLine(prediction);


float[] ReadFile(string path, int width, int height)
{
    float[] picture = new float[width * height];

    Bitmap image = new Bitmap(path);

    // Do some processing
    for (int x = 0; x < image.Width; x++)
    {
        for (int y = 0; y < image.Height; y++)
        {
            Color pixelColor = image.GetPixel(x, y);

            int currentPixel = x * y;

            picture[currentPixel] = pixelColor.R/255+pixelColor.G/255+pixelColor.B/255;
        }
    }

    return picture;
}

Console.ReadKey();