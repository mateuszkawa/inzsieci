# Service

To run queries, use the following URL:

http://csharpscraper.azurewebsites.net/api/products/ + name of the product, with spaces changed to %20.

Currently MediaMarkt, Neonet, Saturn and Euro are working.


# Start/stop service

To manage service:

1. Create DreamSpark account with [this](http://weka.pwr.edu.pl/2897992,41.dhtml)
2. I'm not sure how it's working, but to be safe, [buy yourself Azure license (it's free for students)](https://e5.onthehub.com/WebStore/OfferingDetails.aspx?o=98a24997-f5b7-e611-9423-b8ca3a5db7a1&ws=98c060e9-b28b-e011-969d-0030487d8897&vsro=8)
3. Send me your account's email so I can add you to the project as an administrator.
4. If everything goes well, you can login into Azure portal and start/stop service by yourself.
5. If you're not an "fancy-UI" person, you can use PowerShell to do the same:
    1. [Install node.js](https://nodejs.org/en/download/)
    2. Using PowerShell and npm, install Azure CLI
        npm install -g azure-cli
    3. Login to the Azure account
        azure login
    4. Now you can stop scraper with this command
        azure webapp stop CSharpScraper CSharpScraper
    5. And start again the app with this command
        azure webapp start CSharpScraper CSharpScraper
