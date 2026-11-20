using Microsoft.EntityFrameworkCore;
using Mikos_Lab.Data;
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();

// WithViews = controllers can also show the pages in Views/
builder.Services.AddControllersWithViews();

builder.Services.AddDbContext<MikoContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Miko")));
var app = builder.Build();

// serves the files in wwwroot (css, images)
app.UseStaticFiles();

app.MapControllers();

// /Scan opens ScanController.Index, / opens HomeController.Index
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");


app.Run();