# faizan-innovaxel-pervaz
URL Shortening Service

Using Postman You can Use Urls

1. Create short URLs (POST /shorten)
    Add any Link for shortening in Body Json : 
    {
    "url": "https://www.google.com"
    }

2. Retrieve original URLs (GET /shorten/<short_code>)

3. Redirect short URLs to the original (/<short_code>)

4. Update original URLs (PUT /shorten/<short_code>)
    You have to pass a body for updating url on the short code like : 
    {
    "url": "https://www.new-url.com"
    }
5. Delete URLs (DELETE /shorten/<short_code>)
    
6. Track stats (access count) (GET /shorten/<short_code>/stats)

