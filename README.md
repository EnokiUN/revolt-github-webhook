# revolt-github-webhook
A bot example that handles github webhooks and sends stuff to revolt using voltage and aiohttp's web server capabilities.

## deployment (if you can even call it that)
I am just hosting the bot on replit, do host it all you have to do is:
1. Rreate a new python repl
2. Paste & modify bot.py as desired
3. **Add variables to enviroment**
4. Add the url of the repl (https://examplerepl.exampleuser.repl.co) with "/github" at the end (e.g. https://examplerepl.exampleuser.repl.co/github) to the webhooks of your repository
5. Make sure to add the bot to the server with the channel that the messages are supposed to be sent to and that it has sufficient permissions.
6. Use somthing like uptimerobot to keep the repl alive.

That's it, congrats you have github webhooks in your revolt server, woo!
