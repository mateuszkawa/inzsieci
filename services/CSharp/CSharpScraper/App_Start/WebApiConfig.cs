using System.Net.Http.Headers;
using System.Web.Http;

namespace CSharpScraper
{
    public static class WebApiConfig
    {
        public static void Register(HttpConfiguration config)
        {
            // Web API configuration and services
            config.Formatters.JsonFormatter.SupportedMediaTypes.Add(new MediaTypeHeaderValue("text/html"));
            // Web API routes
            config.MapHttpAttributeRoutes();

            config.Routes.MapHttpRoute(
                name: "DefaultDebugApi",
                routeTemplate: "debug/{controller}",
                defaults: new { controller = "Search", action = "GetDebug" }
            );

            config.Routes.MapHttpRoute(
                name: "DefaultApi",
                routeTemplate: "{controller}",
                defaults: new { controller = "Search", action = "Get" }
            );
        }
    }
}
