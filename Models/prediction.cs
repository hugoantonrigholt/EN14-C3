using Microsoft.EntityFrameworkCore;
namespace Mikos_Lab.Models
{
    [PrimaryKey(nameof(MeasurementId), nameof(CellId))]
    public partial class Prediction
    {
        public int MeasurementId{ get; set; }
        public int CellId{ get; set; }
        public int LabelId{ get; set; }
        public double Confidence{ get; set; }
    
        public Measurement Measurement { get; set; } = null!;
        public Cell Cell { get; set; } = null!;
        public Label Label{ get; set; } = null!;

        
    }
}