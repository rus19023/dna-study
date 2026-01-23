from data.db import decks

## run once to sync in-memory decks to database

# from data.decks import DECKS

# for name, cards in DECKS.items():
#     decks.update_one(
#         {"_id": name},
#         {"$set": {"cards": cards}},
#         upsert=True
#     )

## end run once block



def get_deck_names():
    return sorted(decks.distinct("_id"))


def get_deck(deck_name):
    doc = decks.find_one({"_id": deck_name})
    return doc["cards"] if doc else []


def add_card(deck_name, question, answer):
    decks.update_one(
        {"_id": deck_name},
        {
            "$push": {
                "cards": {
                    "question": question,
                    "answer": answer
                }
            }
        },
        upsert=True
    )
    
