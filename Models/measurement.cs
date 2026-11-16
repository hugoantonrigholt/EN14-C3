namespace Mikos_Lab.Models
{
    public partial class Measurement
    {
        public int MeasurementId{ get; set; }
        public int SampleId{ get; set; }
        public int ModelVersionId{ get; set; }
        public DateTime MeasuredAt{ get; set; }
   
        public Sample Sample { get; set; } = null!;
        public ModelVersion ModelVersion { get; set; } = null!;
        
         public ICollection<Prediction> Predictions { get; set; } = new List<Prediction>();
   }
}