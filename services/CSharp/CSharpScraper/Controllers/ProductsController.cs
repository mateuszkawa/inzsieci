using System.Collections.Generic;
using System.Web.Http;
using CSharpScraper.Models;
using HtmlAgilityPack;
using Swashbuckle.Swagger.Annotations;
using System.Linq;
using System;

namespace CSharpScraper.Controllers
{
    public class ProductsController : ApiController
    {
        // GET api/products/{name}
        [SwaggerOperation("Get")]
        public Product Get(string name)
        {
            var result = new List<Product>()
            {
                GetMediaMarkt(name),
                GetSaturn(name),
                GetEuro(name),
                GetNeonet(name)
            };

            return result.OrderBy(p => p.Price).ToList()[0];
        }

        private Product GetMediaMarkt(string name)
        {
            var result = new List<Product>();
            var webget = new HtmlWeb();
            var doc = webget.Load("https://mediamarkt.pl/search?query[querystring]=" + name.Replace(' ', '+'));
            var products = doc.DocumentNode.SelectNodes("//*[@itemtype='http://schema.org/Product']");

            if (products != null)
            {
                foreach (var product in products)
                {
                    result.Add(new Product
                    {
                        Name = product.SelectSingleNode(".//*[@class='js-product-name']").InnerText.Trim(),
                        Price = decimal.Parse(product.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ',')),
                        Url = "https://mediamarkt.pl" + product.SelectSingleNode(".//*[@class='js-product-name']").Attributes["href"].Value
                    });
                }
                return result.OrderBy(p => p.Price).ToList()[0];
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }

        private Product GetSaturn(string name)
        {
            var result = new List<Product>();
            var webget = new HtmlWeb();
            var doc = webget.Load("https://saturn.pl/search?query[querystring]=" + name.Replace(' ', '+'));
            var products = doc.DocumentNode.SelectNodes("//*[@itemtype='http://schema.org/Product']");

            if (products != null)
            {
                foreach (var product in products)
                {
                    result.Add(new Product
                    {
                        Name = product.SelectSingleNode(".//*[@class='js-product-name']").InnerText.Trim(),
                        Price = decimal.Parse(product.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ',')),
                        Url = "https://saturn.pl" + product.SelectSingleNode(".//*[@class='js-product-name']").Attributes["href"].Value
                    });
                }
                return result.OrderBy(p => p.Price).ToList()[0];
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
        private Product GetEuro(string name)
        {
            var result = new List<Product>();
            var webget = new HtmlWeb();
            var doc = webget.Load("http://www.euro.com.pl/search.bhtml?keyword=" + name.Replace(' ', '+'));
            var products = doc.DocumentNode.SelectNodes("//*[@class='product-row']");

            if (products != null)
            {
                foreach (var product in products)
                {
                    var nameNode = product.SelectSingleNode(".//*[@class='product-name']");
                    result.Add(new Product
                    {
                        Name = nameNode.SelectSingleNode(".//*").InnerText.Trim(),
                        Price = decimal.Parse(product.SelectSingleNode(".//*[@class='price-normal selenium-price-normal']").InnerText.Split(new[] { "&nbsp" }, StringSplitOptions.None)[0].Trim()),
                        Url = "https://www.euro.com.pl" + nameNode.SelectSingleNode(".//*").Attributes["href"].Value,
                    });
                }
                return result.OrderBy(p => p.Price).ToList()[0];
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
        private Product GetNeonet(string name)
        {
            var result = new List<Product>();
            var webget = new HtmlWeb();
            var doc = webget.Load("https://www.neonet.pl/catalogsearch/result/?q=" + name.Replace(' ', '+'));
            var products = doc.DocumentNode.SelectNodes("//li");

            if (products != null)
            {
                foreach (var product in products)
                {
                    var nameNode = product.SelectSingleNode(".//*[@class='product-name']");

                    if (nameNode != null)
                    {
                        var priceNode = product.SelectSingleNode(".//*[@class='special-price']");
                        if (priceNode == null)
                            priceNode = product.SelectSingleNode(".//*[@class='price']");
                        else
                            priceNode = priceNode.SelectSingleNode(".//*[@class='price']");

                        result.Add(new Product
                        {
                            Name = nameNode.SelectSingleNode(".//*").InnerText.Trim(),
                            Price = decimal.Parse(priceNode.InnerText.Split('z')[0].Trim()),
                            Url = nameNode.SelectSingleNode(".//*").Attributes["href"].Value,
                        });
                    }
                }
                if(result.Count > 0)
                    return result.OrderBy(p => p.Price).ToList()[0];
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
    }
}
