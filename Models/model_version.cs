using Microsoft.EntityFrameworkCore;
namespace Mikos_Lab.Models
{
    [Index(nameof(DatasetId),nameof(VersionNo), IsUnique = true)]
    public partial class ModelVersion
    {
        public int ModelVersionId{ get; set; }
        public int DatasetId{ get; set; }
        public int VersionNo{ get; set; }
        public string ModelFile{ get; set; } = "";
        public int LabelsUsed{ get; set; }
        public double? Accuracy{ get; set; }
        public DateTime TrainedAt{ get; set; }
        public Dataset Dataset { get; set; } = null!; //Navigation property: this version belongs to one dataset.

        public ICollection<Measurement> Measurements { get; set; } = new List<Measurement>();

        
    }
}