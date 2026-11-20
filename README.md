# EN14-C3

Requirements:
////////////
Software

.NET 10 SDK
SQL Server Express LocalDB (comes with Visual Studio’s “ASP.NET and web development” workload, or install it separately)
dotnet-ef tool: dotnet tool install --global dotnet-ef
Optional: SSMS or the VS Code SQL Server extension, to look inside the database

Operating system

LocalDB only runs on Windows. On Mac or Linux they would need a regular SQL Server instance (for example in Docker) and a different connection string.

Project files

The project itself: the Models and Data folders, Program.cs, appsettings.json and the Migrations folder. The guide says to commit Migrations so everyone gets the same database.

Setup commands

dotnet restore
dotnet ef database update
dotnet run
//////////