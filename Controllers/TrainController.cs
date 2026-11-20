using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Train/Index.cshtml. the data for the page gets added here later
public class TrainController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
