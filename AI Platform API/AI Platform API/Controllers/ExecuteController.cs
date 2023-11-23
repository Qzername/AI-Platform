using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Numpy;
using System.Drawing;

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ExecuteController : ControllerBase
    {
        [HttpPost("[action]")]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> Execute(IFormFile file)
        {
            float[] rawPicture = new float[28 * 28];

            using (var memoryStream = new MemoryStream())
            {
                await file.CopyToAsync(memoryStream);
                using (var image = (Bitmap)Image.FromStream(memoryStream))
                {
                    for (int y = 0; y < image.Height; y++)
                    {
                        for (int x = 0; x < image.Width; x++)
                        {
                            Color pixelColor = image.GetPixel(x, y);

                            rawPicture[x + (y * image.Height)] = (255 - Convert.ToSingle(pixelColor.R)) / 255f;
                        }
                    }
                }
            }

            float[,,] picture = new float[1, 28, 28];

            for (int x = 0; x < 28; x++)
                for (int y = 0; y < 28; y++)
                    picture[0, x, y] = rawPicture[(x * 28) + y];

            NDarray array = np.array(picture);

            var model = Keras.Models.BaseModel.LoadModel("./Database/Models/FirstRun.h5");
            NDarray prediction = model.Predict(array);

            int maxI = 0;
            float max = -1;

            for (int i = 0; i < 10; i++)
            {
                if (max < (float)prediction[0][i].PyObject)
                {
                    max = (float)prediction[0][i].PyObject;
                    maxI = i;
                }
            }

            return Ok(maxI);
        }
    }
}
