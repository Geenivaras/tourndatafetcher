# Tournament Data Fetcher

Python code to fetch smash.gg data

## Usage

Go to your smashdata.gg page

Run in the web console:

```javascript
function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
download(JSON.stringify(data), 'playertag.json', 'text/plain');
```

Download your smashdata.gg page as html file 

Then run:

```bash
python tournDataFetcher.py playertag.json <your-html-file>
```
