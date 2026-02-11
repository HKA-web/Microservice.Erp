using Syncfusion.EJ2.DocumentEditor;
using Syncfusion.EJ2.Spreadsheet;
using Syncfusion.EJ2.PdfViewer;
using Newtonsoft.Json;
using Microsoft.Extensions.Caching.Memory;
using Syncfusion.XlsIO;
using Syncfusion.Pdf;
using Syncfusion.DocIORenderer;
using Syncfusion.Licensing;
using System.Globalization;
using System.Reflection.PortableExecutable;
using System.Collections;
using System.Collections.Specialized;
using System.Net;
using System;

namespace ERPro.NET
{
    public class Base
    {
        public IMemoryCache _cache = new MemoryCache(
                new MemoryCacheOptions
                {
                    SizeLimit = 1024,
                });
        public Base()
        {
            SyncfusionLicenseProvider.RegisterLicense("@32312E312E3232bkOVb/Donh5md37J/QdgVOQvUyEqjSNIrJVS+djxuCU=");
            SyncfusionLicenseProvider.RegisterLicense("Mgo+DSMBaFt+QHJqVk1hXk5Hd0BLVGpAblJ3T2ZQdVt5ZDU7a15RRnVfR15jS3xWcERjXHtcdA==;Mgo+DSMBPh8sVXJ1S0R+X1pFdEBBXHxAd1p/VWJYdVt5flBPcDwsT3RfQF5jTH1TdEdmX35edXFSQg==;ORg4AjUWIQA/Gnt2VFhiQlJPd11dXmJWd1p/THNYflR1fV9DaUwxOX1dQl9gSXtQdkdhXHlfcHFSRGQ=;MjI2MjEzMkAzMjMxMmUzMDJlMzBpbDhTS2lsT3RTVThkZk5uZnJaaTY2WjVjTDRQcTJHdnFjT1NrcHg1cHM4PQ==;MjI2MjEzM0AzMjMxMmUzMDJlMzBDZ28va2dWejhCdEthaEpEL0NGS0JuektIT1JWMWh2NUExY2U0ekdyaXlrPQ==;NRAiBiAaIQQuGjN/V0d+Xk9HfV5AQmBIYVp/TGpJfl96cVxMZVVBJAtUQF1hSn5WdUVhW3pYcXRTQ2hY;MjI2MjEzNUAzMjMxMmUzMDJlMzBhL3N2YjRBcVpWSGN6NW5MWXdMczV0aldEUXZCNkZCU0tOWFlaMVIzdWdRPQ==;MjI2MjEzNkAzMjMxMmUzMDJlMzBtMHVpQmFNbE5pc0hTdGhMdThYTzRFYmJDaVFnM0ZjSml1ajc3K01oU3VjPQ==;Mgo+DSMBMAY9C3t2VFhiQlJPd11dXmJWd1p/THNYflR1fV9DaUwxOX1dQl9gSXtQdkdhXHlfcHNQQmQ=;MjI2MjEzOEAzMjMxMmUzMDJlMzBiL3kvczJualB5REFnT2diY2Q3V2NQMW90VTNsQXQvUE82LzZ5NXFnL3V3PQ==;MjI2MjEzOUAzMjMxMmUzMDJlMzBGUmNtRWlOYlVEV1h4cTNLUG5zbVIwL1k3SFBUVmxHY084SWMyQ3VjNVg4PQ==;MjI2MjE0MEAzMjMxMmUzMDJlMzBhL3N2YjRBcVpWSGN6NW5MWXdMczV0aldEUXZCNkZCU0tOWFlaMVIzdWdRPQ==");
        }
        public void SetCulture()
        {
            CultureInfo cultureInfo = new CultureInfo("en-US");
            /* cultureInfo.TextInfo.ListSeparator = ","; */
            Thread.CurrentThread.CurrentCulture = cultureInfo;
            Thread.CurrentThread.CurrentUICulture = cultureInfo;
            Console.WriteLine(CultureInfo.CurrentCulture.TextInfo);
        }
    }
    public class Document : Base
    {
        public Document() : base() { }
        public string Import(string base64String)
        {
            SetCulture();
            Stream stream = new MemoryStream(Convert.FromBase64String(base64String));
            try
            {
                WordDocument document = WordDocument.Load(stream, FormatType.Docx);
                string json = JsonConvert.SerializeObject(document);
                document.Dispose();
                stream.Dispose();
                return json;
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }

        public string SystemClipboard(string content, string type)
        {
            if (content != null && content != string.Empty)
            {
                try
                {
                    WordDocument document = WordDocument.LoadString(content, GetFormatType(type));
                    string json = JsonConvert.SerializeObject(document);
                    document.Dispose();
                    return json;
                }
                catch (Exception ex)
                {
                    return ex.Message;
                }
            }
            return string.Empty;
        }

        public string ExportPdf(string content)
        {
            Stream document = WordDocument.Save(content, FormatType.Docx);
            Syncfusion.DocIO.DLS.WordDocument docio = new Syncfusion.DocIO.DLS.WordDocument(document, Syncfusion.DocIO.FormatType.Docx);
            DocIORenderer render = new DocIORenderer();
            PdfDocument pdfDocument = render.ConvertToPDF(docio);
            FileStream file = new FileStream("sample.docx", FileMode.OpenOrCreate, FileAccess.ReadWrite);
            pdfDocument.Save(file);
            file.Position = 0;
            pdfDocument.Close();
            document.Close();
            return "success";
        }

        public string ExportSFDT(string content)
        {
            Stream document = WordDocument.Save(content, FormatType.Docx);
            FileStream file = new FileStream("sample.docx", FileMode.OpenOrCreate, FileAccess.ReadWrite);
            document.CopyTo(file);
            file.Close();
            document.Close();
            return "success";
        }

        public string[] RestrictEditing(string passwordBase64, string saltBase64, int spinCount)
        {
            if (passwordBase64 == string.Empty && passwordBase64 == null)
            {
                return Array.Empty<string>();
            }
            return WordDocument.ComputeHash(passwordBase64, saltBase64, spinCount);
        }

        internal static FormatType GetFormatType(string format)
        {
            if (string.IsNullOrEmpty(format))
                throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            switch (format.ToLower())
            {
                case ".dotx":
                case ".docx":
                case ".docm":
                case ".dotm":
                    return FormatType.Docx;
                case ".dot":
                case ".doc":
                    return FormatType.Doc;
                case ".rtf":
                    return FormatType.Rtf;
                case ".txt":
                    return FormatType.Txt;
                case ".xml":
                    return FormatType.WordML;
                case ".html":
                    return FormatType.Html;
                default:
                    throw new NotSupportedException("EJ2 DocumentEditor does not support this file format.");
            }
        }
    }
    public class Spreadsheet : Base
    {
        public Spreadsheet() : base() { }
        public string Open(string base64String, string fileName)
        {
            SetCulture();
            try
            {
                Stream stream = new MemoryStream(Convert.FromBase64String(base64String));
                return Workbook.Open(new OpenRequest
                {
                    File = new FormFile(stream, 0, stream.Length, fileName, fileName)
                });
            }
            catch (Exception e)
            {
                return e.Message;
            }
        }
        public String Save(string jsonString)
        {
            SetCulture();
            SaveSettings? saveSettings = JsonConvert.DeserializeObject<SaveSettings>(jsonString);
            var reader = Workbook.Save(saveSettings).FileStream;
            byte[] buffer = new byte[reader.Length];
            reader.Read(buffer, 0, (int)reader.Length);
            return Convert.ToBase64String(buffer);
        }
        public String Export(string jsonString)
        {
            SetCulture();
            SaveSettings? saveSettings = JsonConvert.DeserializeObject<SaveSettings>(jsonString);
            var reader = Workbook.Save(saveSettings).FileStream;
            byte[] buffer = new byte[reader.Length];
            reader.Read(buffer, 0, (int)reader.Length);

            using (ExcelEngine excelEngine = new ExcelEngine())
            {
                IApplication application = excelEngine.Excel;
                application.DefaultVersion = ExcelVersion.Xlsx;
                IWorkbook workbook = application.Workbooks.Open(new MemoryStream(buffer), ExcelOpenType.Automatic);
                FileStream stream1 = new FileStream("C:\\Users\\syifarahmat.id\\Desktop\\New folder\\Exceljancok.xlsx", FileMode.Create);
                workbook.SaveAs(stream1, ExcelSaveType.SaveAsXLS);
                stream1.Close();

            }
            return "";
        }
        public String GetValues(string jsonString)
        {
            SetCulture();
            SaveSettings? saveSettings = JsonConvert.DeserializeObject<SaveSettings>(jsonString);
            var reader = Workbook.Save(saveSettings).FileStream;
            byte[] buffer = new byte[reader.Length];
            reader.Read(buffer, 0, (int)reader.Length);
            List<Dictionary<string, object>> workbookValues = new List<Dictionary<string, object>>();
            using (ExcelEngine excelEngine = new ExcelEngine())
            {
                IApplication application = excelEngine.Excel;
                application.DefaultVersion = ExcelVersion.Xlsx;
                IWorkbook workbook = application.Workbooks.Open(new MemoryStream(buffer), ExcelOpenType.Automatic);
                foreach (var worksheet in workbook.Worksheets)
                {
                    worksheet.EnableSheetCalculations();
                    List<Dictionary<string, object>> worksheetValues = new List<Dictionary<string, object>>();
                    foreach (IRange range in worksheet.UsedCells)
                    {
                        worksheetValues.Add(new Dictionary<string, object>()
                        {
                            {"Worksheet", range.Worksheet.Name },
                            {"Address", range.Address },
                            {"AddressLocal", range.AddressLocal },
                            {"AddressGlobal", range.AddressGlobal },
                            {"Boolean", range.Boolean },
                            {"Column", range.Column },
                            {"ColumnGroupLevel", range.ColumnGroupLevel },
                            {"ColumnWidth", range.ColumnWidth },
                            {"Count", range.Count },
                            {"DisplayText", range.DisplayText },
                            {"Error", range.Error },
                            {"Formula", range.Formula },
                            {"FormulaArray", range.FormulaArray },
                            {"FormulaHidden", range.FormulaHidden },
                            {"FormulaDateTime", range.FormulaDateTime },
                            {"FormulaBoolValue", range.FormulaBoolValue },
                            {"FormulaErrorValue", range.FormulaErrorValue },
                            {"HasDataValidation", range.HasDataValidation },
                            {"HasBoolean", range.HasBoolean },
                            {"HasDateTime", range.HasDateTime },
                            {"HasFormula", range.HasFormula },
                            {"HasFormulaArray", range.HasFormulaArray },
                            {"HasNumber", range.HasNumber },
                            {"HasRichText", range.HasRichText },
                            {"HasString", range.HasString },
                            {"HasStyle", range.HasStyle },
                            {"IsBlank", range.IsBlank },
                            {"IsBoolean", range.IsBoolean },
                            {"IsError", range.IsError },
                            {"IsGroupedByColumn", range.IsGroupedByColumn },
                            {"IsGroupedByRow", range.IsGroupedByRow },
                            {"IsInitialized", range.IsInitialized },
                            {"LastColumn", range.LastColumn },
                            {"LastRow", range.LastRow },
                            {"Row", range.Row },
                            {"RowGroupLevel", range.RowGroupLevel },
                            {"RowHeight", range.RowHeight },
                            {"CellStyleName", range.CellStyleName },
                            {"Text", range.Text },
                            {"Value", range.Value },
                            {"CalculatedValue", range.CalculatedValue },
                            {"FormulaStringValue", range.FormulaStringValue },
                            {"FormulaNumberValue", range.FormulaNumberValue },
                            {"HasFormulaBoolValue", range.HasFormulaBoolValue },
                            {"HasFormulaErrorValue", range.HasFormulaErrorValue },
                            {"HasFormulaDateTime", range.HasFormulaDateTime },
                            {"HasFormulaNumberValue", range.HasFormulaNumberValue },
                            {"HasFormulaStringValue", range.HasFormulaStringValue },
                            {"IsMerged", range.IsMerged },
                            {"WrapText", range.WrapText },
                            {"HasExternalFormula", range.HasExternalFormula },
                            {"IsStringsPreserved", range.IsStringsPreserved?? false },
                            {"HtmlString", range.HtmlString },
                        }
                        .Where(parameter => parameter.Value != null)
                        .ToDictionary(parameter => parameter.Key, parameter => parameter.Value)
                        );
                    }
                    workbookValues.Add(new Dictionary<string, object>() { { worksheet.Name, worksheetValues }, });
                }
            }
            return JsonConvert.SerializeObject(new Dictionary<string, object>(){
                {"Workbook", workbookValues },
                {"File", Convert.ToBase64String(buffer) },
                {"SaveSetting", saveSettings! },
            }, Formatting.None, new JsonSerializerSettings
            {
                NullValueHandling = NullValueHandling.Ignore,
            });
        }
    }
    public class PdfViewer : Base
    {
        public object Load(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            var memoryCacheEntryOptions = new MemoryCacheEntryOptions().SetPriority(CacheItemPriority.NeverRemove);
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            MemoryStream stream = new MemoryStream();
            object jsonResult = new object();
            if (jsonObject != null && jsonObject.ContainsKey("document"))
            {
                if (jsonObject.ContainsKey("isFileName") && bool.Parse(jsonObject["isFileName"].ToString()!))
                {
                    string? documentPath = jsonObject["document"].ToString();
                    if (!string.IsNullOrEmpty(documentPath))
                    {
                        if (documentPath.StartsWith("http"))
                        {
                            new HttpClient().GetStreamAsync(documentPath).Result.CopyTo(stream);
                        }
                        else
                        {
                            byte[] bytes = File.ReadAllBytes(documentPath);
                            stream = new MemoryStream(bytes);
                        }
                    }
                    else
                    {
                        return (jsonObject["document"] + " is not found");
                    }
                }
                else
                {
                    byte[] bytes = Convert.FromBase64String(jsonObject["document"].ToString()!);
                    stream = new MemoryStream(bytes);
                }
            }
            jsonResult = pdfviewer.Load(stream, jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }

        public object Bookmarks(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            var jsonResult = pdfviewer.GetBookmarks(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object RenderPdfPages(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.GetPage(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object RenderThumbnailImages(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.GetThumbnailImages(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object GetDocumentText(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.GetDocumentText(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object RenderAnnotationComments(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.GetAnnotationComments(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object ExportAnnotations(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.ExportAnnotation(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object ImportAnnotations(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            string jsonResult = string.Empty;
            object JsonResult;
            if (jsonObject != null && jsonObject.ContainsKey("fileName"))
            {
                string? documentPath = jsonObject["document"].ToString();
                if (!string.IsNullOrEmpty(documentPath))
                {
                    jsonResult = File.ReadAllText(documentPath);
                }
                else
                {
                    return (jsonObject["document"] + " is not found");
                }
            }
            else
            {
                string? extension = Path.GetExtension(jsonObject?["importedData"].ToString());
                if (extension != ".xfdf")
                {
                    JsonResult = pdfviewer.ImportAnnotation(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
                    return (JsonConvert.SerializeObject(JsonResult));
                }
                else
                {
                    string? documentPath = jsonObject?["importedData"].ToString();
                    if (!string.IsNullOrEmpty(documentPath))
                    {
                        byte[] bytes = File.ReadAllBytes(documentPath);
                        jsonObject!["importedData"] = Convert.ToBase64String(bytes);
                        JsonResult = pdfviewer.ImportAnnotation(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
                        return (JsonConvert.SerializeObject(JsonResult));
                    }
                    else
                    {
                        return (jsonObject?["document"] + " is not found");
                    }
                }
            }
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object ExportFormFields(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.ExportFormFields(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object ImportFormFields(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.ImportFormFields(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object PrintImages(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            object jsonResult = pdfviewer.GetPrintImage(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (JsonConvert.SerializeObject(jsonResult));
        }
        public object Unload(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            pdfviewer.ClearCache(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return ("Document cache is cleared");
        }
        public object Download(string jsonString)
        {
            SetCulture();
            if (jsonString == string.Empty && jsonString == null)
            {
                return string.Empty;
            }
            Dictionary<string, object>? jsonObject = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonString);
            PdfRenderer pdfviewer = new PdfRenderer(_cache);
            string documentBase = pdfviewer.GetDocumentAsBase64(jsonObject?.ToDictionary(parameter => parameter.Key, parameter => parameter.Value?.ToString()));
            return (documentBase);
        }
    }
}
