# WHY & WHAT

Yet another alternative Halite starter package for Python3

Event loop (read frame > process moves > send moves > read frame) was specifically tuned for multi-threaded environment 
in which a mather thread watches a worker thread and returns computed moves before 1 second-per-move timeout is over,
even if the worker calculating the move is not done.

The goal was to move even further into a stateful constantly-running move calculator that is awaken by 
incoming frame and maintains predictions of future frames. (That is still not in this repo, but the repo is base for that effort.)

Substantial changes:

- Maps, cell references etc are switched to Cartesian system, where all references to cells are `(x,y)` form (and not `[y][x]` form like in the original hlt.py) and "North" is y+=1 (not y-=1 like in the original Halite map). 
- Origin cell is 1,1 not 0,0 (originally had significance for attempts to reflect the map in negative directions, but with switch to vector math, remains just an aesthetic difference) - something that makes the coordinate references closer to Battleships board game.
- In order to switch from "game" to *frame* focus the map data is moved from GameMap to Frame object. The bot class instance that runs the game is now effectively the "Game" but all the does is keep the code and state around.
- The point of this was for me to try asyncio-based flows (cause I am rather fond of 2.7 & Gevent but wanted to see how things are on the other side). So, there is perhaps too much `async def` and `await blah` in here, but that's building blocks for tryly async bot of the future.
- The cardinal enums were switched from int to tuple indicating the direction vector. `NORTH` is `(0,1)`. `WEST` is `(-1,0)`. See bots/models/vector_transform.py for full list. Anyone who understands vectors (how to add them, reverse them, etc) would instantly understand why I switched from arbitrary enum ints - everything that has to do with path / distance calculation becomes very easy.
- Cell references everywhere are tuples of `(x, y)`. Maps are all `dict` objects, one per type of data. Record for a given cell `(x,y)` is found as `frame.production[x,y]` (It's a python trick. `[x,y]` is equivalent to `[(x,y)]`). Effectively the maps are all flat key-value structures with rather fast average access complexity of O(1)
- Iteration through the map is easy - `for (x,y), strength in frame.strength.items()` but it's a rather pointless task to iterate through that. Insted, a list of possible moves is already precomputed (and set to STAY) when frame is parsed. You task is to switch some of those to move to some direction. All interactions are through neighbor graph traversals. In that case, who gives a shit about iteration through map.
- Moves for your cells and your cells only are pre-parsed (at point of frame parsing) into `frame.moves` set. Iterate through that and figure out where you want each to move, change each one and the code will pick up the changes to push to Halite server.

Bonus parts (linux, Mac centric):

- has a built-in viewer initiated by `make show_game` (Uses `open` command to open a locally-hosted version of official JS-based game viewer)
- when one or more of the bots gets `debug` argument in `runGames`, logging is persisted to a local file and can be viewed with `make show_log` command. 

See Overkill bot (`bots/overkill_bot.py`) for example of bootstrapping a bot's logic, `bots/registry.py` file for registering the bot for use and `runGame.sh` for invocation.

Overkill bot is a somewhat massaged Overkill bot taken from https://github.com/erdman/alt-python3-halite-starter/blob/master/README.md which was taken from @nmalaguti Halite forum post http://forums.halite.io/t/so-youve-improved-the-random-bot-now-what/482
   

# HOW TO USE

## `make` flows

See `Makefile` for detail. Some juicy parts:

`make clean run show_logs` will run the bots specified in runGame.sh and will show the logging file contents.

`make show_game` displays the last (only / first) game in a *local* viewer.

`make build_zip` builds the deployable you upload to halite.io

## Coding

See Overkill bot (`bots/overkill_bot.py`). Copy that file or subclass from BaseTimedBot and reimplement `calculate_moves` and `calculate_global_objectives`


# LICENSE

Some of this is derivative of something else in halite's original python package or from wisdom of life in general. Not sure what license that is.
