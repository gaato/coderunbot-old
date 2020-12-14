# CodeRunBot
コードの実行や LaTeX の画像化ができます．

ボットの招待リンクは[こちら](https://discord.com/api/oauth2/authorize?client_id=761428259241328680&permissions=0&scope=bot)．

公式 Discord サーバーは[こちら](https://discord.gg/qRpYRTgvXM)．

使い方は[こちら](https://coderunbot.gart.page/ja/)．

It can run codes and image LaTeX.

[Here](https://discord.com/api/oauth2/authorize?client_id=761428259241328680&permissions=0&scope=bot) is the bot's invitation link.

[Here](https://discord.gg/qRpYRTgvXM) is the official discord server.

[Here](https://coderunbot.gart.page/en/) is how to use.

## 必要要件 Requirements
- Linux or macOS
- python3
- TeXLive
- Poppler (pdftoppm)
- ImageMagick (convert)

## .env
```
DISCORD_TOKEN="YOUR-DISCORD-TOKEN"
```

## 実行方法 How to run it
```
$ git clone git@github.com:Gart2357/coderunbot.git
$ go get -u github.com/gw31415/tex2jpg
$ go install github.com/gw31415/tex2jpg
$ cd coderunbot
$ pip install -r requirements.txt
$ python coderunbot.py
```
