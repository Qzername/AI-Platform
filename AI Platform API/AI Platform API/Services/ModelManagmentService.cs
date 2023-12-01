using Keras.Models;
using Numpy;
using Python.Runtime;
using AIPlatformAPI.Models;

namespace AIPlatformAPI.Services
{
    public class ModelManagementService
    {
        Dictionary<ModelIdentifier, BaseModel> modelDatabase;

        public ModelManagementService()
        {
            np.arange(1);
            PythonEngine.BeginAllowThreads();

            using (Py.GIL())
            {
                var experiments = Directory.GetFiles("./Models/");

                foreach(var experiment in experiments)
                {
                    var generations = Directory.GetFiles(experiment);

                    foreach(var generation in generations)
                        modelDatabase[new ModelIdentifier()
                        {
                            ExperimentName = experiment,
                            GenerationName = generation
                        }] = BaseModel.LoadModel(generation);
                }
            }

        }

        public NDarray Predict(ModelIdentifier model, NDarray data) => modelDatabase[model].Predict(data);

        public async Task AddModel(ModelIdentifier model, IFormFile file) 
        {
            if (!Directory.Exists($"./Models/{model.ExperimentName}/"))
                Directory.CreateDirectory($"./Models/{model.ExperimentName}/");

            using(var fileStream = new FileStream($"./Models/{model.ExperimentName}/{model.GenerationName}.h5", FileMode.CreateNew))
                await file.CopyToAsync(fileStream);
        }

        public void RemoveModel(ModelIdentifier model) => File.Delete($"./Models/{model.ExperimentName}/{model.GenerationName}.h5");
    }
}
