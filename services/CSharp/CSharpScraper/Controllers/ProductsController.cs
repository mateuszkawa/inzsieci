using System.Collections.Generic;
using System.Web.Http;
using CSharpScraper.Models;
using HtmlAgilityPack;
using Swashbuckle.Swagger.Annotations;
using System.Linq;
using System;
using Microsoft.ApplicationInsights;
using System.Globalization;
using System.Text.RegularExpressions;

namespace CSharpScraper.Controllers
{
    public class ProductsController : ApiController
    {
        private TelemetryClient telemetryClient = new TelemetryClient();

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

            if(result.Count(p => p.Name != null && p.Url != null) > 0)
                return result.Where(p => p.Name != null && p.Url != null).OrderBy(p => p.Price).ToList()[0];
            else
                return new Product() { Name = null, Price = 0.00m, Url = null };
        }

        private Product GetMediaMarkt(string name)
        {
            try
            {
                var result = new List<Product>();
                var webget = new HtmlWeb();
                var doc = webget.Load("https://mediamarkt.pl/search?query[querystring]=" + name.Replace(' ', '+'));
                var products = doc.DocumentNode.SelectNodes("//*[@itemtype='http://schema.org/Product']");

                if (products != null)
                {
                    foreach (var product in products)
                    {
                        var price = "";
                        var productName = "";
                        var url = "";

                        var priceNode = product.SelectSingleNode(".//*[@itemtype='http://schema.org/Offer']");
                        if (priceNode == null) // lista itemow
                        {
                            price = Regex.Replace(product.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ','), @"\s+", "");
                            productName = product.SelectSingleNode(".//*[@class='js-product-name']").InnerText.Trim();
                            url = product.SelectSingleNode(".//*[@class='js-product-name']").Attributes["href"].Value;
                        }
                        else // pojedynczy item
                        {
                            price = Regex.Replace(priceNode.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ','), @"\s+", "");
                            productName = product.SelectSingleNode(".//*[@class='m-productDescr_headline']").InnerText.Trim();
                            url = webget.ResponseUri.AbsolutePath;
                        }

                        if (productName.ToLower().Contains(name.ToLower()))
                        {
                            result.Add(new Product
                            {
                                Name = productName,
                                Price = decimal.Parse(price),
                                Url = "https://mediamarkt.pl" + url
                            });
                        }
                    }
                    if(result.Count > 0)
                        return result.OrderBy(p => p.Price).ToList()[0];
                }
            }
            catch(Exception ex)
            {
                telemetryClient.TrackException(ex);
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }

        private Product GetSaturn(string name)
        {
            try
            {
                var result = new List<Product>();
                var webget = new HtmlWeb();
                var doc = webget.Load("https://saturn.pl/search?query[querystring]=" + name.Replace(' ', '+'));
                var products = doc.DocumentNode.SelectNodes("//*[@itemtype='http://schema.org/Product']");

                if (products != null)
                {
                    foreach (var product in products)
                    {
                        var price = "";
                        var productName = "";
                        var url = "";

                        var priceNode = product.SelectSingleNode(".//*[@itemtype='http://schema.org/Offer']");
                        if (priceNode == null) // lista itemow
                        {
                            price = Regex.Replace(product.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ','), @"\s+", "");
                            productName = product.SelectSingleNode(".//*[@class='js-product-name']").InnerText.Trim();
                            url = product.SelectSingleNode(".//*[@class='js-product-name']").Attributes["href"].Value;
                        }
                        else // pojedynczy item
                        {
                            price = Regex.Replace(priceNode.SelectSingleNode(".//*[@itemprop='price']").Attributes["content"].Value.Replace('.', ','), @"\s+", "");
                            productName = product.SelectSingleNode(".//*[@class='m-productDescr_headline']").InnerText.Trim();
                            url = webget.ResponseUri.AbsolutePath;
                        }

                        if (productName.ToLower().Contains(name.ToLower()))
                        {
                            result.Add(new Product
                            {
                                Name = productName,
                                Price = decimal.Parse(price),
                                Url = "https://saturn.pl" + url
                            });
                        }
                    }
                    if(result.Count > 0)
                        return result.OrderBy(p => p.Price).ToList()[0];
                }
            }
            catch(Exception ex)
            {
                telemetryClient.TrackException(ex);
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
        private Product GetEuro(string name)
        {
            try
            {
                var result = new List<Product>();
                var webget = new HtmlWeb();
                var doc = webget.Load("http://www.euro.com.pl/search.bhtml?keyword=" + name.Replace(' ', '+'));
                var products = doc.DocumentNode.SelectNodes("//*[@class='product-row']");

                if (products != null) // lista itemow
                {
                    foreach (var product in products)
                    {
                        var nameNode = product.SelectSingleNode(".//*[@class='product-name']");
                        var price = Regex.Replace(product.SelectSingleNode(".//*[@class='price-normal selenium-price-normal']").InnerText.Split(new[] { "&nbsp" }, StringSplitOptions.None)[0].Trim().Replace(',','.'), @"\s+", "");

                        result.Add(new Product
                        {
                            Name = nameNode.SelectSingleNode(".//*").InnerText.Trim(),
                            Price = decimal.Parse(price, CultureInfo.InvariantCulture),
                            Url = "https://www.euro.com.pl" + nameNode.SelectSingleNode(".//*").Attributes["href"].Value
                        });
                    }
                }
                else // pojedynczy item
                {
                    products = doc.DocumentNode.SelectNodes("//*[@class='product-box']");

                    if(products != null)
                    {
                        foreach (var product in products)
                        {
                            var nameNode = product.SelectSingleNode(".//*[@class='selenium-product-name']");
                            var price = Regex.Replace(product.SelectSingleNode(".//*[@class='price-normal selenium-price-normal']").InnerText.Split(new[] { "&nbsp" }, StringSplitOptions.None)[0].Trim().Replace(',', '.'), @"\s+", "");

                            result.Add(new Product
                            {
                                Name = nameNode.InnerText.Trim(),
                                Price = decimal.Parse(price, CultureInfo.InvariantCulture),
                                Url = "https://www.euro.com.pl" + webget.ResponseUri.AbsolutePath
                            });
                        }
                    }
                }
                if (result.Count > 0)
                    return result.OrderBy(p => p.Price).ToList()[0];
            }
            catch(Exception ex)
            {
                telemetryClient.TrackException(ex);
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
        private Product GetNeonet(string name)
        {
            try
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

                            var price = Regex.Replace(priceNode.InnerText.Split('z')[0].Trim().Replace(',','.'), @"\s+", "");

                            if (nameNode.SelectSingleNode(".//*").InnerText.Trim().ToLower().Contains(name))
                            {
                                result.Add(new Product
                                {
                                    Name = nameNode.SelectSingleNode(".//*").InnerText.Trim(),
                                    Price = decimal.Parse(price, CultureInfo.InvariantCulture),
                                    Url = nameNode.SelectSingleNode(".//*").Attributes["href"].Value,
                                });
                            }
                        }
                    }
                    if (result.Count > 0)
                        return result.OrderBy(p => p.Price).ToList()[0];
                }
            }
            catch(Exception ex)
            {
                telemetryClient.TrackException(ex);
            }
            return new Product() { Name = null, Price = 0.00m, Url = null };
        }
    }
}
