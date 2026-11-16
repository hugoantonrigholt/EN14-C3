namespace Mikos_Lab.Models
{
    public partial class Lens
    {
        public int LensId{ get; set; }
        public string Name{ get; set; } = "";
        public int Magnification{ get; set; }
        public double Na{ get; set; }
        public double UmPerPx{ get; set; }

         public ICollection<Photo> Photos { get; set; } = new List<Photo>();
    

    }
}