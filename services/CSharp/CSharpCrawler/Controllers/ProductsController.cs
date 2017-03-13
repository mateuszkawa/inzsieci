using System.Collections.Generic;
using System.Web.Http;
using CSharpCrawler.Models;
using HtmlAgilityPack;
using Swashbuckle.Swagger.Annotations;

namespace CSharpCrawler.Controllers
{
    public class ProductsController : ApiController
    {
        // GET api/products
        [SwaggerOperation("GetAll")]
        public IEnumerable<Product> Get()
        {
            return new []
            {
                new Product
                {
                    Name = "Product1",
                    Description = "Description1",
                    Price = 23.23m
                },
                new Product
                {
                    Name = "Product2",
                    Description = "Description2",
                    Price = 23.24m
                }
            };
        }

        // GET api/products/{name}
        [SwaggerOperation("Get")]
        public IEnumerable<Product> Get(string name)
        {
            var result = new List<Product>();

            var webget = new HtmlWeb();
            var doc = webget.Load("https://mediamarkt.pl/search?query[querystring]=" + name.Replace(' ', '+'));

            foreach (var product in doc.DocumentNode.SelectNodes("//*[@itemtype='http://schema.org/Product']"))
            {
                result.Add(new Product
                {
                    Name = product.SelectSingleNode(".//*[@class='js-product-name']").InnerText.Trim(),
                    Price = decimal.Parse(product.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.',','))
                });
            }

            return result;
        }
    }
}
