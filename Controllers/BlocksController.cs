using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Blocks/Index.cshtml: every block and component, to look at and copy from.
// not part of the app itself
public class BlocksController : Controller
{
    public IActionResult Index()
    {
        return View();
    }
}
