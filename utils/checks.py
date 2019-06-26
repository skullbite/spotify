import requests
import json
owners = [158750488563679232, 497749482252009472]

config = json.load(open("config.json"))
friends = config["friends"]

def is_owner(ctx):
    return ctx.author.id in owners

def has_voted(ctx):
    if ctx.author.id in friends or ctx.author.id in owners:
        return True
    check_path = "https://discordbots.org/api/bots/{ctx.bot.user.id}/check?userId="
    voted = requests.get(check_path + str(ctx.author.id), headers={"Authorization": config["dbl"]}).json()
    return bool(voted["voted"])
