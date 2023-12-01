using AIPlatformAPI.Data;
using AIPlatformAPI.Services;
using Microsoft.Extensions.Options;
using UniversalTools;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddCors(options =>
{
    options.AddPolicy("CORSpolicy", policy =>
    {
        policy.AllowAnyHeader();
        policy.AllowAnyMethod();
        policy.AllowAnyOrigin();
        policy.SetIsOriginAllowed(x => true);
        policy.SetIsOriginAllowedToAllowWildcardSubdomains();
    });
});

builder.Services.AddSingleton(typeof(SQLManager));

builder.Services.AddSingleton(typeof(ExperimentDatabase));
builder.Services.AddSingleton(typeof(GenerationDatabase));
builder.Services.AddSingleton(typeof(GroupDatabase));
builder.Services.AddSingleton(typeof(PermissionDatabase));

builder.Services.AddSingleton(typeof(ModelManagementService));

//JSON
builder.Services.AddControllers(options =>
    options.AllowEmptyInputInBodyModelBinding = true
    ).AddNewtonsoftJson(options =>
    {
        options.SerializerSettings.NullValueHandling = Newtonsoft.Json.NullValueHandling.Ignore;
    });
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseCors("CORSpolicy");

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();

app.MapControllers();

app.Run();
