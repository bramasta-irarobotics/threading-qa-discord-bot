import discord

async def on_ready_event(bot):
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🌍 Global commands synced: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Sync failed: {e}")
