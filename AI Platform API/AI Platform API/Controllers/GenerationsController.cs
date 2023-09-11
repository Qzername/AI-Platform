using AIPlatformAPI.Data;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GenerationsController : ControllerBase
    {
        GenerationDatabase generationDatabase;

        public GenerationsController(GenerationDatabase generationDatabase)
        {
            this.generationDatabase = generationDatabase;
        }

        [HttpGet("{experimentID}")]
        public IActionResult Get(int experimentID) => Ok(generationDatabase.GetGenerations(experimentID));

        [HttpPost]
        public IActionResult Post([FromBody] int experimentID,[FromBody] string name)
        {
            generationDatabase.CreateGeneration(experimentID, name);
            return Ok();
        }

        [HttpDelete("{generationID}")] // route -> Generations/5
        public IActionResult Delete(int generationID)
        { 
            generationDatabase.DeleteGeneration(generationID);
            return Ok();
        }
    }
}
