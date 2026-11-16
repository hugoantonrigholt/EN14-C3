namespace Mikos_Lab.Models
{
    public partial class Label
    {
        public int LabelId{ get; set; }
        public string Name{ get; set; } = "";
        public string Colour{ get; set; } = "";
        public bool UsedInTraining{ get; set; }

        public ICollection<Cell> Cells { get; set; } = new List<Cell>();
        public ICollection<Prediction> Predictions { get; set; } = new List<Prediction>();
    

    }
}