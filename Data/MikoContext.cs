using Microsoft.EntityFrameworkCore;
using Mikos_Lab.Models;

namespace Mikos_Lab.Data;

public class MikoContext : DbContext
{
    public MikoContext(DbContextOptions<MikoContext> options) : base(options) { }

    // one DbSet = one table
    public DbSet<User> Users => Set<User>();
    public DbSet<Dataset> Datasets => Set<Dataset>();
    public DbSet<BaseModel> BaseModels => Set<BaseModel>();
    public DbSet<ModelVersion> ModelVersions => Set<ModelVersion>();
    public DbSet<Sample> Samples => Set<Sample>();
    public DbSet<Lens> Lenses => Set<Lens>();
    public DbSet<Photo> Photos => Set<Photo>();
    public DbSet<Cell> Cells => Set<Cell>();
    public DbSet<Label> Labels => Set<Label>();
    public DbSet<Measurement> Measurements => Set<Measurement>();
    public DbSet<Prediction> Predictions => Set<Prediction>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // "Student" / "Model" in the table instead of 0 / 1
        modelBuilder.Entity<Cell>()
            .Property(c => c.FoundBy)
            .HasConversion<string>()
            .HasMaxLength(10);

        // only one row can have IsDefault = 1
        modelBuilder.Entity<BaseModel>()
            .HasIndex(b => b.IsDefault)
            .IsUnique()
            .HasFilter("[IsDefault] = 1");

        // sql server allows only one delete path to a table.
        // these links never delete on their own, everything else cascades down from dataset
        modelBuilder.Entity<Prediction>()
            .HasOne(p => p.Cell).WithMany(c => c.Predictions)
            .OnDelete(DeleteBehavior.NoAction); // cell used in a measurement -> 409 on undo
        modelBuilder.Entity<Prediction>()
            .HasOne(p => p.Label).WithMany(l => l.Predictions)
            .OnDelete(DeleteBehavior.NoAction);
        modelBuilder.Entity<Measurement>()
            .HasOne(m => m.ModelVersion).WithMany(v => v.Measurements)
            .OnDelete(DeleteBehavior.NoAction);
        modelBuilder.Entity<Dataset>()
            .HasOne(d => d.BaseModel).WithMany(b => b.Datasets)
            .OnDelete(DeleteBehavior.NoAction);
        modelBuilder.Entity<Photo>()
            .HasOne(p => p.Lens).WithMany(l => l.Photos)
            .OnDelete(DeleteBehavior.NoAction);
        modelBuilder.Entity<Cell>()
            .HasOne(c => c.Label).WithMany(l => l.Cells)
            .OnDelete(DeleteBehavior.NoAction);
    }
}