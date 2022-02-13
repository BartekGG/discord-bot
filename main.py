import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from discord.ext import commands
import database as db
import utils

load_dotenv()

bot = commands.Bot(command_prefix="!")


@bot.command()
async def get(ctx):
    """Get the available and up to date coupon using '!get' command. Coupon is removed from set and person using the command is added to set of coupon holders."""
    r = db.connect()

    available_coupons = r.smembers("available_coupons")
    if len(available_coupons) == 0:
        await ctx.send("There are no KFC coupons left.")
        return

    coupon = r.spop("available_coupons")
    while(coupon != None):
        code, name, expiry = coupon.split(";", 2)
        expiry_datetime = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S.%f")
        is_up_to_date = expiry_datetime - datetime.today()
        if is_up_to_date.total_seconds() <= 0:
            coupon = r.spop("available_coupons")
            continue
        r.sadd("holders", str(ctx.message.author))
        await ctx.send(f"Code {code} from {name} is valid for approximately {utils.timedelta_format(is_up_to_date)}.")
        await ctx.send("You are now added to list of coupon holders.")
        return
    else:
        await ctx.send("All KFC coupons are expired.")


@bot.command()
async def add(ctx, code):
    """Add new KFC coupon using '!add <code>' command. Person using this command is removed from set of coupon holders."""
    r = db.connect()

    if len(code) != 10:
        await ctx.send("KFC coupon code is invalid.")
        return

    name = str(ctx.message.author)
    expiry = datetime.today() + timedelta(days=7)
    r.sadd("available_coupons", f"{code};{name};{expiry}")
    r.srem("holders", name)
    await ctx.send("KFC coupon successfully added.")
    await ctx.send("You are now removed from list of coupon holders.")


@bot.command()
async def coupons(ctx):
    """Get amount of available KFC coupons using '!coupons' command."""
    r = db.connect()
    await ctx.send(f"There are {len(r.smembers('available_coupons'))} coupons left.")


@bot.command()
async def holders(ctx):
    """Get current KFC coupon holders using '!holders' command."""
    r = db.connect()
    holders = r.smembers("holders")
    await ctx.send(f"Current KFC coupons holders are:\n{holders}")

bot.run(os.getenv('TOKEN'))
