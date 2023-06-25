from aiohttp import web
from settings import NOTIFICATION_ENDPOINT, NOTIFICATION_CHANNEL_ID


async def start_server(self):
    app = web.Application()
    app.router.add_post(NOTIFICATION_ENDPOINT, self.on_event)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', )
    await site.start()


async def on_event(self, request):
    # Extract event data from the request
    response = await request.json()
    event_operation = response['event_operation']
    event = response['event']

    # Announce the event update in a specific channel
    channel = self.get_channel(NOTIFICATION_CHANNEL_ID)
    await channel.send(f"New event operation {event_operation}: \n{event}")

    return web.Response()
