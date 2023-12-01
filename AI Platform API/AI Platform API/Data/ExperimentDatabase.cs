using AIPlatformAPI.Models;
using Microsoft.AspNetCore.Server.IIS.Core;
using UniversalTools;

namespace AIPlatformAPI.Data
{
    public class ExperimentDatabase
    {
        SQLManager sqlManager;
        GenerationDatabase generationDatabase;
        GroupDatabase groupDatabase;

        public ExperimentDatabase(SQLManager sqlManager, GenerationDatabase generationDatabase, GroupDatabase groupDatabase)
        {
            this.sqlManager = sqlManager;
            this.generationDatabase = generationDatabase;
            this.groupDatabase = groupDatabase;
        }

        public Experiment[] GetAllExperiments() 
        { 
            var experiments = sqlManager.SelectMany<Experiment>($"SELECT * FROM Experiments"); 
        
            for(int i = 0; i < experiments.Length;i++)
            {
                int experimentID = experiments[i].ID;

                experiments[i].Generations = generationDatabase.GetGenerations(experimentID);
                experiments[i].AllowedGroups = groupDatabase.GetGroup(experimentID);
            }

            return experiments;
        }
        
        public Experiment GetExperiment(string name) 
        { 
            var experiment = sqlManager.SelectSingle<Experiment>($"SELECT * FROM Experiments WHERE Name=\"{name}\"");

            experiment.Generations = generationDatabase.GetGenerations(experiment.ID);
            experiment.AllowedGroups = groupDatabase.GetGroup(experiment.ID);

            return experiment;
        }
        
        public void CreateExperiment(string name) => sqlManager.ExecuteNonQuery($"INSERT INTO Experiments(Name) VALUES(\"{name}\")");
        public void DeleteExperiment(int experimentID)
        {
            var experiment = sqlManager.SelectSingle<Experiment>($"SELECT * FROM Experiments WHERE ID = {experimentID}");

            var generations = generationDatabase.GetGenerations(experimentID);

            foreach (var generation in generations)
                generationDatabase.DeleteGeneration(experiment, generation.ID);

            sqlManager.ExecuteNonQuery($"DELETE FROM Experiments WHERE ID={experimentID}");
        }
    }
}
