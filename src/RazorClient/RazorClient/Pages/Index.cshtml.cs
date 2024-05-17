using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using IHostingEnvironment = Microsoft.AspNetCore.Hosting.IHostingEnvironment;

namespace RazorClient.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private IHostingEnvironment _environment;

    public IndexModel(ILogger<IndexModel> logger, IHostingEnvironment hostingEnvironment)
    {
        _logger = logger;
        _environment = hostingEnvironment;
    }

    public void OnGet()
    {
    }
    
    [BindProperty]
    public IFormFile Upload { get; set; }
    public async Task OnPostAsync()
    {
        var file = Path.Combine(_environment.ContentRootPath, "uploads", Upload.FileName);
        using (var fileStream = new FileStream(file, FileMode.Create))
        {
            await Upload.CopyToAsync(fileStream);
        }
    }
}