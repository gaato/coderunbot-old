import dimscord, asyncdispatch, strutils, options, nre
import config, run, tex

proc messageCreate(s: Shard, m: Message) {.async.} =
  let args = m.content.split(" ")
  if m.author.bot or not args[0].startsWith(prefix):
    return
  let command = args[0].split("\n")[0][prefix.len..args[0].split("\n")[0].high]
  let arg = m.content[(prefix.len + command.len + 1)..m.content.high]
  var sentMessage: Message
  case command.toLower():
  of "test":
    sentMessage = await discord.api.sendMessage(m.channel_id, "Success!")
  of "run":
    sentMessage = await runCode(m, arg)
  of "tex":
    sentMessage = await texToPng(m, arg)
  of "texp":
    sentMessage = await texpToPng(m, arg)
  else:
    return
  discard discord.api.addMessageReaction(
    sentMessage.channel_id,
    sentMessage.id,
    "🚮"
  )
discard """
proc messageReactionAdd(s: Shard, m: Message, u: User, r: Reaction, exists: bool) {.async.} =
  if m.author.id == s.user.id:
    if r.emoji.name == some "🚮":
      discard discord.api.deleteMessage(
        m.channel_id,
        m.id
      )
"""

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
#discord.events.messageReactionAdd = messageReactionAdd

# Connect to Discord and run the bot.
when isMainModule:
  waitFor discord.startSession()
