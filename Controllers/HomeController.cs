using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Home/Index.cshtml. the data for the page gets added here later
public class HomeController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
