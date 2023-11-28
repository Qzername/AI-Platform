using Keras.Models;
using Numpy;
using Python.Runtime;

namespace AIPlatformAPI.Services
{
    public class ModelManagmentService
    {
        BaseModel baseModel;

        public ModelManagmentService()
        {
            np.arange(1);
            PythonEngine.BeginAllowThreads();
            Console.WriteLine("123");

            using (Py.GIL())
            {
                baseModel = BaseModel.LoadModel("./Database/Models/FirstRun.h5");
            }
            Console.WriteLine("321");

        }

        public NDarray Predict(NDarray data)
        {
            return baseModel.Predict(data);
        }
    }
}
