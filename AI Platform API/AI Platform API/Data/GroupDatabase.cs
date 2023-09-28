using AIPlatformAPI.Models;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class GroupDatabase
    {
        SQLManager sqlManager;

        public GroupDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public Group[] GetAllGroups() => sqlManager.SelectMany<Group>($"SELECT * FROM Groups");

        public Group GetGroup(string name) => sqlManager.SelectSingle<Group>($"SELECT * FROM Groups WHERE name=\"{name}\"");

        public void CreateGroup(Group group) => CreateGroup(group.Name, group.Password);
        public void CreateGroup(string name, string password) => sqlManager.ExecuteNonQuery($@"INSERT INTO Groups(Name, Password) VALUES(""{name}"",""{password}"")");
        
        public void DeleteGroup(string name) => sqlManager.ExecuteNonQuery($@"DELETE FROM Groups WHERE Name=""{name}""");
    }
}
