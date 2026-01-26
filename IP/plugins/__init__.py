# IP Plugins Package
# Orchestr8 v3.0 - The Fortress Factory
# Dynamic plugin loading directory
#
# Plugin Contract:
# - Each plugin must export PLUGIN_NAME (str)
# - Each plugin must export PLUGIN_ORDER (int)
# - Each plugin must export render(STATE_MANAGERS) -> mo.Html
#
# Plugins are loaded in order by filename prefix (01_, 02_, etc.)
