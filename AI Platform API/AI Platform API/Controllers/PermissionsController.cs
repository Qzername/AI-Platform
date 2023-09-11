using AIPlatformAPI.Data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace AIPlatformAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PermissionsController : ControllerBase
    {
        PermissionDatabase permissionDatabase;

        public PermissionsController(PermissionDatabase permissionDatabase)
        {
            this.permissionDatabase = permissionDatabase;
        }

        [HttpGet("{experimentID}")]
        public IActionResult Get(int experimentID) => Ok(permissionDatabase.GetAllowedGroups(experimentID));

        [HttpPost]
        public IActionResult Post([FromBody] int experimentID, [FromBody] int groupID)
        {
            permissionDatabase.AddPermission(experimentID, groupID);
            return Ok();
        }

        [HttpDelete] // route -> Experiments/5
        public IActionResult Delete([FromBody] int experimentID, [FromBody] int groupID)
        {
            permissionDatabase.RemovePermission(experimentID, groupID);
            return Ok();
        }
    }
}
