namespace Mikos_Lab.Models
{
    public partial class Sample
    {
        public int SampleId{ get; set; }
        public int DatasetId{ get; set; }
        public string Name{ get; set; } = "";
        public string Light{ get; set; } = "";
        public double? KnownLivePct{ get; set; }
        public DateOnly PreparedOn{ get; set; }
    
        public Dataset Dataset{ get; set; } = null!;
        
        public ICollection<Measurement> Measurements { get; set; } = new List<Measurement>();
        public ICollection<Photo> Photos { get; set; } = new List<Photo>();
    }
}