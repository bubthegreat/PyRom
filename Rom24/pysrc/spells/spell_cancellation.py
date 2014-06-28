import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_cancellation(sn, level, ch, victim, target):
    found = False
    level += 2
    if (not state_checks.IS_NPC(ch) and state_checks.IS_NPC(victim) and not (
        state_checks.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim)) \
            or (state_checks.IS_NPC(ch) and not state_checks.IS_NPC(victim)):
        ch.send("You failed, try dispel magic.\n")
        return
    # unlike dispel magic, the victim gets NO save */
    # begin running through the spells */
    spells = {'armor': None,
              'bless': None,
              'blindness': '$n is no longer blinded',
              'calm': '$n no longer looks so peaceful...',
              'change sex': '$n looks more like $mself again.',
              'charm person': '$n regains $s free will.',
              'chill touch': '$n looks warmer',
              'curse': None,
              'detect evil': None,
              'detect good': None,
              'detect hidden': None,
              'detect invis': None,
              'detect magic': None,
              'faerie fire': "$n's outline fades",
              'fly': '$n falls to the ground! ',
              'frenzy': "$n no longer looks so wild.",
              'giant strength': "$n no longer looks so mighty.",
              'haste': '$n is no longer moving so quickly',
              'infravision': None,
              'invis': '$n fades into existence.',
              'mass invis': '$n fades into existence',
              'pass door': None,
              'protection evil': None,
              'protection good': None,
              'sanctuary': "The white aura around $n's body vanishes.",
              'shield': 'The shield protecting $n vanishes',
              'sleep': None,
              'slow': '$n is no longer moving so slowly.',
              'stone skin': "$n's skin regains its normal texture.",
              'weaken': "$n looks stronger."}

    for k, v in spells.items():
        if handler_magic.check_dispel(level, victim, const.skill_table[k]):
            if v:
                handler_game.act(v, victim, None, None, merc.TO_ROOM)
            found = True

    if found:
        ch.send("Ok.\n")
    else:
        ch.send("Spell failed.\n")


const.register_spell(const.skill_type("cancellation",
                          {'mage': 18, 'cleric': 26, 'thief': 34, 'warrior': 34},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cancellation, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(507), 20, 12, "", "!cancellation!", "")
)