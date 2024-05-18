using System.ComponentModel.DataAnnotations;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
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
        var audioFiles = await GetAudioFilesAsync();

        var response = SendAudioFilesAsync(audioFiles);
    }

    private async Task<List<AudioFile>> GetAudioFilesAsync()
    {
        var audioFiles = new List<AudioFile>();
        foreach (var file in UploadedFiles)
        {
            using var stream = new MemoryStream((int)file.Length);
            await file.CopyToAsync(stream);
            var bytes=stream.ToArray();
            audioFiles.Add(new AudioFile(file.FileName, bytes));
        }
        
        return audioFiles;
    }

    private async Task<string> SendAudioFilesAsync(List<AudioFile> audioFiles)
    {
        using StringContent jsonContent = new(
            JsonSerializer.Serialize(new
            {
                files = audioFiles
            }),
            Encoding.UTF8,
            "application/json");

        using var response = await _httpClient.PostAsync(
            "http://127.0.0.1:5000/submit_input",
            jsonContent);

        //response.EnsureSuccessStatusCode().WriteRequestToConsole();

        var jsonResponse = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"{jsonResponse}\n");
        
        return jsonResponse;
    }
}

public record AudioFile(string Name, byte[] Content);