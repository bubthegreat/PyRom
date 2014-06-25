"""
/***************************************************************************
 *  Original Diku Mud copyright (C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright (C) 1992, 1993 by Michael          *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

/***************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""

import time
import random
import collections


#Global MAXes
MAX_TRADE = 5
MAX_GUILDROOMS = 2
MAX_STATS = 5
MAX_SKILL = 150
MAX_GROUP = 30
MAX_LEVEL = 60
MAX_ALIAS = 10
LEVEL_HERO = (MAX_LEVEL - 9)
LEVEL_IMMORTAL = (MAX_LEVEL - 8)

ML=MAX_LEVEL   # implementor */
L1=MAX_LEVEL - 1   # creator */
L2=MAX_LEVEL - 2   # supreme being */
L3=MAX_LEVEL - 3   # deity */
L4=MAX_LEVEL - 4   # god */
L5=MAX_LEVEL - 5   # immortal */
L6=MAX_LEVEL - 6   # demigod */
L7=MAX_LEVEL - 7   # angel */
L8=MAX_LEVEL - 8   # avatar */
IM=LEVEL_IMMORTAL  # avatar */
HE=LEVEL_HERO  # hero */

#Global Classes
class CHAR_DATA(object):
    def __init__(self):
        from const import race_table
        from tables import clan_table
        self.master = None
        self.leader = None
        self.fighting = None
        self.reply = None
        self.pet = None
        self.memory = None
        self.spec_fun = None
        self.pIndexData = None
        self.desc = None
        self.affected = []
        self.pnote = None
        self.carrying = []
        self.on = None
        self.in_room = None
        self.was_in_room = None
        self.zone = None
        self.pcdata = None
        self.gen_data = None
        self.valid = False
        self.name = ""
        self.id = 0
        self.version = 5
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.prompt = "<%hhp %mm %vmv>"
        self.prefix = ""
        self.group = 0
        self.clan = clan_table[""]
        self.sex = 0
        self.guild = 0
        self.race = 0
        self.level = 0
        self.trust = 0
        self.played = 0
        self.lines = 22
        self.logon = 0
        self.timer = 0
        self.wait = 0
        self.daze = 0
        self.hit = 20
        self.max_hit = 20
        self.mana = 100
        self.max_mana = 100
        self.move = 100
        self.max_move = 100
        self.gold = 0
        self.silver =0
        self.exp = 0
        self.act = 0
        self.comm = 0
        self.wiznet = 0
        self.imm_flags = 0
        self.res_flags = 0
        self.vuln_flags = 0
        self.invis_level = 0
        self.incog_level = 0
        self.affected_by = 0
        self.position = 0
        self.practice = 0
        self.train = 0
        self.carry_weight = 0
        self.carry_number = 0
        self.saving_throw = 0
        self.alignment = 0
        self.hitroll = 0
        self.damroll = 0
        self.armor = [100, 100, 100, 100]
        self.wimpy = 0
    # stats */
        self.perm_stat = [13 for x in range(MAX_STATS)]
        self.mod_stat = [0 for x in range(MAX_STATS)]
    # parts stuff */
        self.form = 0
        self.parts = 0
        self.size = 0
        self.material = ""
    # mobile stuff */
        self.off_flags = 0
        self.damage = [0,0,0]
        self.dam_type = 17
        self.start_pos = 0
        self.default_pos = 0
        self.race = race_table['human']
        self.act = PLR_NOSUMMON
        self.comm = COMM_COMBINE | COMM_PROMPT
    def __repr__(self):
        return self.name
    def send(self, str):
        pass

class PC_DATA:
    def __init__(self):
        self.buffer = None
        self.valid = False
        self.pwd = ""
        self.bamfin = ""
        self.bamfout = ""
        self.title = ""
        self.last_note = 0
        self.last_idea = 0
        self.last_penalty = 0
        self.last_news = 0
        self.last_changes = 0
        self.perm_hit = 0
        self.perm_mana = 0
        self.perm_move = 0
        self.true_sex = 0
        self.last_level = 0
        self.condition = [48,48,48,0]
        self.learned = {}
        self.group_known = {}
        self.points = 0
        self.confirm_delete = False
        self.alias = {}

class GEN_DATA:
    def __init__(self):    
        self.valid = False
        self.skill_chosen = {}
        self.group_chosen = {}
        self.points_chosen = 0


class AREA_DATA:
    def __init__(self):    
        self.reset_list = []
        self.file_name = ""
        self.name = ""
        self.credits = ""
        self.age = 15
        self.nplayer = 0
        self.low_range = 0
        self.high_range = 0
        self.min_vnum = 0
        self.max_vnum = 0
        self.empty = False

    def __repr__(self):
        return "<%s(%s): %d-%d>" % (self.name, self.file_name, self.min_vnum, self.max_vnum)

class HELP_DATA:
    def __init__(self):    
        self.level = 0
        self.keyword = ""
        self.text = ""

    def __repr__(self):
        return "<%s:%d>" % (self.keyword, self.level)

class MOB_INDEX_DATA:
    def __init__(self):    
        self.spec_fun = None
        self.pShop = None
        self.vnum = 0
        self.group = 0
        self.new_format = True
        self.count = 0
        self.killed = 0
        self.player_name = ""
        self.short_descr = ""
        self.long_descr = ""
        self.description = ""
        self.act = 0
        self.affected_by = 0
        self.alignment = 0
        self.level = 0
        self.hitroll = 0
        self.hit = [0, 0, 0]
        self.mana = [0, 0, 0]
        self.damage = [0, 0, 0]
        self.ac = [0, 0, 0, 0]
        self.dam_type = 0
        self.off_flags = 0
        self.imm_flags = 0
        self.res_flags = 0
        self.vuln_flags = 0
        self.start_pos = 0
        self.default_pos = 0
        self.sex = 0
        self.race = 0
        self.wealth = 0
        self.form = 0
        self.parts = 0
        self.size = 0
        self.material = ""
    def __repr__(self):
        return "<MobIndex: %s:%s>" % ( self.short_descr, self.vnum )

class OBJ_INDEX_DATA:
    def __init__(self):
        self.extra_descr = []
        self.affected = []
        self.new_format = True
        self.name = ""
        self.short_descr = ""
        self.description = ""
        self.vnum = 0
        self.reset_num = 0
        self.material = ""
        self.item_type = 0
        self.extra_flags = 0
        self.wear_flags = 0
        self.level = 0
        self.condition = 0
        self.count = 0
        self.weight = 0
        self.cost = 0
        self.value = [0, 0, 0, 0, 0]
    def __repr__(self):
        return "<ObjIndex: %s:%d>" % (self.short_descr, self.vnum)    

# * One object.

class OBJ_DATA:
    def __init__(self):    
        self.contains = []
        self.in_obj = None
        self.on = None
        self.carried_by = None
        self.extra_descr = []
        self.affected = []
        self.pIndexData = None
        self.in_room = None
        self.valid = False
        self.enchanted = False
        self.owner = ""
        self.name = ""
        self.short_descr =""
        self.description =""
        self.item_type = 0
        self.extra_flags = 0
        self.wear_flags = 0
        self.wear_loc = 0
        self.weight = 0
        self.cost = 0
        self.level = 0
        self.condition = 0
        self.material = ""
        self.timer = 0
        self.value = [0 for x in range(5)]

class ROOM_INDEX_DATA:
    def __init__(self):    
        self.people = []
        self.contents = []
        self.extra_descr = []
        self.area = None
        self.exit = [None, None, None, None, None, None]
        self.old_exit = [None, None, None, None, None, None]
        self.name = ""
        self.description = ""
        self.owner = ""
        self.vnum = 0
        self.room_flags = 0
        self.light = 0
        self.sector_type = 0
        self.heal_rate = 0
        self.mana_rate = 0
        self.clan = 0
    def __repr__(self):
        return "<RoomIndex: %d" % (self.vnum)

class EXTRA_DESCR_DATA:
    def __init__(self):    
        self.keyword = ""# Keyword in look/examine
        self.description = ""

class EXIT_DATA:
    def __init__(self):    
        self.to_room =None
        self.exit_info = 0
        self.key = 0
        self.keyword = ""
        self.description = ""

class RESET_DATA:
    def __init__(self):    
        self.command = ""
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0
        self.arg4 = 0

class SHOP_DATA:
    def __init__(self):    
        self.keeper = 0
        self.buy_type = {}
        self.profit_buy = 0
        self.profit_sell = 0
        self.open_hour = 0
        self.close_hour = 0

class SOCIAL_DATA:
    def __init__(self):    
        self.name = ""
        self.char_no_arg = ""
        self.others_no_arg = ""
        self.char_found = ""
        self.others_found = ""
        self.vict_found = ""
        self.char_not_found = ""
        self.char_auto = ""
        self.others_auto = ""

# An affect.
class AFFECT_DATA:
    def __init__(self):    
        self.valid = True
        self.where = 0
        self.type = 0
        self.level = 0
        self.duration = 0
        self.location = 0
        self.modifier = 0
        self.bitvector = 0

#Global Lists
descriptor_list = []
player_list = []
char_list = []
mob_index_hash = {}
obj_index_hash = {}
object_list = []
room_index_hash = {}
area_list = []
help_list = []
greeting_list = []
reset_list = []
shop_list = []
social_list = []


#Global Constants
PULSE_PER_SECOND = 12
PULSE_VIOLENCE = (1 * PULSE_PER_SECOND)
PULSE_MOBILE = (4 * PULSE_PER_SECOND)
PULSE_MUSIC = (6 * PULSE_PER_SECOND)
PULSE_TICK = (60 * PULSE_PER_SECOND)
PULSE_AREA = (120 * PULSE_PER_SECOND)


# * Time and weather stuff.
SUN_DARK = 0
SUN_RISE = 1
SUN_LIGHT = 2
SUN_SET = 3

SKY_CLOUDLESS = 0
SKY_CLOUDY = 1
SKY_RAINING = 2
SKY_LIGHTNING = 3

class time_info_data:
    def __init__(self):
        self.hour = 0
        self.day = 0
        self.month = 0
        self.year = 0


class weather_data:
    def __init__(self):
        self.mmhg = 0
        self.change = 0
        self.sky = 0
        self.sunlight = 0

time_info = time_info_data()
weather_info = weather_data()

#Stats
STAT_STR = 0
STAT_INT = 1
STAT_WIS = 2
STAT_DEX = 3
STAT_CON = 4

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_UP = 4
DIR_DOWN = 5


#Item types
ITEM_LIGHT = 'light'
ITEM_SCROLL = 'scroll'
ITEM_WAND ='wand'
ITEM_STAFF = 'staff'
ITEM_WEAPON = 'weapon'
ITEM_TREASURE = 'treasure'
ITEM_ARMOR = 'armor'
ITEM_POTION = 'potion'
ITEM_CLOTHING = 'clothing'
ITEM_FURNITURE = 'furniture'
ITEM_TRASH = 'trash'
ITEM_CONTAINER = 'container'
ITEM_DRINK_CON = 'drink'
ITEM_KEY = 'key'
ITEM_FOOD = 'food'
ITEM_MONEY = 'money'
ITEM_BOAT = 'boat'
ITEM_CORPSE_NPC = 'npc_corpse'
ITEM_CORPSE_PC = 'pc_corpse'
ITEM_FOUNTAIN = 'fountain'
ITEM_PILL = 'pill'
ITEM_PROTECT = 'protect'
ITEM_MAP = 'map'
ITEM_PORTAL = 'portal'
ITEM_WARP_STONE = 'warp_stone'
ITEM_ROOM_KEY = 'room_key'
ITEM_GEM = 'gem'
ITEM_JEWELRY = 'jewelry'
ITEM_JUKEBOX = 'jukebox'



#Sexes
SEX_NEUTRAL = 0
SEX_MALE = 1
SEX_FEMALE = 2

#Sizes
SIZE_TINY = 0
SIZE_SMALL = 1
SIZE_MEDIUM = 2
SIZE_LARGE = 3
SIZE_HUGE = 4
SIZE_GIANT = 5
size_table = ["tiny",  "small", "medium", "large", "huge", "giant" ]

# AC types */
AC_PIERCE = 0
AC_BASH = 1
AC_SLASH = 2
AC_EXOTIC = 3

DICE_NUMBER = 0
DICE_TYPE = 1
DICE_BONUS = 2

#  Target types.
 
TAR_IGNORE = 0
TAR_CHAR_OFFENSIVE = 1
TAR_CHAR_DEFENSIVE = 2
TAR_CHAR_SELF = 3
TAR_OBJ_INV = 4
TAR_OBJ_CHAR_DEF = 5
TAR_OBJ_CHAR_OFF = 6

TARGET_CHAR = 0
TARGET_OBJ = 1
TARGET_ROOM = 2
TARGET_NONE = 3

#Positions
POS_DEAD = 0
POS_MORTAL = 1
POS_INCAP = 2
POS_STUNNED = 3
POS_SLEEPING = 4
POS_RESTING = 5
POS_SITTING = 6
POS_FIGHTING = 7
POS_STANDING = 8


# * Sector types.
# * Used in #ROOMS.

SECT_INSIDE = 0
SECT_CITY = 1
SECT_FIELD = 2
SECT_FOREST = 3
SECT_HILLS = 4
SECT_MOUNTAIN = 5
SECT_WATER_SWIM = 6
SECT_WATER_NOSWIM = 7
SECT_UNUSED = 8
SECT_AIR = 9
SECT_DESERT = 10
SECT_MAX = 11

# TO types for act.

TO_ROOM = 0
TO_NOTVICT = 1
TO_VICT = 2
TO_CHAR = 3
TO_ALL = 4

# damage classes
DAM_NONE = 0
DAM_BASH = 1
DAM_PIERCE = 2
DAM_SLASH = 3
DAM_FIRE = 4
DAM_COLD = 5
DAM_LIGHTNING = 6
DAM_ACID = 7
DAM_POISON = 8
DAM_NEGATIVE = 9
DAM_HOLY = 10
DAM_ENERGY = 11
DAM_MENTAL = 12
DAM_DISEASE = 13
DAM_DROWNING = 14
DAM_LIGHT = 15
DAM_OTHER = 16
DAM_HARM = 17
DAM_CHARM = 18
DAM_SOUND = 19

LOG_NORMAL = 0
LOG_ALWAYS = 1
LOG_NEVER = 2

WEAPON_EXOTIC = 0
WEAPON_SWORD = 1
WEAPON_DAGGER = 2
WEAPON_SPEAR = 3
WEAPON_MACE = 4
WEAPON_AXE = 5
WEAPON_FLAIL = 6
WEAPON_WHIP = 7
WEAPON_POLEARM = 8


# * Equpiment wear locations.
# * Used in #RESETS.

WEAR_NONE = -1
WEAR_LIGHT = 0
WEAR_FINGER_L = 1
WEAR_FINGER_R = 2
WEAR_NECK_1 = 3
WEAR_NECK_2 = 4
WEAR_BODY = 5
WEAR_HEAD = 6
WEAR_LEGS = 7
WEAR_FEET = 8
WEAR_HANDS = 9
WEAR_ARMS = 10
WEAR_SHIELD = 11
WEAR_ABOUT = 12
WEAR_WAIST = 13
WEAR_WRIST_L = 14
WEAR_WRIST_R = 15
WEAR_WIELD = 16
WEAR_HOLD = 17
WEAR_FLOAT = 18
MAX_WEAR = 19


# * Conditions.

COND_DRUNK = 0
COND_FULL = 1
COND_THIRST = 2
COND_HUNGER = 3

#/* where definitions */
TO_AFFECTS = 0
TO_OBJECT = 1
TO_IMMUNE = 2
TO_RESIST = 3
TO_VULN = 4
TO_WEAPON = 5

# return values for check_imm */
IS_NORMAL = 0
IS_IMMUNE = 1
IS_RESISTANT = 2
IS_VULNERABLE = 3

#Item constants

OBJ_VNUM_SILVER_ONE = 1
OBJ_VNUM_GOLD_ONE = 2
OBJ_VNUM_GOLD_SOME = 3
OBJ_VNUM_SILVER_SOME = 4
OBJ_VNUM_COINS = 5
OBJ_VNUM_CORPSE_NPC = 10
OBJ_VNUM_CORPSE_PC = 11
OBJ_VNUM_SEVERED_HEAD = 12
OBJ_VNUM_TORN_HEART = 13
OBJ_VNUM_SLICED_ARM = 14
OBJ_VNUM_SLICED_LEG = 15
OBJ_VNUM_GUTS = 16
OBJ_VNUM_BRAINS = 17
OBJ_VNUM_MUSHROOM = 20
OBJ_VNUM_LIGHT_BALL = 21
OBJ_VNUM_SPRING = 22
OBJ_VNUM_DISC = 23
OBJ_VNUM_PORTAL = 25
OBJ_VNUM_ROSE = 1001
OBJ_VNUM_PIT = 3010
OBJ_VNUM_SCHOOL_MACE = 3700
OBJ_VNUM_SCHOOL_DAGGER = 3701
OBJ_VNUM_SCHOOL_SWORD = 3702
OBJ_VNUM_SCHOOL_SPEAR = 3717
OBJ_VNUM_SCHOOL_STAFF = 3718
OBJ_VNUM_SCHOOL_AXE = 3719
OBJ_VNUM_SCHOOL_FLAIL = 3720
OBJ_VNUM_SCHOOL_WHIP = 3721
OBJ_VNUM_SCHOOL_POLEARM = 3722
OBJ_VNUM_SCHOOL_VEST = 3703
OBJ_VNUM_SCHOOL_SHIELD = 3704
OBJ_VNUM_SCHOOL_BANNER = 3716
OBJ_VNUM_MAP = 3162
OBJ_VNUM_WHISTLE = 2116

# * Well known room virtual numbers.
# * Defined in #ROOMS.
ROOM_VNUM_LIMBO = 2
ROOM_VNUM_CHAT = 1200
ROOM_VNUM_TEMPLE = 3001
ROOM_VNUM_ALTAR = 3054
ROOM_VNUM_SCHOOL = 3700
ROOM_VNUM_BALANCE = 4500
ROOM_VNUM_CIRCLE = 4400
ROOM_VNUM_DEMISE = 4201
ROOM_VNUM_HONOR = 4300

#* but may be arbitrary beyond that.
TYPE_UNDEFINED = -1
TYPE_HIT = 1000

def IS_SET(flag, bit):
    return flag & bit
def SET_BIT(var, bit):
    return var | bit
def REMOVE_BIT(var, bit):
    return var & ~(bit)

A = 1
B = 1 << 1
C = 1 << 2
D = 1 << 3
E = 1 << 4
F = 1 << 5
G = 1 << 6
H = 1 << 7
I = 1 << 8
J = 1 << 9
K = 1 << 10
L = 1 << 11
M = 1 << 12
N = 1 << 13
O = 1 << 14
P = 1 << 15
Q = 1 << 16
R = 1 << 17
S = 1 << 18
T = 1 << 19
U = 1 << 20
V = 1 << 21
W = 1 << 22
X = 1 << 23
Y = 1 << 24
W = 1 << 25
Z = 1 << 26
aa = 1 << 27
bb = 1 << 28
cc = 1 << 29
dd = 1 << 30
ee = 1 << 31
ff = 1 << 32
gg = 1 << 33
hh = 1 << 34
ii = 1 << 35
jj = 1 << 36
kk = 1 << 37
ll = 1 << 38
mm = 1 << 39
nn = 1 << 40
oo = 1 << 41
pp = 1 << 42
qq = 1 << 43
rr = 1 << 44
ss = 1 << 45
tt = 1 << 46
uu = 1 << 47
vv = 1 << 48
ww = 1 << 49
xx = 1 << 50
yy = 1 << 51
zz = 1 << 52



#  ACT bits for mobs.
#  Used in #MOBILES.

ACT_IS_NPC = A  # Auto set for mobs    */
ACT_SENTINEL = B #  Stays in one room    */
ACT_SCAVENGER = C  # Picks up objects */
ACT_AGGRESSIVE = F   # Attacks PC's     */
ACT_STAY_AREA = G    # Won't leave area */
ACT_WIMPY = H
ACT_PET = I     # Auto set for pets    */
ACT_TRAIN = J     # Can train PC's   */
ACT_PRACTICE = K     # Can practice PC's    */
ACT_UNDEAD = O 
ACT_CLERIC = Q
ACT_MAGE = R
ACT_THIEF = S
ACT_WARRIOR = T
ACT_NOALIGN = U
ACT_NOPURGE = V
ACT_OUTDOORS = W
ACT_INDOORS = Y
ACT_IS_HEALER = aa
ACT_GAIN = bb
ACT_UPDATE_ALWAYS = cc
ACT_IS_CHANGER = dd

OFF_AREA_ATTACK = A
OFF_BACKSTAB = B
OFF_BASH = C
OFF_BERSERK = D
OFF_DISARM = E
OFF_DODGE = F
OFF_FADE = G
OFF_FAST = H
OFF_KICK = I
OFF_KICK_DIRT = J
OFF_PARRY = K
OFF_RESCUE = L
OFF_TAIL = M
OFF_TRIP = N
OFF_CRUSH = O
ASSIST_ALL = P
ASSIST_ALIGN = Q
ASSIST_RACE = R
ASSIST_PLAYERS = S
ASSIST_GUARD = T
ASSIST_VNUM = U

IMM_SUMMON = A
IMM_CHARM = B
IMM_MAGIC = C
IMM_WEAPON = D
IMM_BASH = E
IMM_PIERCE = F
IMM_SLASH = G
IMM_FIRE = H
IMM_COLD = I
IMM_LIGHTNING = J
IMM_ACID = K
IMM_POISON = L
IMM_NEGATIVE = M
IMM_HOLY = N
IMM_ENERGY = O
IMM_MENTAL = P
IMM_DISEASE = Q
IMM_DROWNING = R
IMM_LIGHT = S
IMM_SOUND = T
IMM_WOOD = X
IMM_SILVER = Y
IMM_IRON = Z
 
# RES bits for mobs */
RES_SUMMON = A
RES_CHARM = B
RES_MAGIC = C
RES_WEAPON = D
RES_BASH = E
RES_PIERCE = F
RES_SLASH = G
RES_FIRE = H
RES_COLD = I
RES_LIGHTNING = J
RES_ACID = K
RES_POISON = L
RES_NEGATIVE = M
RES_HOLY = N
RES_ENERGY = O
RES_MENTAL = P
RES_DISEASE = Q
RES_DROWNING = R
RES_LIGHT = S
RES_SOUND = T
RES_WOOD = X
RES_SILVER = Y
RES_IRON = Z
 
# VULN bits for mobs */
VULN_SUMMON = A
VULN_CHARM = B
VULN_MAGIC = C
VULN_WEAPON = D
VULN_BASH = E
VULN_PIERCE = F
VULN_SLASH = G
VULN_FIRE = H
VULN_COLD = I
VULN_LIGHTNING = J
VULN_ACID = K
VULN_POISON = L
VULN_NEGATIVE = M
VULN_HOLY = N
VULN_ENERGY = O
VULN_MENTAL = P
VULN_DISEASE = Q
VULN_DROWNING = R
VULN_LIGHT = S
VULN_SOUND = T
VULN_WOOD = X
VULN_SILVER = Y
VULN_IRON = Z
 
# body form */
FORM_EDIBLE = A
FORM_POISON = B
FORM_MAGICAL = C
FORM_INSTANT_DECAY = D
FORM_OTHER = E  # defined by material bit */
 
# actual form */
FORM_ANIMAL = G
FORM_SENTIENT = H
FORM_UNDEAD = I
FORM_CONSTRUCT = J
FORM_MIST = K
FORM_INTANGIBLE = L
 
FORM_BIPED = M
FORM_CENTAUR = N
FORM_INSECT = O
FORM_SPIDER = P
FORM_CRUSTACEAN = Q
FORM_WORM = R
FORM_BLOB = S
 
FORM_MAMMAL = V
FORM_BIRD = W
FORM_REPTILE = X
FORM_SNAKE = Y
FORM_DRAGON = Z
FORM_AMPHIBIAN = aa
FORM_FISH = bb
FORM_COLD_BLOOD = cc    
 
# body parts */
PART_HEAD = A
PART_ARMS = B
PART_LEGS = C
PART_HEART = D
PART_BRAINS = E
PART_GUTS = F
PART_HANDS = G
PART_FEET = H
PART_FINGERS = I
PART_EAR = J
PART_EYE = K
PART_LONG_TONGUE = L
PART_EYESTALKS = M
PART_TENTACLES = N
PART_FINS = O
PART_WINGS = P
PART_TAIL = Q
# for combat */
PART_CLAWS = U
PART_FANGS = V
PART_HORNS = W
PART_SCALES = X
PART_TUSKS = Y


# Bits for 'affected_by'.
# Used in #MOBILES.

AFF_BLIND = A
AFF_INVISIBLE = B
AFF_DETECT_EVIL = C
AFF_DETECT_INVIS = D
AFF_DETECT_MAGIC = E
AFF_DETECT_HIDDEN = F
AFF_DETECT_GOOD = G
AFF_SANCTUARY = H
AFF_FAERIE_FIRE = I
AFF_INFRARED = J
AFF_CURSE = K
AFF_UNUSED_FLAG = L # unused */
AFF_POISON = M
AFF_PROTECT_EVIL = N
AFF_PROTECT_GOOD = O
AFF_SNEAK = P
AFF_HIDE = Q
AFF_SLEEP = R
AFF_CHARM = S
AFF_FLYING = T
AFF_PASS_DOOR = U
AFF_HASTE = V
AFF_CALM = W
AFF_PLAGUE = X
AFF_WEAKEN = Y
AFF_DARK_VISION = Z
AFF_BERSERK = aa
AFF_SWIM = bb
AFF_REGENERATION = cc
AFF_SLOW = dd


# Extra flags.
# Used in #OBJECTS.

ITEM_GLOW = A
ITEM_HUM = B
ITEM_DARK = C
ITEM_LOCK = D
ITEM_EVIL = E
ITEM_INVIS = F
ITEM_MAGIC = G
ITEM_NODROP = H
ITEM_BLESS = I
ITEM_ANTI_GOOD = J
ITEM_ANTI_EVIL = K
ITEM_ANTI_NEUTRAL = L
ITEM_NOREMOVE = M
ITEM_INVENTORY = N
ITEM_NOPURGE = O
ITEM_ROT_DEATH = P
ITEM_VIS_DEATH = Q
ITEM_NONMETAL = S
ITEM_NOLOCATE = T
ITEM_MELT_DROP = U
ITEM_HAD_TIMER = V
ITEM_SELL_EXTRACT = W
ITEM_BURN_PROOF = Y
ITEM_NOUNCURSE = Z



# Wear flags.
# Used in #OBJECTS.

ITEM_TAKE = A
ITEM_WEAR_FINGER = B
ITEM_WEAR_NECK = C
ITEM_WEAR_BODY = D
ITEM_WEAR_HEAD = E
ITEM_WEAR_LEGS = F
ITEM_WEAR_FEET = G
ITEM_WEAR_HANDS = H
ITEM_WEAR_ARMS = I
ITEM_WEAR_SHIELD = J
ITEM_WEAR_ABOUT = K
ITEM_WEAR_WAIST = L
ITEM_WEAR_WRIST = M
ITEM_WIELD = N
ITEM_HOLD = O
ITEM_NO_SAC = P
ITEM_WEAR_FLOAT = Q


# weapon types */
WEAPON_FLAMING = A
WEAPON_FROST = B
WEAPON_VAMPIRIC = C
WEAPON_SHARP = D
WEAPON_VORPAL = E
WEAPON_TWO_HANDS = F
WEAPON_SHOCKING = G
WEAPON_POISON = H

# gate flags */
GATE_NORMAL_EXIT = A
GATE_NOCURSE = B
GATE_GOWITH = C
GATE_BUGGY = D
GATE_RANDOM = E

# furniture flags */
STAND_AT = A
STAND_ON = B
STAND_IN = C
SIT_AT = D
SIT_ON = E
SIT_IN = F
REST_AT = G
REST_ON = H
REST_IN = I
SLEEP_AT = J
SLEEP_ON = K
SLEEP_IN = L
PUT_AT = M
PUT_ON = N
PUT_IN = O
PUT_INSIDE = P


# * Apply types (for affects).
# * Used in #OBJECTS.
APPLY_NONE = 0
APPLY_STR = 1
APPLY_DEX = 2
APPLY_INT = 3
APPLY_WIS = 4
APPLY_CON = 5
APPLY_SEX = 6
APPLY_CLASS = 7
APPLY_LEVEL = 8
APPLY_AGE = 9
APPLY_HEIGHT = 10
APPLY_WEIGHT = 11
APPLY_MANA = 12
APPLY_HIT = 13
APPLY_MOVE = 14
APPLY_GOLD = 15
APPLY_EXP = 16
APPLY_AC = 17
APPLY_HITROLL = 18
APPLY_DAMROLL = 19
APPLY_SAVES = 20
APPLY_SAVING_PARA = 20
APPLY_SAVING_ROD = 21
APPLY_SAVING_PETRI = 22
APPLY_SAVING_BREATH = 23
APPLY_SAVING_SPELL = 24
APPLY_SPELL_AFFECT = 25


# * Values for containers (value[1]).
# * Used in #OBJECTS.
CONT_CLOSEABLE = 1
CONT_PICKPROOF = 2
CONT_CLOSED = 4
CONT_LOCKED = 8
CONT_PUT_ON = 16

# Room flags.
# Used in #ROOMS.
ROOM_DARK = A
ROOM_NO_MOB = C
ROOM_INDOORS = D

ROOM_PRIVATE = J
ROOM_SAFE = K
ROOM_SOLITARY = L
ROOM_PET_SHOP = M
ROOM_NO_RECALL = N
ROOM_IMP_ONLY = O
ROOM_GODS_ONLY = P
ROOM_HEROES_ONLY = Q
ROOM_NEWBIES_ONLY = R
ROOM_LAW = S
ROOM_NOWHERE = T


# Exit flags.
# Used in #ROOMS.

EX_ISDOOR = A
EX_CLOSED = B
EX_LOCKED = C
EX_PICKPROOF = F
EX_NOPASS = G
EX_EASY = H
EX_HARD = I
EX_INFURIATING = J
EX_NOCLOSE = K
EX_NOLOCK = L


# ACT bits for players.

PLR_IS_NPC = A     # Don't EVER set.  */

# RT auto flags */
PLR_AUTOASSIST = C
PLR_AUTOEXIT = D
PLR_AUTOLOOT = E
PLR_AUTOSAC = F
PLR_AUTOGOLD = G
PLR_AUTOSPLIT = H

# RT personal flags */
PLR_HOLYLIGHT = N
PLR_CANLOOT = P
PLR_NOSUMMON = Q
PLR_NOFOLLOW = R
# 2 bits reserved, S-T */

# penalty flags */
PLR_PERMIT = U
PLR_LOG = W
PLR_DENY = X
PLR_FREEZE = Y
PLR_THIEF = Z
PLR_KILLER = aa
PLR_OMNI = bb

# RT comm flags -- may be used on both mobs and chars */
COMM_QUIET = A
COMM_DEAF = B
COMM_NOWIZ = C
COMM_NOAUCTION = D
COMM_NOGOSSIP = E
COMM_NOQUESTION = F
COMM_NOMUSIC = G
COMM_NOCLAN = H
COMM_NOQUOTE = I
COMM_SHOUTSOFF = J

# display flags */
COMM_COMPACT = L
COMM_BRIEF = M
COMM_PROMPT = N
COMM_COMBINE = O
COMM_TELNET_GA = P
COMM_SHOW_AFFECTS = Q
COMM_NOGRATS = R

# penalties */
COMM_NOEMOTE = T
COMM_NOSHOUT = U
COMM_NOTELL = V
COMM_NOCHANNELS = W 
COMM_SNOOP_PROOF = Y
COMM_AFK = Z

# WIZnet flags */
WIZ_ON = A
WIZ_TICKS = B
WIZ_LOGINS = C
WIZ_SITES = D
WIZ_LINKS = E
WIZ_DEATHS = F
WIZ_RESETS = G
WIZ_MOBDEATHS = H
WIZ_FLAGS = I
WIZ_PENALTIES = J
WIZ_SACCING = K
WIZ_LEVELS = L
WIZ_SECURE = M
WIZ_SWITCHES = N
WIZ_SNOOPS = O
WIZ_RESTORE = P
WIZ_LOAD = Q
WIZ_NEWBIE = R
WIZ_PREFIX = S
WIZ_SPAM = T

# memory settings */
MEM_CUSTOMER = A   
MEM_SELLER = B
MEM_HOSTILE = C
MEM_AFRAID = D

PAGELEN = 22

boot_time = time.time()
current_time = 0

#movement
dir_name = ["north", "east", "south", "west", "up", "down"]
rev_dir = [2, 3, 0, 1, 5, 4]
movement_loss = [1, 2, 2, 3, 4, 6, 4, 1, 6, 10, 6]

#Character Tracking
max_on = 0

where_name = ["<used as light>     ",
              "<worn on finger>    ",
              "<worn on finger>    ",
              "<worn around neck>  ",
              "<worn around neck>  ",
              "<worn on torso>     ",
              "<worn on head>      ",
              "<worn on legs>      ",
              "<worn on feet>      ",
              "<worn on hands>     ",
              "<worn on arms>      ",
              "<worn as shield>    ",
              "<worn about body>   ",
              "<worn about waist>  ",
              "<worn around wrist> ",
              "<worn around wrist> ",
              "<wielded>           ",
              "<held>              ",
              "<floating nearby>   "]


#utility functions
def name_lookup(dict, arg, key='name'):
    for i, n in dict.items():
        if n.__dict__[key] == arg:
            return i

def prefix_lookup(dict, arg):
    if not arg:
        return None
    results = [v for k,v in dict.items() if k.startswith(arg)]
    if results:
        return results[0]
    return None

def value_lookup(dict, arg):
    if not arg:
        return None
    for k,v in dict.items():
        if v == arg:
            return k
    return None

def mass_replace(str, dict):
    for k,v in dict.items():
        if v:
            str = str.replace(k,v)
    return str

def PERS(ch, looker):
    if not looker.can_see(ch):
        return "someone"
    if IS_NPC(ch):
        return ch.short_descr
    else:
        return ch.name

def OPERS(looker, obj):
    if not looker.can_see_obj(obj):
        return "something"
    return obj.short_descr

def IS_NPC(ch):
    return IS_SET(ch.act, ACT_IS_NPC)

def IS_IMMORTAL(ch):
    return ch.get_trust() >= LEVEL_IMMORTAL

def IS_HERO(ch):
    return ch.get_trust() >= LEVEL_HERO

def IS_TRUSTED(ch,level):
    return ch.get_trust() >= level
def is_affected( ch, sn ):
    return True if [paf for paf in ch.affected if paf.type == sn ][:1] else False

def IS_AFFECTED(ch, bit):
    return IS_SET(ch.affected_by, bit)

def GET_AGE(ch):
    return int((17 + (ch.played + time.time() - ch.logon)/72000))

def IS_GOOD(ch):
    return ch.alignment >= 350

def IS_EVIL(ch):
    return ch.alignment <= -350

def IS_NEUTRAL(ch):
    return not IS_GOOD(ch) and not IS_EVIL(ch)

def IS_AWAKE(ch):
    return ch.position > POS_SLEEPING

def GET_AC(ch,type):
    from const import dex_app
    return (ch.armor[type] + ( dex_app[ch.get_curr_stat(STAT_DEX)].defensive if IS_AWAKE(ch) else 0 ) )

def GET_HITROLL(ch):
    from const import str_app
    return ( ( ch.hitroll+str_app[ ch.get_curr_stat(STAT_STR)].tohit) )

def GET_DAMROLL(ch):
    from const import str_app
    return ( (ch.damroll+str_app[ch.get_curr_stat(STAT_STR)].todam) )

def IS_OUTSIDE(ch):
    return not IS_SET( ch.in_room.room_flags, ROOM_INDOORS )

def WAIT_STATE(ch, npulse):
    ch.wait = max(ch.wait, npulse)

def DAZE_STATE(ch, npulse):
    ch.daze = max(ch.daze, npulse)

def get_carry_weight(ch):
    return ch.carry_weight + (ch.silver/10 + (ch.gold * 2 / 5) )


 # Object macros.

def CAN_WEAR(obj, part):
    return IS_SET( obj.wear_flags,  part)

def IS_OBJ_STAT(obj, stat):
    return IS_SET(obj.extra_flags, stat)
def IS_WEAPON_STAT(obj,stat):
    return IS_SET(obj.value[4],stat)
def WEIGHT_MULT(obj):
    return obj.value[4] if obj.item_type is ITEM_CONTAINER else 100

def dice(number, size):
    return sum( [ random.randint(1, size ) for x in range(number) ])

def number_fuzzy(number):
    return random.randint(number-1, number+1)

def set_title(ch, title):
    if IS_NPC(ch):
        return
        
    nospace = ['.', ',', '!', '?']
    if title[0] in nospace:
        ch.pcdata.title = title
    else:
        ch.pcdata.title = ' ' + title

def read_forward(str, jump = 1):
    return str[jump:]

def read_letter(str):
    str = str.lstrip()
    return(str[1:], str[:1])

def read_word(str, lower = True):
    if not str:
        return ("", "")
    str = str.lstrip()
    word = str.split()[0]
    if word[0] == "'":
        word = str[:str.find("'", 1)+1]
    if lower:
        word = word.lower()
    str = str.lstrip()
    str = str[len(word)+1:]
    return (str, word.strip())

def read_int(str):
    if not str:
        return (None,None)
    str = str.lstrip()
    number = ""
    negative = False
    for c in str:
        if c == '-':
            negative = True
        elif c.isdigit():
            number += c
        else:
            break;

    str = str.lstrip()
    if not negative:
        str = str[len(number):]
        return (str, int(number) )
    else:
        str = str[len(number)+1:]
        number = int(number)*-1
        return (str, number)

def read_string(str):
    if not str:
        return (None,None)
    end = str.find('~')
    word = str[0:end]
    
    str = str[end+1:]

    return (str, word.strip())

def read_flags(str):
    if not str:
        return (None, None)
    str, w = read_word(str, False)
    if w == '0' or w == 0:
        return (str, 0)
    if w.isdigit():
        return (str, int(w))
    flags = 0

    for c in w:
        flag = 0
        if 'A' <= c and c <= 'Z':
            flag = A
            while c != 'A':
                flag *= 2
                c = chr( ord(c)-1 )

        elif 'a' <= c and c <= 'z':
            flag = aa
            while c != 'a':
                flag *= 2
                c = chr( ord(c)-1 )

        flags += flag
    return (str, flags)

def read_to_eol(str):
    str = str.split('\n')
    line = str.pop(0)
    str = "\n".join(str)
    return (str, line)


def is_name(arg, name):
    name, tmp = read_word(name)
    if not arg:
        return False
    while tmp:
        if tmp.lower().startswith(arg):
            return True
        name, tmp = read_word(name)
    return False

# * Given a string like 14.foo, return 14 and 'foo'
def number_argument( argument ):
    if '.' not in argument:
        return (1, argument)

    dot = argument.find('.')
    number = argument[:dot]
    if number.isdigit():
        return (int(number), argument[dot+1:])
    return (1, argument)

def check_blind( ch ):
    if not IS_NPC(ch) and IS_SET(ch.act,PLR_HOLYLIGHT):
        return True

    if IS_AFFECTED(ch, AFF_BLIND):
        ch.send( "You can't see a thing!\n\r") 
        return False 
    return True

def get_mob_id():
    return time.time()

def number_door( ):
    return random.randint(0,5)

# * Count occurrences of an obj in a list.
def count_obj_list(pObjIndex, contents):
    return len([obj for obj in contents if obj.pIndexData == pObjIndex])

# find an effect in an affect list */
def affect_find(paf, sn):
    found = [paf_find for paf_find in paf if paf_find.type == sn][:1]
    if found:
        return found[0]
    else:
        return None

# * Find some object with a given index data.
# * Used by area-reset 'P' command.
def get_obj_type( pObjIndex ):
    search = [obj for obj in object_list if obj.pIndexData == pObjIndex][:1]
    return search[0] if search else None


def CH(d): return d.original if d.original else d.character

# * Simple linear interpolation.
def interpolate(level, value_00, value_32):
    return value_00 + level * (value_32 - value_00) / 32

#Given a string like 14*foo, return 14 and 'foo'
def mult_argument(argument):
    if '*' not in argument:
        return (1, argument)
    mult = argument.find('*')
    number = argument[:mult]
    if not number.isdigit():
        return (1, argument)
    rest = argument[mult+1:]
    return (int(number), rest)


def append_file(ch, fp, str):
    with open(fp, "a") as f:
        f.write(str + "\n")

def format_obj_to_char(obj, ch, fShort):
    buf = ''
    if (fShort and not obj.short_descr) or not obj.description:
        return buf

    if IS_OBJ_STAT(obj, ITEM_INVIS):
        buf += "(Invis) "
    if IS_AFFECTED(ch, AFF_DETECT_EVIL) and IS_OBJ_STAT(obj, ITEM_EVIL):
        buf += "(Red Aura) "
    if IS_AFFECTED(ch, AFF_DETECT_GOOD) and  IS_OBJ_STAT(obj, ITEM_BLESS):
        buf += "(Blue Aura) "
    if IS_AFFECTED(ch, AFF_DETECT_MAGIC) and IS_OBJ_STAT(obj, ITEM_MAGIC):
        buf += "(Magical) "
    if IS_OBJ_STAT(obj, ITEM_GLOW):
        buf += "(Glowing) "
    if IS_OBJ_STAT(obj, ITEM_HUM):
        buf += "(Humming) "

    if fShort:
        if obj.short_descr:
            buf += obj.short_descr
    else:
        if obj.description:
            buf += obj.description
    if IS_SET(ch.act, PLR_OMNI):
        buf += "(%d)" % obj.pIndexData.vnum
    return buf

# * Show a list to a character.
# * Can coalesce duplicated items.
def show_list_to_char(clist, ch, fShort, fShowNothing):
    if not ch.desc:
        return
    objects = collections.OrderedDict()
    for obj in clist:
        if obj.wear_loc == WEAR_NONE and ch.can_see_obj(obj):
            frmt = format_obj_to_char(obj, ch, fShort)
            if frmt not in objects:
                objects[frmt] = 1
            else:
                objects[frmt] += 1


    if not objects and fShowNothing:
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE):
            ch.send("     ")
        ch.send("Nothing.\n")

     #* Output the formatted list.
    for desc, count in objects.items():
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\n" % (count, desc))
        else:
            for i in range(count):
                ch.send("     %s\n" % desc)

def show_char_to_char_0(victim, ch):
    buf = ''
    if IS_SET(victim.comm, COMM_AFK):
        buf += "[AFK] "
    if IS_AFFECTED(victim, AFF_INVISIBLE):
        buf += "(Invis) "
    if victim.invis_level >= LEVEL_HERO:
        buf += "(Wizi) "
    if IS_AFFECTED(victim, AFF_HIDE):
        buf += "(Hide) "
    if IS_AFFECTED(victim, AFF_CHARM):
        buf += "(Charmed) "
    if IS_AFFECTED(victim, AFF_PASS_DOOR):
        buf += "(Translucent) "
    if IS_AFFECTED(victim, AFF_FAERIE_FIRE):
        buf += "(Pink Aura) "
    if IS_EVIL(victim) and IS_AFFECTED(ch, AFF_DETECT_EVIL):
        buf += "(Red Aura) "
    if IS_GOOD(victim) and IS_AFFECTED(ch, AFF_DETECT_GOOD):
        buf += "(Golden Aura) "
    if IS_AFFECTED(victim, AFF_SANCTUARY):
        buf += "(White Aura) "
    if not IS_NPC(victim) and IS_SET(victim.act, PLR_KILLER):
        buf += "(KILLER) "
    if not IS_NPC(victim) and IS_SET(victim.act, PLR_THIEF):
        buf += "(THIEF) "

    if IS_NPC(victim) and victim.position == victim.start_pos and victim.long_descr:
        buf += victim.long_descr
        ch.send(buf)
        if IS_SET(ch.act, PLR_OMNI):
            ch.send("(%d)" % victim.pIndexData.vnum)
        return

    buf += PERS(victim, ch)
    if not IS_NPC(victim) and not IS_SET(ch.comm, COMM_BRIEF) \
    and victim.position == POS_STANDING and not ch.on:
        buf += victim.pcdata.title

    if victim.position == POS_DEAD: buf += " is DEAD!!"
    elif victim.position == POS_MORTAL: buf += " is mortally wounded."
    elif victim.position == POS_INCAP: buf += " is incapacitated."
    elif victim.position == POS_STUNNED: buf += " is lying here stunned."
    elif victim.position == POS_SLEEPING:
        if victim.on:
            if IS_SET(victim.on.value[2], SLEEP_AT):
                buf += " is sleeping at %s." % (victim.on.short_descr)
            elif IS_SET(victim.on.value[2], SLEEP_ON):
                buf += " is sleeping on %s." % (victim.on.short_descr)
            else:
                buf += " is sleeping in %s." % (victim.on.short_descr)
        else:
            buf += " is sleeping here."
    elif victim.position == POS_RESTING:
        if victim.on:
            if IS_SET(victim.on.value[2], REST_AT):
                buf += " is resting at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], REST_ON):
                buf += " is resting on %s." % victim.on.short_descr
            else:
                buf += " is resting in %s." % victim.on.short_descr
        else:
            buf += " is resting here."
    elif victim.position == POS_SITTING:
        if victim.on:
            if IS_SET(victim.on.value[2], SIT_AT):
                buf += " is sitting at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], SIT_ON):
                buf += " is sitting on %s." % victim.on.short_descr
            else:
                buf += " is sitting in %s." % victim.on.short_descr
        else:
            buf += " is sitting here."
    elif victim.position == POS_STANDING:
        if victim.on:
            if IS_SET(victim.on.value[2], STAND_AT):
                buf += " is standing at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], STAND_ON):
                buf += " is standing on %s." % victim.on.short_descr
            else:
                buf += " is standing in %s." % victim.on.short_descr
        else:
            buf += " is here."
    elif victim.position == POS_FIGHTING:
        buf += " is here, fighting "
        if not victim.fighting:
            buf += "thin air??"
        elif victim.fighting == ch:
            buf += "YOU!"
        elif victim.in_room == victim.fighting.in_room:
            buf += "%s." % PERS(victim.fighting, ch)
        else:
            buf += "someone who left??"
    buf = buf.capitalize()
    if IS_NPC(victim) and IS_SET(ch.act, PLR_OMNI):
        buf += "(%s)" % victim.pIndexData.vnum
    ch.send(buf)
    return

def show_char_to_char_1(victim, ch):
    if victim.can_see(ch):
        if ch == victim:
            act("$n looks at $mself.", ch, None, None, TO_ROOM)
        else:
            act("$n looks at you.", ch, None, victim, TO_VICT)
            act("$n looks at $N.", ch, None, victim, TO_NOTVICT)
    if victim.description:
        ch.send(victim.description + "\n")
    else:
        act("You see nothing special about $M.", ch, None, victim, TO_CHAR)
    if victim.max_hit > 0:
        percent = (100 * victim.hit) // victim.max_hit
    else:
        percent = -1
    buf = PERS(victim, ch)
    if percent >= 100:
        buf += " is in excellent condition.\n"
    elif percent >= 90:
        buf += " has a few scratches.\n"
    elif percent >= 75:
        buf += " has some small wounds and bruises.\n"
    elif percent >= 50:
        buf += " has quite a few wounds.\n"
    elif percent >= 30:
        buf += " has some big nasty wounds and scratches.\n"
    elif percent >= 15:
        buf += " looks pretty hurt.\n"
    elif percent >= 0:
        buf += " is in awful condition.\n"
    else:
        buf += " is bleeding to death.\n"

    buf = buf.capitalize()
    ch.send(buf)

    found = False
    for iWear in range(MAX_WEAR):
        obj = victim.get_eq(iWear)
        if obj and ch.can_see_obj(obj):
            if not found:
                act("$N is using:", ch, None, victim, TO_CHAR)
                found = True
            ch.send(where_name[iWear])
            ch.send(format_obj_to_char(obj, ch, True) + "\n")

    if victim != ch and not IS_NPC(ch) \
    and random.randint(1, 99) < ch.get_skill("peek"):
        ch.send("\nYou peek at the inventory:\n")
        check_improve(ch, 'peek', True, 4)
        show_list_to_char(victim.carrying, ch, True, True)
    return

def show_char_to_char(list, ch):
    for rch in list:
        if rch == ch:
            continue

        if ch.get_trust() < rch.invis_level:
            continue

        if ch.can_see(rch):
            show_char_to_char_0(rch, ch)
            ch.send("\n")
        elif ch.in_room.is_dark() and IS_AFFECTED(rch, AFF_INFRARED):
            ch.send("You see glowing red eyes watching YOU!\n")

def check_blind(ch):
    if not IS_NPC(ch) and IS_SET(ch.act, PLR_HOLYLIGHT):
        return True
    if IS_AFFECTED(ch, AFF_BLIND):
        ch.send("You can't see a thing!\n")
        return False
    return True

def add_follower( ch, master ):
    if ch.master:
        print ("BUG: Add_follower: non-null master.")
        return
    ch.master        = master
    ch.leader        = None
    if master.can_see(ch):
        act( "$n now follows you.", ch, None, master, TO_VICT )
    act( "You now follow $N.",  ch, None, master, TO_CHAR )
    return

def stop_follower( ch ):
    if not ch.master:
        print ("BUG: Stop_follower: null master.")
        return

    if IS_AFFECTED(ch, AFF_CHARM):
        REMOVE_BIT( ch.affected_by, AFF_CHARM )
        ch.affect_strip('charm person')

    if ch.master.can_see(ch) and ch.in_room:
        act( "$n stops following you.", ch, None, ch.master, TO_VICT)
        act( "You stop following $N.", ch, None, ch.master, TO_CHAR)
    if ch.master.pet == ch:
        ch.master.pet = None
    ch.master = None
    ch.leader = None
    return

# nukes charmed monsters and pets */
def nuke_pets( ch ):
    if ch.pet:
        stop_follower(ch.pet)
        if ch.pet.in_room:
            act("$N slowly fades away.",ch,None,ch.pet,TO_NOTVICT)
        ch.pet.extract(True)
    ch.pet = None
    return

def die_follower(ch):
    if ch.master:
        if ch.master.pet == ch:
            ch.master.pet = None
        stop_follower( ch )
    ch.leader = None

    for fch in char_list[:]:
        if fch.master == ch:
            stop_follower( fch )
        if fch.leader == ch:
            fch.leader = fch
    return

# * Get an extra description from a list.
def get_extra_descr(name, edlist):
    if not edlist: return None
    for ed in edlist:
        if name.lower() in ed.keyword:
            return ed.description
    return None

def find_location( ch, arg ):
    if arg.isdigit():
        vnum = int(arg)
        if vnum not in room_index_hash:
            return None
        else:
            return room_index_hash[vnum]
    victim = ch.get_char_world(arg)
    if victim:
        return victim.in_room
    obj = ch.get_obj_world(arg)
    if obj:
        return obj.in_room
    return None

#Magic functions
def say_spell(ch, spell):
    syl_dict = {"ar":"abra", "au":"kada", "bless":"fido", "blind":"nose", "bur":"mosa", "cu":"judi", "de":"oculo", "en":"unso", "light":"dies",
            "lo":"hi", "mor":"zak", "move":"sido", "ness":"lacri", "ning":"illa", "per":"duda",  "ra":"gru", "fresh":"ima", "re":"candus",
            "son":"sabru", "tect":"infra", "tri":"cula", "ven":"nofo", "a":"a", "b":"b", "c":"q", "d":"e", "e":"z", "f":"y", "g":"o",
            "h":"p", "i":"u", "j":"y", "k":"t", "l":"r", "m":"w", "n":"i", "o":"a", "p":"s", "q":"d", "r":"f", "s":"g", "t":"h", "u":"j",
            "v":"z", "w":"x", "x":"n", "y":"l", "z": "k" }
    incantation = mass_replace(spell.name, syl_dict)

    buf = "$n utters the words, '%s'." % incantation
    buf2 = "$n utters the words, '%s'." % spell.name

    for rch in ch.in_room.people:
        send = buf2 if ch.guild==rch.guild else buf
        act(send, ch, None, rch, TO_VICT)


def saves_spell(level, victim, dam_type):
    save = 50 + ( victim.level - level) * 5 - victim.saving_throw * 2
    if IS_AFFECTED(victim, AFF_BERSERK):
        save += victim.level//2

    immunity = victim.check_immune(dam_type)
    if immunity == IS_IMMUNE:
        return True
    elif immunity == IS_RESISTANT:
        save += 2
    elif immunity == IS_VULNERABLE:
        save -= 2

    if not IS_NPC(victim) and victim.guild.fMana:
        save = 9 * save // 10
    save = max( 5, min(save, 95 ) )

    return random.randint(1,99) < save

def saves_dispel(dis_level, spell_level, duration):
    if duration == -1:
      spell_level += 5
      # very hard to dispel permanent effects */

    save = 50 + (spell_level - dis_level) * 5
    save = max( 5, min(save, 95 ) )
    return random.randint(1,99) < save

def check_dispel(dis_level, victim, skill):
    from const import skill_table
    if is_affected(victim, skill):
        for af in victim.affected[:]:
            if af.type == skill:
                if not saves_dispel(dis_level,af.level,af.duration):
                    victim.affect_strip(sn)
                    if skill.msg_off:
                        victim.send(skill_table[sn].msg_off + "\n")
                    return True
                else:
                    af.level -= 1
    return False

target_name = ''
fLogAll = False

# for finding mana costs -- temporary version */
def mana_cost (ch, min_mana, level):
    if ch.level + 2 == level:
        return 1000
    return max(min_mana, (100 // (2 + ch.level - level)))

def find_spell(ch, name):
    #* finds a spell the character can cast if possible */
    from const import skill_table
    found = -1
    if IS_NPC(ch):
        return prefix_lookup(skill_table,name)
    for key, sn in const.skill_table.items():
        if sn.name.lower().startswith(name.lower()):
            if found == -1:
                found = sn
        if ch.level >= sn.skill_level[ch.guild.name] and key in ch.pcdata.learned:
            return sn
    return found

# trust levels for load and clone */
def obj_check (ch, obj):
    if IS_TRUSTED(ch,GOD) \
    or (IS_TRUSTED(ch,IMMORTAL) and obj.level <= 20 and obj.cost <= 1000) \
    or (IS_TRUSTED(ch,DEMI)     and obj.level <= 10 and obj.cost <= 500) \
    or (IS_TRUSTED(ch,ANGEL)    and obj.level <=  5 and obj.cost <= 250) \
    or (IS_TRUSTED(ch,AVATAR)   and obj.level ==  0 and obj.cost <= 100):
        return True
    else:
        return False


# for clone, to insure that cloning goes many levels deep */
def recursive_clone(ch, obj, clone):
    import db
    for c_obj in obj.contains:
        if obj_check(ch,c_obj):
            t_obj = db.create_object(c_obj.pIndexData,0)
            db.clone_object(c_obj,t_obj)
            t_obj.to_obj(clone)
            recursive_clone(ch,c_obj,t_obj)

def act(format, ch, arg1, arg2, send_to, min_pos = POS_RESTING):
    if not format:
        return
    if not ch or not ch.in_room:
        return

    vch = arg2
    obj1 = arg1
    obj2 = arg2

    he_she = ["it",  "he",  "she"]
    him_her = ["it",  "him", "her"]
    his_her = ["its", "his", "her"]

    to_players = ch.in_room.people

    if send_to is TO_VICT:
        if not vch:
            print ("Act: null vict with TO_VICT: " + format)
            return
        if not vch.in_room:
            return
        to_players = vch.in_room.people

    for to in to_players:
        if not to.desc or to.position < min_pos:
            continue
        if send_to is TO_CHAR and to is not ch:
            continue
        if send_to is TO_VICT and ( to is not vch or to is ch ):
            continue
        if send_to is TO_ROOM and to is ch:
            continue
        if send_to is TO_NOTVICT and (to is ch or to is vch):
            continue
        
        act_trans = {}
        if arg1:
            act_trans['$t'] = str(arg1)
        if arg2 and type(arg2) == str:
            act_trans['$T'] = str(arg2)
        if ch:
            act_trans['$n'] = PERS(ch, to)
            act_trans['$e'] = he_she[ch.sex]
            act_trans['$m'] = him_her[ch.sex]
            act_trans['$s'] = his_her[ch.sex]
        if vch and type(vch) == CHAR_DATA:
            act_trans['$N'] = PERS(vch, to)
            act_trans['$E'] = he_she[vch.sex]
            act_trans['$M'] = him_her[vch.sex]
            act_trans['$S'] = his_her[vch.sex]
        if obj1 and obj1.__class__ == OBJ_DATA:
            act_trans['$p'] = OPERS(to, obj1)
        if obj2 and obj2.__class__ == OBJ_DATA: 
            act_trans['$P'] = OPERS(to, obj2)
        act_trans['$d'] = arg2 if not arg2 else "door"
        
        format = mass_replace(format, act_trans)
        to.send(format+"\n")
    return
    
def wiznet( string, ch, obj, flag, flag_skip, min_level):
    from nanny import con_playing
    for d in descriptor_list:
        if   d.is_connected(con_playing) \
        and  IS_IMMORTAL(d.character) \
        and  IS_SET(d.character.wiznet, WIZ_ON) \
        and  (not flag or IS_SET(d.character.wiznet,flag)) \
        and  (not flag_skip or not IS_SET(d.character.wiznet,flag_skip)) \
        and  get_trust(d.character) >= min_level \
        and  d.character != ch:
            if IS_SET(d.character.wiznet,WIZ_PREFIX):
                d.send("-. ",d.character)
            act(string,d.character,obj,ch,TO_CHAR,POS_DEAD)

#ensureall do_functions become class methods
import interp
import handler_ch
import handler_obj
import handler_room