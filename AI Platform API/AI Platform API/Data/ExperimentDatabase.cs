using AIPlatformAPI.Models;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class ExperimentDatabase
    {
        SQLManager sqlManager;

        public ExperimentDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public Experiment[] GetAllExperiments() => sqlManager.SelectMany<Experiment>($"SELECT * FROM Experiments");
        public Experiment GetExperiment(string name) => sqlManager.SelectSingle<Experiment>($"SELECT * FROM Experiments WHERE Name=\"{name}\"");
        public void CreateExperiment(string name) => sqlManager.ExecuteNonQuery($"INSERT INTO Experiments(Name) VALUES({name})");
        public void DeleteExperiment(int experimentID) => sqlManager.ExecuteNonQuery($"DELETE FROM Experiments WHERE ID={experimentID}");

    }
}
