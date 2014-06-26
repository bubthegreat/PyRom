import merc
import const
import interp
import handler


def do_ostat(self, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        ch.send("Stat what?\n")
        return
    obj = ch.get_obj_world(arg)
    if not obj:
        ch.send("Nothing like that in hell, earth, or heaven.\n")
        return

    ch.send("Name(s): %s\n" % obj.name )
    ch.send("Vnum: %d  Format: %s  Type: %s  Resets: %d\n" % (
        obj.pIndexData.vnum, "new" if obj.pIndexData.new_format else "old",
        obj.item_type, obj.pIndexData.reset_num ) )
    ch.send("Short description: %s\nLong description: %s\n" % (obj.short_descr, obj.description ))
    ch.send("Wear bits: %s\nExtra bits: %s\n" % (handler.wear_bit_name(obj.wear_flags),
                                                 handler.extra_bit_name( obj.extra_flags)))
    ch.send("Number: 1/%d  Weight: %d/%d/%d (10th pounds)\n" % ( obj.get_number(),
        obj.weight, obj.get_weight(),obj.true_weight() ) )
    ch.send("Level: %d  Cost: %d  Condition: %d  Timer: %d\n" % (obj.level, obj.cost, obj.condition, obj.timer ) )

    ch.send( "In room: %d  In object: %s  Carried by: %s  Wear_loc: %d\n" % (
        0 if not obj.in_room else obj.in_room.vnum,
        "(none)" if not obj.in_obj else obj.in_obj.short_descr,
        "(noone)" if not obj.carried_by else "someone" if not ch.can_see(obj.carried_by) else obj.carried_by.name,
        obj.wear_loc ) )
    ch.send("Values: %s\n" % [v for v in obj.value])
    # now give out vital statistics as per identify */

    if obj.item_type == merc.ITEM_SCROLL \
    or obj.item_type == merc.ITEM_POTION \
    or obj.item_type == merc.ITEM_PILL:
        ch.send( "Level %d spells of:", obj.value[0] )
        for value in obj.value:
            if value and value in const.skill_table:
                ch.send(" '%s'" % const.skill_table[value].name)

        ch.send(".\n")
    elif obj.item_type == merc.ITEM_WAND \
    or obj.item_type == merc.ITEM_STAFF:
        ch.send("Has %d(%d) charges of level %d" % (obj.value[1], obj.value[2], obj.value[0] ))
        ch.send(buf)

        if obj.value[3] and obj.value[3] in const.skill_table:
              ch.send(" '%s'" %  (const.skill_table[obj.value[3]].name) )
        ch.send(".\n")
    elif obj.item_type == merc.ITEM_DRINK_CON:
          ch.send("It holds %s-colored %s.\n" % (const.liq_table[obj.value[2]].liq_color,
                                                 const.liq_table[obj.value[2]].liq_name) )
    elif obj.item_type == merc.ITEM_WEAPON:
          ch.send("Weapon type is ")
          weapon_type = { merc.WEAPON_EXOTIC:"exotic", merc.WEAPON_SWORD:"sword",
                          merc.WEAPON_DAGGER:"dagger", merc.WEAPON_SPEAR:"spear/staff",
                          merc.WEAPON_MACE:"mace/club", merc.WEAPON_AXE:"axe",
                          merc.WEAPON_FLAIL:"flail", merc.WEAPON_WHIP:"whip",
                          merc.WEAPON_POLEARM: "polearm" }
          if obj.value[0] not in weapon_type:
              ch.send("unknown\n")
          else:
              ch.send(const.weapon_table[obj.value[0]] + "\n")
          if obj.pIndexData.new_format:
              ch.send("Damage is %dd%d (average %d)\n" % (obj.value[1],obj.value[2], (1 + obj.value[2]) * obj.value[1] // 2))
          else:
              ch.send("Damage is %d to %d (average %d)\n" % ( obj.value[1], obj.value[2], ( obj.value[1] + obj.value[2] ) // 2 ) )
          ch.send("Damage noun is %s.\n" % (const.attack_table[obj.value[3]].noun if obj.value[3] in const.attack_table else "undefined") )
          if obj.value[4] > 0:  # weapon flags */
              ch.send("Weapons flags: %s\n" % handler.weapon_bit_name(obj.value[4]))
    elif obj.item_type == merc.ITEM_ARMOR:
        ch.send( "Armor class is %d pierce, %d bash, %d slash, and %d vs. magic\n" % (
              obj.value[0], obj.value[1], obj.value[2], obj.value[3] ) )
    elif obj.item_type == merc.ITEM_CONTAINER:
        ch.send("Capacity: %d#  Maximum weight: %d#  flags: %s\n" % (obj.value[0], obj.value[3], handler.cont_bit_name(obj.value[1])))
        if obj.value[4] != 100:
            ch.send("Weight multiplier: %d%%\n" % obj.value[4])

    if obj.extra_descr or obj.pIndexData.extra_descr:
        ch.send("Extra description keywords: '")
        extra_descr = obj.extra_descr
        extra_descr.extend(obj.pIndexData.extra_descr)
        for ed in extra_descr:
            ch.send(ed.keyword)
            ch.send(" ")
    affected = obj.affected
    if not obj.enchanted:
        affected.extend(obj.pIndexData.affected)
    for paf in affected:
        ch.send("Affects %s by %d, level %d" % (handler.affect_loc_name(paf.location), paf.modifier,paf.level))
        if paf.duration > -1:
            ch.send(", %d hours.\n" % paf.duration)
        else:
            ch.send(".\n")
        if paf.bitvector:
            if paf.where == TO_AFFECTS:
                ch.send("Adds %s affect.\n" % handler.affect_bit_name(paf.bitvector))
            elif paf.where == TO_WEAPON:
                ch.send("Adds %s weapon flags.\n" % handler.weapon_bit_name(paf.bitvector))
            elif paf.where == TO_OBJECT:
                ch.send("Adds %s object flag.\n" % handler.extra_bit_name(paf.bitvector))
            elif paf.where == TO_IMMUNE:
                ch.send("Adds immunity to %s.\n" % handler.imm_bit_name(paf.bitvector))
            elif paf.where == TO_RESIST:
                ch.send("Adds resistance to %s.\n" % handler.imm_bit_name(paf.bitvector))
            elif paf.where == TO_VULN:
                ch.send("Adds vulnerability to %s.\n" % handler.imm_bit_name(paf.bitvector))
            else:
                ch.send("Unknown bit %d: %d\n" % paf.where,paf.bitvector)

interp.cmd_table['ostat'] = interp.cmd_type('ostat', do_ostat, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)