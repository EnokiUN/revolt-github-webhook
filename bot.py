from os import getenv
from hashlib import sha256
from hmac import new
from json import dumps
import voltage
from aiohttp import web

class GithubClient(voltage.Client):
    def __init__(self, channel_id: str, webhook_secret: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.secret = lambda x: new(webhook_secret.encode(), dumps(x, separators=(",", ":")).encode(), sha256).hexdigest()
        self.channel: voltage.Channel
        self.listeners = {"ready": self.handle_webserver}

        self.app = web.Application()
        
        async def home(request):
            return web.Response(text="Hello, World!")
        
        async def github(request):
            data = await request.json()
            headers = request.headers
            action = data['action']
            event = headers["X-Github-Event"]
            if not headers["X-Hub-Signature-256"][7:] == self.secret(data):
                return web.Response(status=403)
            if handler := getattr(self, f"github_{event}_{action}", None):
                await handler(data)
            return web.Response(status=200)

        self.app.add_routes([web.get("/", home), web.post("/github", github)])

    async def handle_webserver(self):
        self.channel = self.get_channel(self.channel_id)
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()

    async def github_issue_comment_created(self, data):
        number = data['issue']['number']
        url = data['issue']['url']
        sender_name = data['sender']['login']
        sender_avatar = data['sender']['avatar_url']
        comment_content = data['comment']['body']
        embed = voltage.SendableEmbed(
            title = f"New comment on issue #{number}",
            url = url,
            description = f"{sender_name}: {comment_content}",
            icon_url = sender_avatar,
            colour = "#ffff00"
        )
        await self.channel.send("[]()", embed=embed)

client = GithubClient(getenv("CHANNEL"), getenv("WEBHOOK_SECRET"))

client.run(getenv("TOKEN"))
