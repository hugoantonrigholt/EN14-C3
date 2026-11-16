namespace Mikos_Lab.Models
{
    public partial class BaseModel
        {
        public int BaseModelId{ get; set; }
        public string Name{ get; set; } = "";
        public string Method{ get; set; } = "";
        public string ModelFile{ get; set; } = "";
        public int MinLabels{ get; set; }
        public bool IsDefault{ get; set; }

        public ICollection<Dataset> Datasets { get; set; } = new List<Dataset>();
        }

}