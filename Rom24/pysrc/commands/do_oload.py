import logging

logger = logging.getLogger()

import merc
import object_creator
import interp
import game_utils
import handler_game
import state_checks


def do_oload(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg1.isdigit():
        ch.send("Syntax: load obj <vnum> <level>.\n")
        return
    level = ch.trust  # default

    if arg2:  # load with a level
        if not arg2.isdigit():
            ch.send("Syntax: oload <vnum> <level>.\n")
            return
        level = int(arg2)
        if level < 0 or level > ch.trust:
            ch.send("Level must be be between 0 and your level.\n")
            return
    vnum = int(arg1)
    if vnum not in merc.itemTemplate:
        ch.send("No object has that vnum.\n")
        return
    obj = object_creator.create_item(merc.itemTemplate[vnum], level)
    if state_checks.CAN_WEAR(obj, merc.ITEM_TAKE):
        obj.to_environment(ch)
    else:
        obj.to_environment(ch.in_room)
    handler_game.act("$n has created $p!", ch, obj, None, merc.TO_ROOM)
    handler_game.wiznet("$N loads $p.", ch, obj, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.trust)
    ch.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('oload', do_oload, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1))
