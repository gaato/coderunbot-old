import httpclient, json, asyncdispatch, dimscord, strutils
import config
const url = "https://wandbox.org/api/compile.json"

proc runCode*(m: Message, arg: string) {.async.} =
  let client = newAsyncHttpClient()
  client.headers = newHttpHeaders({
    "Content-Type": "application/json",
    "Accept": "text/plain",
  })
  let argLines = arg.splitLines
  echo argLines
  let compiler = argLines[0]
  let code = argLines[1..argLines.high].join("\n")
  let body = %*{
    "compiler": compiler,
    "code": code,
  }
  echo body
  let response = await client.request(
    url,
    httpMethod = HttpPost,
    body = $body
  )
  discard await discord.api.sendMessage(
    m.channel_id,
    await response.body
  )
