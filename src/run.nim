import httpclient, json, asyncdispatch, dimscord, strutils, tables, options
import config, languages

const url = "https://wandbox.org/api/compile.json"

proc codeResult(m: Message, data: string) {.async.} =
  discard await discord.api.sendMessage(
    m.channel_id,
    embed = some Embed(
      title: some "実行結果",
      description: some "```\n" & data & "\n```",
      color: some 0x7789ec
    )
  )

proc runCode*(m: Message, arg: string) {.async.} =
  let client = newAsyncHttpClient()
  client.headers = newHttpHeaders({
    "Content-Type": "application/json",
    "Accept": "text/plain",
  })
  let argLines = arg.splitLines
  let language: string = argLines[0]
  var compiler: string
  try:
    compiler = compilers[language]
  except KeyError:
    discard await discord.api.sendMessage(
      m.channel_id,
      "Invalid Language\n" & $compilers
    )
    return
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
  await codeResult(m, await response.body)
