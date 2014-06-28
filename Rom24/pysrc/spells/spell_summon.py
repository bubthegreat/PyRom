import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_summon(sn, level, ch, victim, target):
    victim = ch.get_char_world(handler_magic.target_name)
    if not victim \
            or victim == ch \
            or victim.in_room == None \
            or state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_SAFE) \
            or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_SAFE) \
            or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_PRIVATE) \
            or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_SOLITARY) \
            or state_checks.IS_SET(victim.in_room.room_flags, merc.ROOM_NO_RECALL) \
            or (state_checks.IS_NPC(victim) and state_checks.IS_SET(victim.act, merc.ACT_AGGRESSIVE)) \
            or victim.level >= level + 3 \
            or (not state_checks.IS_NPC(victim) and victim.level >= merc.LEVEL_IMMORTAL) \
            or victim.fighting != None \
            or (state_checks.IS_NPC(victim) and state_checks.IS_SET(victim.imm_flags, merc.IMM_SUMMON)) \
            or (state_checks.IS_NPC(victim) and victim.pIndexData.pShop != None) \
            or (not state_checks.IS_NPC(victim) and state_checks.IS_SET(victim.act, merc.PLR_NOSUMMON)) \
            or (state_checks.IS_NPC(victim) and handler_magic.saves_spell(level, victim, merc.DAM_OTHER)):
        ch.send("You failed.\n")
        return

    handler_game.act("$n disappears suddenly.", victim, None, None, merc.TO_ROOM)
    victim.from_room()
    victim.to_room(ch.in_room)
    handler_game.act("$n arrives suddenly.", victim, None, None, merc.TO_ROOM)
    handler_game.act("$n has summoned you! ", ch, None, victim, merc.TO_VICT)
    victim.do_look("auto")


const.register_spell(const.skill_type("summon",
                          {'mage': 24, 'cleric': 12, 'thief': 29, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_summon, merc.TAR_IGNORE, merc.POS_STANDING, None,
                          const.SLOT(40), 50, 12, "", "!Summon!", ""))