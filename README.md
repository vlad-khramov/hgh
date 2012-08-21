Heroes of Git and Hub
=====================

Heroes of Git and Hub is a game where you become a hero leading army of your Github repositories to glorious victories. Demo version is available at http://hgh.dev8.ru

The source code is distributed under [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) licence.


Installation
------------

1. Clone repo
2. Run `pip install -r requirements.txt`
3. Create application in Github account settings and set GITHUB_APP_ID and GITHUB_API_SECRET in `hgh/settings.py`
4. Run `python manage.py syncdb`
5. Run `python manage.py migrate`
6. Run `python manage.py runserver`
7. Open in your browser http://localhost:8000/
8. Add to cronjobs (hourly) `python path/to/project/crons/update_heroes.py` to auto update heroes and army


Short usage instruction
-----------------------

1. Login with your github account
2. Force a friend to login with her github account
3. Both push the red "Fight!" button
4. Play off your repos against each other
5. Be glad to watch your hero leveling
6. Enjoy!


Comprehensive description
-------------------------

Heroes of Git and Hub is a kind of [ZPG](http://en.wikipedia.org/wiki/Zero-player_game) in sense that stats of a hero and his army are computed from github account and repos properties (public_repos, forks, watchers, etc). But it introduces an action component - the battle. To start one two players have to push red "Fight!" buttons after logon.

During the battle you can choose target for any of your repo-units and select what spell you want to cast at this turn (if you have got one in a spellbook, of course!). Confirm making your choice by pushing the "Move" button. When the opponent makes her decision too, consequences of your actions will be shown to both. If hero discovers all her units are perished she feels sad and becomes defeated.

For winning battles hero is awarded with experience points. And even for being defeated if her army was weaker than the opponent's one. Once hero get enough experience points she gain upper level. With new level race bonuses are recomputed and some additional stats added automatically. Every next level requires more experience points to be reached than previous one.

Any player can compete with others if she wants. For this purpose ratings by hero experince and by overall army power are available at the main page.


Game mechanics
--------------

This section is left blank intentionally. Since not every visitor is game designer or CRPG fan, we suppose. By your first demand we shall fill it with formulae and game logic.

After all, we hope you enjoy our game in some way!

Always opened to feedback and suggestions,  
Vladimir Hramov, Denis Untevskiy