from ruamel.yaml import YAML

yaml = YAML()
with open("core/basic.yml", "r", encoding="utf-8") as file:
    basic_config = yaml.load(file)
    bot_owner_ids = basic_config['bot_owner_ids']
    bot_prefix = basic_config['bot_prefix']
    message_rate = basic_config['message_rate']