import osproc, random, strutils, options, asyncdispatch, nre
import dimscord
import config

randomize()

proc texToPng*(m: Message, arg: string) {.async.} =
  let pid = rand(int.high)
  var f: File
  f = open("tex-template.tex", FileMode.fmRead)
  let texCode = f.readAll.replace("[REPLACE]", arg)
  f.close
  f = open("/tmp/" & $pid & ".tex", FileMode.fmWrite)
  f.write(texCode)
  f.close
  discard execCmd("uplatex -halt-on-error -output-directory=/tmp /tmp/" & $pid & ".tex")
  let pdfResult = execCmd("dvipdfmx -q -o /tmp/" & $pid & ".pdf /tmp/" & $pid & ".dvi")  
  if pdfResult != 0:
    f = open("/tmp/" & $pid & ".log", FileMode.fmRead)
    var err = f.readAll
    f.close
    err = "!" & err.split("!")[1]
    err = err.split("Here")[0]
    discard await discord.api.sendMessage(
      m.channel_id,
      embed = some Embed(
        title: some "エラー Error",
        description: some err,
        color: some 0xff0000,
        author: some EmbedAuthor(
          name: some m.author.username,
          icon_url: some m.author.avatarUrl
        )
      )
    )
    discard execCmd("rm -v " & $pid & ".*")
    return
  let cropResult = execCmd("pdfcrop /tmp/" & $pid & ".pdf --margins \"4 4 4 4\"")
  if cropResult != 0:
    return
  let pngResult = execCmd("pdftoppm -png -r 800 /tmp/" & $pid & "-crop.pdf /tmp/" & $pid)
  if pngResult != 0:
    return
  f = open("/tmp/" & $pid & "-1.png")
  let files = @[DiscordFile(
    name: "output.png",
    body: f.readAll
  )]
  f.close
  discard execCmd("rm -v " & $pid & ".*")
  discard await discord.api.sendMessage(
    m.channel_id,
    embed = some Embed(
      color: some 0x007000,
      image: some EmbedImage(
        url: some "attachment://output.png"
      ),
      author: some EmbedAuthor(
        name: some m.author.username,
        icon_url: some m.author.avatarUrl
      ),
    ),
    files = some files
  )

proc texpToPng*(m: Message, arg: string) {.async.} =
  let pid = rand(int.high)
  var f: File
  f = open("texp-template.tex", FileMode.fmRead)
  let texCode = f.readAll.replace("[REPLACE]", arg)
  f.close
  f = open("/tmp/" & $pid & ".tex", FileMode.fmWrite)
  f.write(texCode)
  f.close
  discard execCmd("uplatex -halt-on-error -output-directory=/tmp /tmp/" & $pid & ".tex")
  let pdfResult = execCmd("dvipdfmx -q -o /tmp/" & $pid & ".pdf /tmp/" & $pid & ".dvi")  
  if pdfResult != 0:
    f = open("/tmp/" & $pid & ".log", FileMode.fmRead)
    var err = f.readAll
    f.close
    err = "!" & err.split("!")[1]
    err = err.split("Here")[0]
    discard await discord.api.sendMessage(
      m.channel_id,
      embed = some Embed(
        title: some "エラー Error",
        description: some err,
        color: some 0xff0000,
        author: some EmbedAuthor(
          name: some m.author.username,
          icon_url: some m.author.avatarUrl
        )
      )
    )
    discard execCmd("rm -v " & $pid & ".*")
    return
  let cropResult = execCmd("pdfcrop /tmp/" & $pid & ".pdf")
  if cropResult != 0:
    return
  let pngResult = execCmd("pdftoppm -png -r 500 /tmp/" & $pid & "-crop.pdf /tmp/" & $pid)
  if pngResult != 0:
    return
  discard execCmd("convert /tmp/" & $pid & "-1.png -gravity northwest -chop 0x30 /tmp/" & $pid & "-2.png")
  discard execCmd("convert /tmp/" & $pid & "-2.png -gravity southeast -chop 0x100 /tmp/" & $pid & "-3.png")
  discard execCmd("convert /tmp/" & $pid & "-3.png -background \"#FFFFFF\" -gravity northwest -splice 300x100 /tmp/" & $pid & "-4.png")
  discard execCmd("convert /tmp/" & $pid & "-4.png -background \"#FFFFFF\" -gravity southeast -splice 300x100 /tmp/" & $pid & "-5.png")
  f = open("/tmp/" & $pid & "-5.png")
  let files = @[DiscordFile(
    name: "output.png",
    body: f.readAll
  )]
  f.close
  discard execCmd("rm -v " & $pid & ".*")
  discard await discord.api.sendMessage(
    m.channel_id,
    embed = some Embed(
      color: some 0x007000,
      image: some EmbedImage(
        url: some "attachment://output.png"
      ),
      author: some EmbedAuthor(
        name: some m.author.username,
        icon_url: some m.author.avatarUrl
      ),
    ),
    files = some files
  )
