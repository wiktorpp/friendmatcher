from user import User, get_user

print("Module message_handler has been loaded.")

async def on_message(message):

    self = get_user(message.author)

    if message.content.startswith(".grant"):
        await self.store_permissions_for_user(message.author)
        await message.channel.send("Permissions granted, you can leave this server now")

    elif message.content.startswith(".help"):
        await message.channel.send(
            "Aviable commands:\n"
            ".enable .en\n"
            ".disable .dis\n"
            ".intro [introduction]\n"
            ".tags <add | del | show>"
            ".match\n"
        )

    elif message.content == ".enable" or message.content == ".en":
        await self.enable_service()

    elif message.content == ".disable" or message.content == ".dis":
        await self.disable_service()
    
    elif message.content.startswith(".intro"):
        new_introduction = message.content[7:]
        if len(new_introduction) == 0:
            await self.dm(
                "Your introduction is:\n"
                f"{self.introduction}\n"
                "To change your introduction, type \".intro <new intro>\""
            )
        else:
            self.introduction = new_introduction
            await self.dm("Changed")

    elif message.content.startswith(".tags"):
        if message.content.startswith(".tags add"):
            self.tags.add_from_str(message.content[9:])
            await self.dm("Added")
        elif message.content.startswith(".tags del"):
            pass
        elif message.content.startswith(".tags show"):
            await self.dm(str(self.tags))
        elif message.content == ".tags":
            await self.dm(str(self.tags))
        else:
            await self.dm("Invalid command")

    elif message.content == ".match":
        try: await message.delete()
        except: pass
        await self.match()

    elif message.content.startswith("%"):
        import io
        import sys
        import traceback
        import textwrap
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            request = message.content[1:]
            request_funct = None #Avoids request_funct not defined
            try:
                exec(
                    "async def request_funct():\n" +
                    "    return_value = (" + request + ")" + "\n"
                    "    globals().update(locals())\n"
                    "    return return_value",
                    globals()
                )
            except:
                exec(
                    "async def request_funct():\n" +
                    "    " + request.replace("\n", "\n    ") + "\n"
                    "    globals().update(locals())\n"
                    "    return None",
                    globals()
                )
            return_value = await request_funct()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            if return_value != None:
                output = str(return_value) + "\n" + output
        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            for chunk in textwrap.wrap(output, 2000, replace_whitespace=False):
                await message.channel.send(chunk)