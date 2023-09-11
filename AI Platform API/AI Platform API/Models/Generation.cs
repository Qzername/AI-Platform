namespace AIPlatformAPI.Models
{
    public struct Generation
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public Dictionary<string, string> DataRequirements;
    }
}