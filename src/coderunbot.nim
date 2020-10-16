import dimscord, asyncdispatch, strutils, options, nre, tables
import config, run, tex

var
  userMessageIdToBotMessageId = initOrderedTable[string, string]()
  botMessageIdToAuthorId = initOrderedTable[string, string]()

template addToTable(t: OrderedTable[untyped, untyped], k: untyped, v: untyped) =
  t.add(k, v)
  if t.len > 10:
    for i in t.keys:
      t.del(i)
      break

proc messageCreate(s: Shard, m: Message) {.async.} =
  let args = m.content.split(" ")
  if m.author.bot or not args[0].startsWith(prefix):
    return
  let command = args[0].split("\n")[0][prefix.len..args[0].split("\n")[0].high].strip
  let arg = m.content[(prefix.len + command.len)..m.content.high].strip
  var sentMessage: Message
  try:
    case command.toLower():
    of "test":
      sentMessage = await discord.api.sendMessage(m.channel_id, "Success!")
    of "help":
      sentMessage = await discord.api.sendMessage(
        m.channel_id,
        embed = some Embed(
          title: some "使い方 Help",
          description: some "https://coderunbot.gart.page/"
        )
      )
    of "run":
      sentMessage = await runCode(m, arg)
    of "tex":
      sentMessage = await texToPng(m, arg)
    of "texp":
      sentMessage = await texpToPng(m, arg)
    else:
      return
  except:
    sentMessage = await discord.api.sendMessage(
      m.channel_id,
      embed = some Embed(
        title: some "内部エラー Internal Error",
        color: some 0xff0000,
        author: some EmbedAuthor(
          name: some m.author.username,
          icon_url: some m.author.avatarUrl
        )
      )
    )
  finally:
    discard discord.api.addMessageReaction(
      sentMessage.channel_id,
      sentMessage.id,
      "🚮"
    )
    userMessageIdTobotMessageId.addToTable(m.id, sentMessage.id)
    botMessageIdToAuthorId.addToTable(sentMessage.id, m.author.id)

proc messageUpdate(s: Shard, m: Message, o: Option[Message], exists: bool) {.async.} =
  if userMessageIdToBotMessageId.hasKey(m.id):
    botMessageIdToAuthorId.del(userMessageIdToBotMessageId[m.id])
    discard discord.api.deleteMessage(
      m.channel_id,
      userMessageIdToBotMessageId[m.id]
    )
    userMessageIdToBotMessageId.del(m.id)
    await messageCreate(s, m)

proc messageReactionAdd(s: Shard, m: Message, u: User, r: Reaction, exists: bool) {.async.} =
  if m.author.id == s.user.id:
    if botMessageIdToAuthorId.hasKey(m.id) and botMessageIdToAuthorId[m.id] == u.id:
      if r.emoji.name == some "🚮":
        discard discord.api.deleteMessage(
          m.channel_id,
          m.id
        )

proc onReady(s: Shard, r: Ready) {.async.} =
  echo "Ready as: " & $r.user
  await s.updateStatus(game = some GameStatus(
    name: "]help",
    kind: gatPlaying
  ), status = "idle")

discord.events.onReady = onReady
discord.events.messageCreate = messageCreate
discord.events.messageUpdate = messageUpdate
discord.events.messageReactionAdd = messageReactionAdd

# Connect to Discord and run the bot.
when isMainModule:
  waitFor discord.startSession()
