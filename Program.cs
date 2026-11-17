using Microsoft.EntityFrameworkCore;
using Mikos_Lab.Data;
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddControllers();
builder.Services.AddDbContext<MikoContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Miko")));
var app = builder.Build();

app.MapControllers();


app.Run();







