import dotenv, dimscord, os
let env = initDotEnv()
env.load()
let discord* = newDiscordClient(getEnv("DISCORD_TOKEN"))
let prefix* = "]"