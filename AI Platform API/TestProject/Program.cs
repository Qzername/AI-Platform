using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System.Diagnostics;
using System.Drawing;

string onnxModelPath = "./model.onnx";

using (var session = new InferenceSession(onnxModelPath))
{
    // Przygotowanie danych wejściowych (analogicznie do poprzednich przykładów)
    var inputTensor = new DenseTensor<float>(ReadFile("down.png",64,64), new[]{1,64,64,3});

    // Przygotowanie słownika wejścia dla modelu
    var inputMeta = session.InputMetadata.First();
    var inputs = new NamedOnnxValue[] { NamedOnnxValue.CreateFromTensor(inputMeta.Key, inputTensor) };

    // Wykonanie predykcji
    using (var results = session.Run(inputs))
    {
        // Pobranie tensora wyjściowego
        var outputTensor = results.First().AsTensor<float>();

        // Przetworzenie i wyświetlenie wyników
        Console.WriteLine("Wyniki predykcji:");
        foreach (var result in outputTensor)
        {
            Console.WriteLine(result);
        }
    }
}

float[] ReadFile(string path, int width, int height)
{
    float[] picture = new float[width * height*3];

    Bitmap image = new Bitmap(path);

    // Do some processing
    for (int x = 0; x < image.Width; x++)
    {
        for (int y = 0; y < image.Height; y++)
        {
            Color pixelColor = image.GetPixel(x, y);

            int currentPixel = x * y;

            picture[currentPixel] = pixelColor.R/255;
            picture[currentPixel+1] = pixelColor.G/255;
            picture[currentPixel+2] = pixelColor.B/255;
        }
    }

    return picture;
}

Console.ReadKey();