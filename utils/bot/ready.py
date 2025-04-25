import discord
ANNOUNCEMENT_CHANNEL_ID = 1364799478204207157

async def on_ready_event(bot):
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🌍 Global commands synced: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Sync failed: {e}")

    announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        await announcement_channel.send("🔄 Bot berhasil dinyalakan")