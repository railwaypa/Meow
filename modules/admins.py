from pyrogram import Client, filters
from pyrogram.types import Message
from config import HNDLR, call_py
from modules.helpers.decorators import authorized_users_only
from modules.helpers.handlers import skip_current_song, skip_item
from modules.helpers.queues import QUEUE, clear_queue
from config import SUDO_USERS

@Client.on_message(filters.user(SUDO_USERS) & filters.command(["skip"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.me & filters.command(["skip"], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ Try again!**")
        elif op == 1:
            await m.reply("Skip done**")
        else:
            await m.reply(
                f"**⏭ song name** \n**🎵 Now** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ Give name to skip: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.user(SUDO_USERS) & filters.command(["end", "stop"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.me & filters.command(["end", "stop"], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**✅ stoped **")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**❌ Try again!**")


@Client.on_message(filters.user(SUDO_USERS) & filters.command(["pause"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.me & filters.command(["pause"], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ Pause.**\n\n• give command to play again » {HNDLR}resume"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("** ❌ Try again!**")


@Client.on_message(filters.user(SUDO_USERS) & filters.command(["resume"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.me & filters.command(["resume"], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶ resumed**\n\n• Give command » {HNDLR}pause**"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**❌ Try again!**")
