<table>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SeafoodStudios/Cosmica/refs/heads/main/static/logo.png" height="100px"></td>
    <td><h1>Search Engine</h1></td>
  </tr>
</table>

Cosmica is a free, open source search engine that allows you to browse the web without personalization. Nowadays, large tech companies are creating search engines that log and store your data to be sold to companies and to personalize your experience. Therefore, you won't be able to access most of the diverse Internet. Cosmica, on the other hand, allows you to see the more diverse, better Internet freely.

> [!TIP]
> In order to get a better browsing experience, you should search more general things that are family friendly. We store your searches for prolonged periods of time, so please don't search anything bad.

Its features include:
- A safe, polite and ethical web scraper; individual index.
- Fully open source.
- Simple, user-friendly interface.
- Custom crawler.
- Not big tech, made by a single developer.
- If our search engine can't find it, the AI will.

Here's how Cosmica works:
1. Cosmica scrapes the web, starting from a seed URL and finding links in that URL's page, saving it in the database, finding another seed URL, while respecting the "robots.txt" rules.
2. Then, a Flask REST API makes this database available through a Python list of dictionaries format.
3. Another Flask app is used to access the previous API, to make it look smoother, which is the frontend.
4. When the user accesses it, the user will search something and be redirected to the right URL.
5. Then, the site will display the search results. If there are none, AI will make a summary.

You can find Cosmica here:
[https://cosmica.pythonanywhere.com/](https://cosmica.pythonanywhere.com/)

Thank you for reading this, and I hope you enjoy Cosmica!

\- SeafoodStudios
