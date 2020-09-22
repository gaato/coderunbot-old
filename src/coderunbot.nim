import dimscord, asyncdispatch, strutils, options, dotenv, os

let env = initDotEnv()
env.load()

let discord = newDiscordClient(getEnv("DISCORD_TOKEN"))

let prefix = "]"

proc messageCreate(s: Shard, m: Message) {.async.} =
  let args = m.content.split(" ")
  if m.author.bot or not args[0].startsWith(prefix):
    return
  let command = args[0][prefix.len..args[0].high]

  case command.toLowerAscii():
  of "test":
    discard await discord.api.sendMessage(m.channel_id, "Success!")
  of "echo":
    var text = args[1..args.high].join(" ")
    if text == "":
      text = "Empty text."
    discard await discord.api.sendMessage(m.channel_id, text)
  else:
    discard

proc onReady(s: Shard, r: Ready) {.async.} =
  echo "Ready as: " & $r.user

  await s.updateStatus(game = some GameStatus(
    name: "around.",
    kind: gatPlaying
  ), status = "idle")

proc messageDelete(s: Shard, m: Message, exists: bool) {.async.} =
  echo "Awild message has been deleted!"

discord.events.onReady = onReady
discord.events.messageCreate = messageCreate
discord.events.messageDelete = messageDelete

# Connect to Discord and run the bot.
when isMainModule:
  waitFor discord.startSession()