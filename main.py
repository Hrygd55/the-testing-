import os
import random
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("7911194402:AAFjl3oR9i4dDhBRotS2AP5fOw5x3teCeK8") 

GRID_SIZE = 5
NUM_MINES = 3
SIMULATIONS = 5000

def generate_tiles():
    return [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

def simulate(revealed):
    safe_counts = defaultdict(int)
    hidden = [t for t in generate_tiles() if t not in revealed]
    for _ in range(SIMULATIONS):
        mines = set(random.sample(hidden, NUM_MINES))
        for tile in hidden:
            if tile not in mines:
                safe_counts[tile] += 1
    return {tile: safe_counts[tile] / SIMULATIONS for tile in hidden}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send safe tiles (like `0,0 1,2`) and I’ll predict the safest next.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coords = update.message.text.strip()
        safe_tiles = [tuple(map(int, p.split(','))) for p in coords.split()]
        probs = simulate(safe_tiles)
        best_tile = max(probs, key=probs.get)
        chance = probs[best_tile]
        await update.message.reply_text(f"Safest next tile: {best_tile}\nMine risk: {100 - chance*100:.2f}%")
    except:
        await update.message.reply_text("❌ Invalid format. Example: `0,0 1,1 2,2`")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, predict))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
