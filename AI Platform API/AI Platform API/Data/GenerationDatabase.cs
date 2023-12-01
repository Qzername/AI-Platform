using AIPlatformAPI.Models;
using AIPlatformAPI.Services;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class GenerationDatabase
    {
        SQLManager sqlManager;
        ModelManagementService modelManagementService;

        public GenerationDatabase(SQLManager sqlManager, ModelManagementService modelManagementService)
        {
            this.sqlManager = sqlManager;
            this.modelManagementService = modelManagementService;
        }

        public Generation[] GetGenerations(int experimentID) => sqlManager.SelectMany<Generation>($"SELECT * FROM Generations WHERE Experiment_ID = {experimentID}");
        public void CreateGeneration(int experimentID, string name) => sqlManager.ExecuteNonQuery($"INSERT INTO Generations(Experiment_ID, Name, Requirements) VALUES({experimentID}, \"{name}\", \"\")");
        public void DeleteGeneration(int generationID) => DeleteGeneration(sqlManager.SelectSingle<Experiment>($"SELECT Experiments.* FROM Experiments INNER JOIN Generations ON Experiments.ID = Generations.Experiment_ID WHERE Generations.ID = {generationID}"), generationID);

        public void DeleteGeneration(Experiment experiment, int generationID)
        {
            var currentGeneration = sqlManager.SelectSingle<Generation>($"SELECT * FROM Generations WHERE ID = {generationID}");

            sqlManager.ExecuteNonQuery($"DELETE FROM Generations WHERE ID = {generationID}");

            modelManagementService.RemoveModel(new ModelIdentifier()
            {
                ExperimentName = experiment.Name,
                GenerationName = currentGeneration.Name,
            });
        }
    }
}