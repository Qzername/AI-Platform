using UniversalTools;

namespace AI_Platform_API.Data
{
    public class ExperimentDatabase
    {
        SQLManager sqlManager;

        public ExperimentDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public void CreateExperiment(string name) => sqlManager.ExecuteNonQuery("INSERT INTO ")
    }
}
