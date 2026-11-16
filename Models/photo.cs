namespace Mikos_Lab.Models
{
    public partial class Photo
    {
        public int PhotoId{ get; set; }
        public int SampleId{ get; set; }
        public int LensId{ get; set; }
        public string PhotoFile{ get; set; } = "";
        public double Sharpness{ get; set; }
        public DateTime TakenAt{ get; set; }
    
        public Sample Sample { get; set; } = null!;
        public Lens Lens { get; set; } = null!;
        
        public ICollection<Cell> Cells { get; set; } = new List<Cell>();
        

    }
}