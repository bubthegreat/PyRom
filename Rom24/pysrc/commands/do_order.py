import logging


logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


def do_order(ch, argument):
    argument, arg = game_utils.read_word(argument)
    remainder, arg2 = game_utils.read_word(argument)

    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    if not arg or not argument:
        ch.send("Order whom to do what?\n")
        return

    if ch.is_affected(merc.AFF_CHARM):
        ch.send("You feel like taking, not giving, orders.\n")
        return
    victim = None
    if arg == "all":
        fAll = True
        victim = None
    else:
        fAll = False
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not victim.is_affected( merc.AFF_CHARM) or victim.master != ch \
                or (state_checks.IS_IMMORTAL(victim) and victim.trust >= ch.trust):
            ch.send("Do it yourself!\n")
            return
    found = False
    for och in merc.rooms[ch.in_room].people[:]:
        if state_checks.IS_AFFECTED(och, merc.AFF_CHARM) \
                and och.master == ch \
                and (fAll or och == victim):
            found = True
            handler_game.act("$n orders you to '%s'." % argument, ch, None, och, merc.TO_VICT)
            och.interpret(argument)

    if found:
        state_checks.WAIT_STATE(ch, merc.PULSE_VIOLENCE)
        ch.send("Ok.\n")
    else:
        ch.send("You have no followers here.\n")
    return


interp.register_command(interp.cmd_type('order', do_order, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
