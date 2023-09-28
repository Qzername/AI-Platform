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

        [HttpGet]
        public IActionResult Get() => Ok(groupDatabase.GetAllGroups());

        [HttpGet("{name}")]
        public IActionResult Get(string name) => Ok(groupDatabase.GetGroup(name));

        [HttpPost]
        public IActionResult Post(GroupInformation groupInformation)
        {
            groupDatabase.CreateGroup(groupInformation.Name, groupInformation.Password);
            return Ok();
        }

        public struct GroupInformation
        {
            public string Name { get; set; }
            public string Password { get; set; }    
        }

        [HttpDelete("{name}")] // route -> Generations/name
        public IActionResult Delete(string name)
        {
            groupDatabase.DeleteGroup(name);
            return Ok();
        }
    }
}
