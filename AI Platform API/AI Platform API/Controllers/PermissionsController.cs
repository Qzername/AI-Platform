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
        public IActionResult Post(PermissionInformation permissionInformation)
        {
            permissionDatabase.AddPermission(permissionInformation.ExperimentID, permissionInformation.GroupID);
            return Ok();
        }

        [HttpDelete] // route -> Experiments/5
        public IActionResult Delete(PermissionInformation permissionInformation)
        {
            permissionDatabase.RemovePermission(permissionInformation.ExperimentID, permissionInformation.GroupID);
            return Ok();
        }

        public struct PermissionInformation
        {
            public int ExperimentID { get; set; }
            public int GroupID { get; set; }
        }
    }
}
