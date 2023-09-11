using AIPlatformAPI.Data;
using AIPlatformAPI.Models;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ExperimentsController : ControllerBase
    {
        ExperimentDatabase experimentDatabase;

        public ExperimentsController(ExperimentDatabase experimentDatabase)
        {
            this.experimentDatabase = experimentDatabase;
        }

        [HttpGet]
        public IActionResult Get() => Ok(experimentDatabase.GetAllExperiments());

        [HttpGet("{name}")]
        public IActionResult Get(string name) => Ok(experimentDatabase.GetExperiment(name));

        [HttpPost]
        public IActionResult Post([FromBody] string name)
        {
            experimentDatabase.CreateExperiment(name);
            return Ok();
        }

        [HttpDelete("{id}")] // route -> Experiments/5
        public IActionResult Delete(int id)
        {
            experimentDatabase.DeleteExperiment(id);
            return Ok();
        }
    }
}
