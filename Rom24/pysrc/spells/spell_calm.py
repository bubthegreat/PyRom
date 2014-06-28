



# RT calm spell stops all fighting in the room */
import random
import const
import fight
import handler_game
import merc
import state_checks


def spell_calm(sn, level, ch, victim, target):
    # get sum of all mobile levels in the room */
    count = 0
    mlevel = 0
    high_level = 0
    for vch in ch.in_room.people:
        if vch.position == merc.POS_FIGHTING:
            count = count + 1
        if state_checks.IS_NPC(vch):
            mlevel += vch.level
        else:
            mlevel += vch.level // 2
        high_level = max(high_level, vch.level)

    # compute chance of stopping combat */
    chance = 4 * level - high_level + 2 * count

    if state_checks.IS_IMMORTAL(ch):  # always works */
        mlevel = 0

    if random.randint(0, chance) >= mlevel:  # hard to stop large fights */
        for vch in ch.in_room.people:
            if state_checks.IS_NPC(vch) and (state_checks.IS_SET(vch.imm_flags, merc.IMM_MAGIC) \
                                        or state_checks.IS_SET(vch.act, merc.ACT_UNDEAD)):
                return

            if state_checks.IS_AFFECTED(vch, merc.AFF_CALM) or state_checks.IS_AFFECTED(vch, merc.AFF_BERSERK) \
                    or state_checks.is_affected(vch, const.skill_table['frenzy']):
                return

            vch.send("A wave of calm passes over you.\n")

            if vch.fighting or vch.position == merc.POS_FIGHTING:
                fight.stop_fighting(vch, False)
            af = handler_game.AFFECT_DATA()
            af.where = merc.TO_AFFECTS
            af.type = sn
            af.level = level
            af.duration = level // 4
            af.location = merc.APPLY_HITROLL
            if not state_checks.IS_NPC(vch):
                af.modifier = -5
            else:
                af.modifier = -2
            af.bitvector = merc.AFF_CALM
            vch.affect_add(af)

            af.location = merc.APPLY_DAMROLL
            vch.affect_add(af)


const.register_spell(const.skill_type("calm",
                          {'mage': 48, 'cleric': 16, 'thief': 50, 'warrior': 20},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_calm, merc.TAR_IGNORE, merc.POS_FIGHTING, None, const.SLOT(509),
                          30, 12, "", "You have lost your peace of mind.", ""))