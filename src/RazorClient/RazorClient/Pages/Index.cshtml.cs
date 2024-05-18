using System.ComponentModel.DataAnnotations;
using System.Net.Http.Headers;
using System.Text.Json.Nodes;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Net.Http;
using System.Text.Json;

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
        //var content = new ByteArrayContent(bytes);
        using StringContent jsonContent = new(
        JsonSerializer.Serialize(new
        {
            userId = 77,
            id = 1,
            title = "write code sample",
            completed = false
        }),
        Encoding.UTF8,
        "application/json");

        using HttpResponseMessage response = await _httpClient.PostAsync(
            "http://127.0.0.1:5000/submit_input",
            jsonContent);

        //response.EnsureSuccessStatusCode().WriteRequestToConsole();

        var jsonResponse = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"{jsonResponse}\n");

        //var content = new StringContent(myObject.ToString(), Encoding.UTF8, "application/json");
        //using var response = await _httpClient.PostAsync("http://127.0.0.1:5000", content);
        //var responseText = await response.Content.ReadAsStringAsync();
        //Console.WriteLine(responseText);
    }
}