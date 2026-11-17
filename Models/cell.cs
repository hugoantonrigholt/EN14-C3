namespace Mikos_Lab.Models
{
  public partial class Cell
    {
        public int CellId{ get; set; }
        public int PhotoId{ get; set; }
        public int X{ get; set; }
        public int Y{ get; set; }
        public int Radius{ get; set; }
        public FoundBy FoundBy{ get; set; }
        public int? LabelId{ get; set; }
        public DateTime? LabelledAt{ get; set; }

        public Photo Photo { get; set; } = null!; 
        public Label Label { get; set; } = null!;

        public ICollection<Prediction> Predictions { get; set; } = new List<Prediction>();
        

    }

}