using AIPlatformAPI.Models;
using AIPlatformAPI.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Numpy;
using Python.Runtime;
using System.Drawing;

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ModelManagementController : ControllerBase
    {
        ModelManagementService modelManagmentService;

        public ModelManagementController(ModelManagementService modelManagmentService)
        {
            this.modelManagmentService = modelManagmentService; 
        }

        [HttpPost("[action]")]
        public async Task<IActionResult> Execute(IFormCollection form)
        {
            ModelIdentifier model = new ModelIdentifier();

            model.ExperimentName = form["ExperimentName"]!;
            model.GenerationName = form["GenerationName"]!;

            var file = form.Files[0];

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

            using (Py.GIL())
            {
                NDarray array;
                array = np.array(picture);

                NDarray prediction = modelManagmentService.Predict(model,array);

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

        [HttpPost]
        public async Task<IActionResult> Post(IFormCollection form)
        {
            ModelIdentifier model = new ModelIdentifier();

            model.ExperimentName = form["ExperimentName"]!;
            model.GenerationName = form["GenerationName"]!;

            using (Py.GIL())
            {
                await modelManagmentService.AddModel(model, form.Files[0]);
            }

            return Ok();
        }

        [HttpDelete]
        public async Task<IActionResult> Delete(IFormCollection form)
        {
            ModelIdentifier model = new ModelIdentifier();

            model.ExperimentName = form["ExperimentName"]!;
            model.GenerationName = form["GenerationName"]!;

            using (Py.GIL())
            {
                modelManagmentService.RemoveModel(model);
            }

            return Ok();
        }
    }
}
