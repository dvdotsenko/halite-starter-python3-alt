import sys
import os

def doit():
    for f in os.listdir('.'):
        if f.endswith('.hlt'):
            with open('./viewer/game_data.js', 'wb') as destination,\
                    open(f) as source:

                destination.write(('var gameData=' + source.read()).encode('utf-8'))
            return

if __name__ == '__main__':
    doit()
