namespace AIPlatformAPI.Models
{
    public struct Experiment
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public Group[] AllowedGroups { get; set; }
        public Generation[] Generations { get; set; }
    }
}
