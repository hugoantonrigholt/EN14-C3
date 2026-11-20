using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Label/Index.cshtml. the data for the page gets added here later
public class LabelController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
