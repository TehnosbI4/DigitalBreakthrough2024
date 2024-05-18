using System.ComponentModel.DataAnnotations;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace RazorClient.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private IWebHostEnvironment _environment;

    public IndexModel(ILogger<IndexModel> logger, IWebHostEnvironment hostingEnvironment)
    {
        _logger = logger;
        _environment = hostingEnvironment;
    }

    [BindProperty, Display(Name="File")]
    public IList<IFormFile> UploadedFiles { get; set; }
    
    public void OnPost()
    {
        var e = UploadedFiles;
    }
}