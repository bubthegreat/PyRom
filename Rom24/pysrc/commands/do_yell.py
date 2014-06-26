import merc
import interp
import nanny


def do_yell(ch, argument):
    if merc.IS_SET(ch.comm, merc.COMM_NOSHOUT):
        ch.send("You can't yell.\n")
        return
    if not argument:
        ch.send("Yell what?\n")
        return
    merc.act("You yell '$t'", ch, argument, None, merc.TO_CHAR)
    for d in merc.descriptor_list:
        if d.is_connected(nanny.con_playing) \
        and d.character != ch \
        and d.character.in_room != None \
        and d.character.in_room.area == ch.in_room.area \
        and not merc.IS_SET(d.character.comm, merc.COMM_QUIET):
            merc.act("$n yells '$t'", ch, argument, d.character, merc.TO_VICT)

interp.cmd_table['yell'] = interp.cmd_type('yell', do_yell, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)