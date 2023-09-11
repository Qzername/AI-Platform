using AIPlatformAPI.Data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GroupsController : ControllerBase
    {
        GroupDatabase groupDatabase;

        public GroupsController(GroupDatabase groupDatabase)
        {
            this.groupDatabase = groupDatabase;
        }


        [HttpGet("{name}")]
        public IActionResult Get(string name) => Ok(groupDatabase.GetGroup(name));

        [HttpPost]
        public IActionResult Post([FromBody] string name, [FromBody] string password)
        {
            groupDatabase.CreateGroup(name, password);
            return Ok();
        }

        [HttpDelete("{name}")] // route -> Generations/name
        public IActionResult Delete(string name)
        {
            groupDatabase.DeleteGroup(name);
            return Ok();
        }
    }
}
