import os
import hikari
import lightbulb
import datetime
from dotenv import load_dotenv

load_dotenv()
bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    default_enabled_guilds=(997221213359313058)
)

@bot.listen()
async def on_started(event: hikari.StartedEvent):
    print('It\'s alive!')

@bot.command
@lightbulb.command('hello', 'Returns a kind greeting')
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hi(ctx):
    await ctx.respond("Hello there my friend")

@bot.command
@lightbulb.command('ping', 'Says Pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")

@bot.command()
@lightbulb.option("count", "The amount of messages to purge.", type=int, max_value=100, min_value=1)
# You may also use pass_options to pass the options directly to the function
@lightbulb.command("purge", "Purge a certain amount of messages from a channel.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext, count: int) -> None:
    """Purge a certain amount of messages from a channel."""
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    # Fetch messages that are not older than 14 days in the channel the command is invoked in
    # Messages older than 14 days cannot be deleted by bots, so this is a necessary precaution
    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")


bot.run()

