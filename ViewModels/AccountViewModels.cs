using System.ComponentModel.DataAnnotations;

namespace Mikos_Lab.ViewModels;

public class SignInViewModel
{
    [Required(ErrorMessage = "Enter your username.")]
    public string Username { get; set; } = "";

    [Required(ErrorMessage = "Enter your password.")]
    [DataType(DataType.Password)]
    public string Password { get; set; } = "";
}

public class SignUpViewModel
{
    [Required(ErrorMessage = "Choose a username.")]
    [StringLength(50, MinimumLength = 3, ErrorMessage = "Use 3 to 50 characters.")]
    public string Username { get; set; } = "";

    [Required(ErrorMessage = "Choose a password.")]
    [MinLength(8, ErrorMessage = "Use at least 8 characters.")]
    [DataType(DataType.Password)]
    public string Password { get; set; } = "";

    [Required(ErrorMessage = "Repeat your password.")]
    [Compare(nameof(Password), ErrorMessage = "The passwords do not match.")]
    [DataType(DataType.Password)]
    public string RepeatPassword { get; set; } = "";
}