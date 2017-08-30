# tgposts-templates

Telegram bot that helps you to create formatted posts for your Telegram
channels.
For bot to work you'd need to install
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
package from PIP, and set the bot token (obtain from
[@BotFather](https://t.me/BotFather)) in the `bot.py` file.

## Templates

Template can contain any Python code, mandatory is for template to expose `class
Template` (this is hardcoded) with `get_params()`, `set_params()` and
`get_template()` methods. See `templates/example/` for more information.

Bot is multi-user, templates are organized on a per-user basis under the
`templates/` directory. To get rolling, create a sub-directory under
`templates/` named exactly as your username, and an empty `__init__.py` file,
along with the actual template file.

Example:

```bash
mkdir -p templates/br0ziliy
touch templates/br0ziliy/__init__.py
cp templates/example/ExampleTemplate.py templates/br0ziliy/MyChannelTemplate.py
```

## Discalimer

This was an excersice for me to learn the `python-telegram-bot` API and Python
dynamic modules loading. If the bot code hurts you and you'd like to change
something (like, refactor it to proper OO model, or add config file) - PRs are welcome :)
