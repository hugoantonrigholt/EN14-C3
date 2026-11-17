using Microsoft.EntityFrameworkCore;

namespace Mikos_Lab.Models

{
    [Index(nameof(Username), IsUnique = true)]

    public partial class User
    {
        public int UserId{ get; set; }
        public string Username{ get; set; } = "";
        public string DisplayName{ get; set; } = "";
        public string PasswordHash{ get; set; } = "";
        public DateTime CreatedAt{ get; set; }

        public ICollection<Dataset> Datasets { get; set; } = new List<Dataset>();

    }
}