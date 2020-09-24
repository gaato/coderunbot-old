import httpclient, json, asyncdispatch, dimscord, strutils, tables
import config, languages

const url = "https://wandbox.org/api/compile.json"

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
  discard await discord.api.sendMessage(
    m.channel_id,
    await response.body
  )
