import string

class Wish:
    def __init__(self):
        pass

    def format_words(self, text):
        wishlist = []
        text = text.replace("Wishlist: ", "")
        user_input = text.split(",")
        for i in user_input:
            word = i.strip()
            if "-" in word:
                item = []
                for segment in word.split("-"):
                    item.append(segment.capitalize())
                rejoined = "-".join(item).title()
                wishlist.append(rejoined)
            elif "/" in word:
                item = []
                for segment in word.split("/"):
                    item.append(segment.capitalize())
                rejoined = "/".join(item).title()
                wishlist.append(rejoined)
            else:
                item = string.capwords(word)
                wishlist.append(item)
        return wishlist

# wish = Wish()
# print(wish.format_words("Wishlist: swaggering boots Skin, rox's pathFinder outfit, exo-rifle skin"))