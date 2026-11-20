using Microsoft.AspNetCore.Mvc;

namespace Mikos_Lab.Controllers;

// shows Views/Account/SignIn.cshtml and SignUp.cshtml.
// handling the form (checking the password, making the account) gets added here later
public class AccountController : Controller
{
    public IActionResult SignIn()
    {
        return View();
    }

    public IActionResult SignUp()
    {
        return View();
    }
}
