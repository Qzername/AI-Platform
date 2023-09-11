using AIPlatformAPI.Models;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class PermissionDatabase
    {
        SQLManager sqlManager;

        public PermissionDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public Group[] GetAllowedGroups(int experimentID) => sqlManager.SelectMany<Group>($"SELECT Groups.ID, Groups.Name FROM Groups, AllowedGroups WHERE AllowedGroups.Experiment_ID = {experimentID}");
        public void AddPermission(int experimentID, int groupID) => sqlManager.ExecuteNonQuery($"INSERT INTO AllowedGroups(Experiment_ID, Group_ID) VALUES({experimentID},{groupID})");
        public void RemovePermission(int experimentID, int groupID) => sqlManager.ExecuteNonQuery($"DELETE FROM AllowedGroups WHERE Experiment_ID = {experimentID} AND Group_ID = {groupID}");
    }
}
