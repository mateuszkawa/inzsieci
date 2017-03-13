using System.Collections.Generic;
using System.Web.Http;
using CSharpCrawler.Models;
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
            return new[]
            {
                new Product
                {
                    Name = name,
                    Description = "Description1",
                    Price = 23.23m
                },
                new Product
                {
                    Name = name,
                    Description = "Description2",
                    Price = 23.24m
                }
            };
        }
    }
}
