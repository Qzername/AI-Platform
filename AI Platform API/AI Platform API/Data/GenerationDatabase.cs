using AIPlatformAPI.Models;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class GenerationDatabase
    {
        SQLManager sqlManager;

        public GenerationDatabase(SQLManager sqlManager)
        {
            this.sqlManager = sqlManager;
        }

        public Generation[] GetGenerations(int experimentID) => sqlManager.SelectMany<Generation>($"SELECT * FROM Generations WHERE Experiment_ID = {experimentID}");
        public void CreateGeneration(int experimentID, string name) => sqlManager.ExecuteNonQuery($"INSERT INTO Generations(Experiment_ID, Name) VALUES({experimentID}, {name},"+@"""{}"")");
        public void DeleteGeneration(int generationID) => sqlManager.ExecuteNonQuery($"DELETE FROM Generations WHERE ID = {generationID}");
    }
}