import httpclient, json, asyncdispatch, dimscord, strutils, tables, options, random, nre
import config, wandboxLang

randomize()
const url = "https://wandbox.org/api/compile.json"

proc codeResult(m: Message, data: JsonNode): Future[Message] {.async.} =
  var fields: seq[EmbedField]   
  var embedColor = 0xff0000
  var files: seq[DiscordFile]
  for item in data.pairs:
    if item.key == "program_message" or item.key == "compiler_message":
      continue
    let val = item.val.getStr
    if item.key == "status" and val == "0":
      embedColor = 0x007000
    if val.len > 1000 or val.splitLines.len > 100:
      files.add(
        DiscordFile(
          name: item.key & ".txt",
          body: val
        )
      )
    else:
      fields.add(
        EmbedField(
          name: item.key,
          value: "```\n" & val & "\n```"
        )
      )
  return await discord.api.sendMessage(
    m.channel_id,
    embed = some Embed(
      title: some "実行結果 Result",
      color: some embedColor,
      author: some EmbedAuthor(
        name: some m.author.username,
        icon_url: some m.author.avatarUrl
      ),
      fields: some fields,
    ),
    files = some files
  )

proc runCode*(m: Message, arg: string): Future[Message] {.async.} =
  let client = newAsyncHttpClient()
  client.headers = newHttpHeaders({
    "Content-Type": "application/json",
    "Accept": "text/plain",
  })
  let argLines = arg.replace(re"```.+\n", "").replace("```", "").strip.splitLines
  let language: string = argLines[0].toLowerAscii
  var compiler: string
  try:
    compiler = compilers[language]
  except KeyError:
    return await discord.api.sendMessage(
      m.channel_id,
      embed = some Embed(
        title: some "以下の言語に対応しています\nThe following languages are supported",
        description: some "`" & languages.join("`, `") & "`",
        color: some 0xff0000,
        author: some EmbedAuthor(
          name: some m.author.username,
          icon_url: some m.author.avatarUrl
        ),
      ),
    )
  let code = argLines[1..argLines.high].join("\n")
  let body = %*{
    "compiler": compiler,
    "code": code,
  }
  let response = await client.request(
    url,
    httpMethod = HttpPost,
    body = $body
  )
  let data = parseJson(await response.body)
  return await codeResult(m, data)