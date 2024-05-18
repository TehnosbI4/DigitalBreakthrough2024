using System.ComponentModel.DataAnnotations;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace RazorClient.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;
    private IWebHostEnvironment _environment;
    private static HttpClient _httpClient = new();

    public IndexModel(ILogger<IndexModel> logger, IWebHostEnvironment hostingEnvironment)
    {
        _logger = logger;
        _environment = hostingEnvironment;
    }

    [BindProperty, Display(Name="File")]
    public IList<IFormFile> UploadedFiles { get; set; }
    
    public async Task OnPost()
    {
        foreach (var file in UploadedFiles)
        {
            using var stream = new MemoryStream((int)file.Length);
            await file.CopyToAsync(stream);
            var bytes=stream.ToArray();
            await SendMp3Async(bytes);
        }
    }

    private static async Task SendMp3Async(byte[] bytes)
    {
        var content = new ByteArrayContent(bytes);
        using var response = await _httpClient.PostAsync("https://localhost:5000/", content);
        var responseText = await response.Content.ReadAsStringAsync();
        Console.WriteLine(responseText);
    }
}