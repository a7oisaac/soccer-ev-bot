import discord
import math
import itertools
import os

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def poisson_probability(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def probability_over(line, lam):
    k = int(line)
    prob = 0
    for i in range(k+1, 15):
        prob += poisson_probability(lam, i)
    return prob

def expected_value(p, payout):
    return (p * payout) - (1 - p)

def generate_picks():
    players = {
        "Striker A Over 2.5 Shots": probability_over(2.5, 3.2),
        "Winger B Over 1.5 SOT": probability_over(1.5, 2.1),
        "GK C Over 3.5 Saves": probability_over(3.5, 3.8),
    }

    payout = 3
    combos = list(itertools.combinations(players.items(), 2))
    results = []

    for combo in combos:
        names = [c[0] for c in combo]
        probs = [c[1] for c in combo]

        combined = probs[0] * probs[1]
        ev = expected_value(combined, payout)

        results.append((names, combined, ev))

    results.sort(key=lambda x: x[2], reverse=True)
    return results[0]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = discord.utils.get(client.get_all_channels(), name="general")

    best = generate_picks()
    names, prob, ev = best

    message = f"""
🔥 **Soccer EV Pick**

- {names[0]}
- {names[1]}

Hit Probability: {round(prob*100,2)}%
Expected Value: {round(ev*100,2)}%
"""

    await channel.send(message)

client.run(TOKEN)
