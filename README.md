# CodeRunBot
コードの実行や LaTeX の画像化ができます．

公式 Discord サーバーはこちら．（予定）

使い方は[こちら](https://coderunbot.gart.page/ja/)．

It can run codes and image LaTeX.

Here is the official discord server. (plan)

[Here](https://coderunbot.gart.page/en/) is how to use.

## 必要要件 Requirements
- Linux or macOS
- python3
- go

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
$ python main.py
```
