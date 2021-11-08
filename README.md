# CodeRunBot

コードの実行や LaTeX の画像化ができます．

ボットの招待リンクは[こちら](https://discord.com/api/oauth2/authorize?client_id=761428259241328680&permissions=0&scope=bot)．

公式 Discord サーバーは[こちら](https://discord.gg/qRpYRTgvXM)．

使い方は[こちら](https://coderunbot.gaato.dev/ja/)．

It can run codes and render LaTeX.

[Here](https://discord.com/api/oauth2/authorize?client_id=761428259241328680&permissions=0&scope=bot) is the bot's invitation link.

[Here](https://discord.gg/qRpYRTgvXM) is the official discord server.

[Here](https://coderunbot.gaato.dev/en/) is how to use.

## 必要要件 Requirements

- Linux or macOS
- python3
- [render-tex-server](https://github.com/gaato/render-tex-server)

## .env

```
DISCORD_TOKEN="YOUR-DISCORD-TOKEN"
```

## 実行方法 How to run it

```
$ git clone git@github.com:gaato/coderunbot.git
$ cd coderunbot
$ pip install -r requirements.txt
$ python coderunbot.py
```

## コマンドの追加の仕方 How to add commands

`commands/command_<コマンド名>.py` というファイルに `async def main(message, arg)` と関数を定義する．

Define a function `async def main(message, arg)` in the file `commands/command_<command name>.py`.
