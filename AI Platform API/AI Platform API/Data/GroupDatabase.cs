using AI_Platform_API.Models;
using UniversalTools;

namespace AI_Platform_API.Data
{
    public class GroupDatabase
    {
        SQLManager sqlManager;

        public GroupDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public void CreateGroup(Group group) => CreateGroup(group.Name, group.Password);
        public void CreateGroup(string name, string password) => sqlManager.ExecuteNonQuery($"INSERT INTO Groups(Name, Password) VALUES({name},{password})");

        public Group GetGroup(string name) => sqlManager.SelectSingle<Group>($"SELECT * FROM Groups WHERE name=\"{name}\"");

        public void DeleteGroup(string name) => sqlManager.ExecuteNonQuery($@"DELETE FROM Groups WHERE Name=""{name}""");
    }
}
