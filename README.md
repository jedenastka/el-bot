# Discord El

**El** is Discord bot made by Grzesiek11 as side project to learn Python. Ideas of this bot are making it's code avalible for everyone and giving all functionality for free.

It's meant to be all-in-one, containing things like music bot, ulities, moderation tools etc. in future. El is also built for modularity and configurability - everyone can write plugins and submit them via pull request or use only on his instance, server admins can configure most of functionality aspects etc.

## Rewrite

This repository contains rewritten version of El. The old version was very hard to maintain cause creator had 0 knowledge of Python when he began the project.

## Name

*El* comes from *eleven*, like the number in my nick. I wanted short name that will look good as main prefix. I was playing *Iji* a bit just before starting the project, in that game everyone has very short names, I think that also had some inpact on the name. *El* as female name was inspired by *Chell*, it sounds similar, so I made El girl... Huh.

## Invite link

[Simple invite (no role)](https://discordapp.com/api/oauth2/authorize?client_id=469107044587405313&permissions=0&scope=bot)

[OP invite (OP role)](https://discordapp.com/api/oauth2/authorize?client_id=469107044587405313&permissions=8&scope=bot)

## Official Discord server

[![Invite](https://i.imgur.com/Q4anxDV.png "Invite")](https://discord.gg/VFkBgXr "Invite")

Here you can ask your question about the bot, test it or see what is planned. Also, if you don't have a GitLab account, it's the best way to report a bug or feature request.

## Dependicies for hosting own instance

* **Device** that can run Python - can be PC, laptop, calculator or phone (if you don't mind lags, potato or piece of wood should be fine).
* **Python itself**, minimal - 3.6.x, recommended - 3.7+
* Latest release of **discord.py library**, you can install it with:
```
python3 -m pip install discord.py[voice]
```
* **gTTS** and **youtube-dl** *(optional)* - for `music` and `tts` modules. Installation command:
```
python3 -m pip install gTTS youtube-dl
```
* **FFmpeg** and **Opus** binaries - again, for anything related to audio. Installation command for Debian-based users:
```
sudo apt install ffmpeg libopus0
```
* **Internet** connecton
* **secrets.py** file:
```py
token = 'your_bot_token'
```

## Licensing

[GNU GPL v3](LICENSE)