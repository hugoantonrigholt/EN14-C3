using Microsoft.EntityFrameworkCore;

namespace Mikos_Lab.Models
{
    [Index(nameof(UserId),(nameof(Name)), IsUnique = true)]
    public partial class Dataset
    {
        public int DatasetId{ get; set; }
        public int UserId{ get; set; }
        public int BaseModelId{ get; set; }
        public string Name{ get; set; } = "";
        public DateTime CreatedAt{ get; set; }
    
        public User User { get; set; } = null!;
        public BaseModel BaseModel{ get; set; } = null!;
        

        public ICollection<Sample> Samples { get; set; } = new List<Sample>();
        public ICollection<ModelVersion> ModelVersions { get; set; } = new List<ModelVersion>();

    }
}