using System.ComponentModel.DataAnnotations;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text.Json;
using System.Net.Http;

namespace RazorClient.Pages;

public class IndexModel : PageModel
{
    public List<AnalyzeResult> Results { get; set; }
    
    private readonly ILogger<IndexModel> _logger;
    private IWebHostEnvironment _environment;
    private static HttpClient _httpClient = new() {Timeout = TimeSpan.FromMinutes(30) };
    private string _filesPath;

    public IndexModel(ILogger<IndexModel> logger, IWebHostEnvironment hostingEnvironment)
    {
        _logger = logger;
        _environment = hostingEnvironment;
        _filesPath = Path.Combine(_environment.ContentRootPath, "wwwroot", "AudioFiles");
    }

    [BindProperty, Display(Name = "File")] public IList<IFormFile> UploadedFiles { get; set; }

    public async Task<IActionResult> OnPost()
    {
        var audioFiles = await GetAudioFilesAsync();

        var responseString = await SendAudioFilesAsync(audioFiles);
        
        var response = JsonSerializer.Deserialize<ResponseDto>(responseString);
        
        
        var table = new List<AnalyzeResult>();
        if (response?.Data.Count == audioFiles.Count)
        {
            for (var i = 0; i < audioFiles.Count; i++)
            {
                var file = audioFiles[i];
                var filePath = Path.Combine("AudioFiles", file.Name);
                var predictionResult = response.Data[i];  
                var row = new AnalyzeResult(filePath, predictionResult.Prediction, predictionResult.Text!);
                table.Add(row);
            }
        }
        

        Results = table;
        
        return Partial("_TablePartial", Results);
    }
    
    public void OnGet()
    {
        Results = new List<AnalyzeResult>();
    }
    //
    // public PartialViewResult OnGetTablePartial()
    // {
    //     // Results = new List<AnalyzeResult>()
    //     // {
    //     //     new AnalyzeResult(
    //     //         "AudioFiles/02.05.2024 01_08_44.mp3",
    //     //         true, "ewrtyu")
    //     // };
    //     return Partial("_TablePartial", Results); 
    // }

    private async Task<List<AudioFile>> GetAudioFilesAsync()
    {
        var exists = Directory.Exists(_filesPath);

        if (!exists)
        {
            Directory.CreateDirectory(_filesPath);
        }

        var audioFiles = new List<AudioFile>();
        foreach (var file in UploadedFiles)
        {
            var filePath = Path.Combine(_filesPath, file.FileName);
            await using (var fileStream = new FileStream(filePath, FileMode.Create)) 
            {
                await file.CopyToAsync(fileStream);
            }

            // byte[] bytes = await System.IO.File.ReadAllBytesAsync(filePath);
            // string fileInBase64 = Convert.ToBase64String(bytes);
            // audioFiles.Add(new AudioFile(file.FileName, fileInBase64));
            audioFiles.Add(new AudioFile(file.FileName, filePath));
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

public record AudioFile(string Name, string Content);
public record AnalyzeResult(string Name, bool Status, string Text);

public class PredictionResult
{
    public bool Prediction { get; set; }
    public string? Text { get; set; }
}

public class ResponseDto
{
    public IList<PredictionResult> Data { get; set; }
}