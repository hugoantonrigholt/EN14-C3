using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Scan/Index.cshtml. the data for the page gets added here later
public class ScanController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
