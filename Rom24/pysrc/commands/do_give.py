import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks

def do_give(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg2:
        ch.send("Give what to whom?\n")
        return
    if arg1.isdigit():
        # 'give NNNN coins victim'
        amount = int(arg1)
        if amount <= 0 or (arg2 != "coins" and arg2 != "coin" and arg2 != "gold" and arg2 != "silver"):
            ch.send("Sorry, you can't do that.\n")
            return
        silver = arg2 != "gold"
        argument, arg2 = game_utils.read_word(argument)
        if not arg2:
            ch.send("Give what to whom?\n")
            return
        victim = ch.get_char_room(arg2)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if ( not silver and ch.gold < amount) or (silver and ch.silver < amount):
            ch.send("You haven't got that much.\n")
            return
        if silver:
            ch.silver -= amount
            victim.silver += amount
        else:
            ch.gold -= amount
            victim.gold += amount

        act("$n gives you %d %s." % (amount, "silver" if silver else "gold"), ch, None, victim, merc.TO_VICT)
        act("$n gives $N some coins.", ch, None, victim, merc.TO_NOTVICT)
        act("You give $N %d %s." % (amount, "silver" if silver else "gold"), ch, None, victim, merc.TO_CHAR)

        if victim.is_npc() and victim.act.is_set(merc.ACT_IS_CHANGER):
            change = 95 * amount / 100 / 100 if silver else 95 * amount
            if not silver and change > victim.silver:
                victim.silver += change
            if silver and change > victim.gold:
                victim.gold += change
            if change < 1 and victim.can_see(ch):
                act("$n tells you 'I'm sorry, you did not give me enough to change.'", victim, None, ch,
                                 merc.TO_VICT)
                ch.reply = victim
                victim.do_give("%d %s %s" % (amount, "silver" if silver else "gold", ch.name))
            elif victim.can_see(ch):
                victim.do_give("%d %s %s" % (change, "gold" if silver else "silver", ch.name))
                if silver:
                    victim.do_give("%d silver %s" % ((95 * amount / 100 - change * 100), ch.name))
                act("$n tells you 'Thank you, come again.'", victim, None, ch, merc.TO_VICT)
                ch.reply = victim
        return
    obj = ch.get_item_carry(arg1, ch)
    if not obj:
        ch.send("You do not have that item.\n")
        return
    if obj.wear_loc != merc.WEAR_NONE:
        ch.send("You must remove it first.\n")
        return
    victim = ch.get_char_room(arg2)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.is_npc() and victim.pIndexData.pShop is not None:
        act("$N tells you 'Sorry, you'll have to sell that.'", ch, None, victim, merc.TO_CHAR)
        ch.reply = victim
        return
    if not ch.can_drop_item(obj):
        ch.send("You can't let go of it.\n")
        return
    if victim.carry_number + obj.get_number() > victim.can_carry_n():
        act("$N has $S hands full.", ch, None, victim, merc.TO_CHAR)
        return
    if state_checks.get_carry_weight(victim) + obj.get_weight() > victim.can_carry_w():
        act("$N can't carry that much weight.", ch, None, victim, merc.TO_CHAR)
        return
    if not victim.can_see_item(obj):
        act("$N can't see it.", ch, None, victim, merc.TO_CHAR)
        return
    obj.from_environment()
    obj.to_environment(victim)
    act("$n gives $p to $N.", ch, obj, victim, merc.TO_NOTVICT)
    act("$n gives you $p.", ch, obj, victim, merc.TO_VICT)
    act("You give $p to $N.", ch, obj, victim, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('give', do_give, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
