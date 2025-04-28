import discord
from data.all_channel_ids import Channel_IDs

ANNOUNCEMENT_CHANNEL_ID = Channel_IDs.bot_status.value

async def on_ready_event(bot):
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🌍 Global commands synced: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Sync failed: {e}")

    announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    if announcement_channel:
        try:
            # Hapus semua pesan di channel
            await announcement_channel.purge()
        except Exception as e:
            print(f"⚠️ Gagal menghapus pesan di announcement channel: {e}")
        
        try:
            # Kirim pesan baru setelah menghapus
            await announcement_channel.send("🔄 Bot berhasil dinyalakan")
        except Exception as e:
            print(f"⚠️ Gagal mengirim pesan di announcement channel: {e}")
