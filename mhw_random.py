#!/usr/bin/env python3


import os, random, sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEAPONS_DIR = os.path.join(BASE_DIR, "assets", "weapons")
MONSTERS_DIR = os.path.join(BASE_DIR, "assets", "monsters")

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def random_items():
    ws = [f for f in os.listdir(WEAPONS_DIR) if f.endswith(".png")]
    ms = [f for f in os.listdir(MONSTERS_DIR) if f.endswith(".png")]
    return (random.choice(ws), random.choice(ms)) if ws and ms else (None, None)

# ══════ 应援句 ══════
WEAPON_CHEERS = {
    "太刀": [["太刀侠来了！见切如风，登龙如虹~","纱雾最喜欢看太刀的红刃一闪啦！"],
             ["气刃兜割！唰——啪！","记得开刃再登龙哦，不然像个笨笨~"],
             ["袈裟斩~气刃斩~登龙！","太刀的节奏感，纱雾百看不厌呢"]],
    "大剑": [["蓄力…蓄力…真蓄斩！","纱雾帮你数着 1…2…3…放！"],
             ["肩撞铁山靠！大剑的浪漫就是一刀流~","打不中也没关系，气势要到！"],
             ["拔刀一击，收刀走人！","大剑的简洁美学，纱雾好喜欢"]],
    "双刀": [["鬼人化开启！嗷嗷嗷嗷——","转就完事了！纱雾看得眼花缭乱~"],
             ["搓背搓背搓背！双刀侠出击！","记得喝强走药哦，不然中途没体力啦"],
             ["乱舞乱舞乱舞！刀光剑影！","双刀的暴力美学，纱雾给你满分~"]],
    "大锤": [["锤子蓄力转圈圈~大地一击！","敲头眩晕是锤子的浪漫，纱雾懂的！"],
             ["给我晕！再晕！晕到死！","锤哥锤姐们冲呀，纱雾给你递鬼人药~"],
             ["斜坡转转转~空中转转转~","锤子的机动性可不输虫棍哦"]],
    "弓箭": [["龙之千矢！咻咻咻咻咻——","滑步刚射滑步刚射，手别抽筋呀"],
             ["曲射！全弹发射！","远程优雅狩猎，纱雾在营地泡好茶等你~"],
             ["接击瓶装好，刚射走起！","弓箭输出爆炸，纱雾都惊呆啦"]],
    "操虫棍": [["虫棍飞天流！比怪物跳得还高~","吸完红白黄三灯再开打，纱雾提醒你！"],
               ["虫棍侠永不落地！空中攻击就是帅！","记得喂饱你的猎虫哦，饿肚子可不行"],
               ["红灯攻击白灯移速黄灯防御！","三灯齐亮，你就是真正的空战王者"]],
    "斩斧": [["属性解放突刺！抱脸虫出击！","炸就完事了！纱雾远远帮你喊666"],
             ["斧形态走位，剑形态输出，零距离解放！","这波操作纱雾给你满分~"],
             ["高出力状态！完全解放——Boom！","纱雾捂着耳朵但还是忍不住看呢"]],
    "片手剑": [["片手剑！能打能奶能骑乘~","万能型猎人就是你啦，纱雾敬佩！"],
               ["盾砸眩晕接骑乘，片手剑的节奏太舒服了","道具流片手，队友都爱死你~"],
               ["不拔刀也能用道具！片手剑的隐藏技巧","纱雾觉得片手剑是最被低估的武器呢"]],
    "盾斧": [["充能…装瓶…超解！！！","一发超解命中时的快感，纱雾懂的！"],
             ["电锯模式嗡嗡嗡~锯就完事了！","记得先上红盾再超解，别空大啦"],
             ["GP反击！超解回击！帅炸了！","盾斧的操作上限，纱雾还在学习呢"]],
    "狩猎笛": [["吹笛子给队友上buff！节奏感拉满~","纱雾喜欢听狩猎笛的声音，好安心"],
               ["笛子侠是团队的灵魂！攻大防大回血全安排","纱雾也想被你buff一下呢~"],
               ["每一个音符都是对队友的守护","狩猎笛是最温柔的武器，纱雾觉得"]],
    "轻弩": [["速射速射速射！轻弩机动性拉满~","边跑边打，怪物摸都摸不到你！"],
             ["各种弹种切换，轻弩是战术大师！","纱雾帮你准备好了弹药箱~"],
             ["起爆龙弹！插满地！","怪物踩上去的瞬间，纱雾捂嘴偷笑"]],
    "重弩": [["架起盾牌！机关龙弹扫射——","站桩输出的王者，纱雾在背后支持你！"],
             ["扩散弹…狙击龙弹…哒哒哒哒哒！","重弩的火力压制，怪物根本抬不起头"],
             ["特射准备…龙击弹发射！！","纱雾被后坐力震得退了一步…好厉害"]],
    "铳枪": [["全弹发射！龙击炮！Boom——","铳枪的爆炸美学，纱雾看得好过瘾！"],
             ["炮击炮击炮击！管你肉质多硬！","无视肉质的浪漫，铳枪侠冲鸭~"],
             ["蓄力炮→全弹→龙击炮→装填！","无限连招！纱雾在帮你算弹数呢"]],
    "长枪": [["盾防！反击！稳如泰山~","长枪侠的坚毅，纱雾最欣赏了"],
             ["你不倒下我不退！长枪就是宣言！","防反流长枪，怪物打你等于打自己~"],
             ["Power Guard！绝对防御！","纱雾觉得长枪是最有安全感的武器"]],
}

GENERAL_CHEERS = [
    ["Ciallo~ (>w<)b  加油猎人酱！","纱雾在营地等你凯旋哦，别猫车啦"],
    ["唔姆…这只可不简单！带好陷阱和闪光弹","Ciallo~ (>w<)b  纱雾给你上buff"],
    ["牙白得斯内! 这签运纱雾看好你哟","断尾破头一条龙，猎人酱冲鸭~"],
    ["诶嘿，纱雾今天手气不错嘛","记得吃猫饭再去哦，别饿着肚子狩猎"],
    ["呜哇…这组合有点凶险，带上大桶爆弹G","纱雾会帮你祈祷不猫车的~ Ciallo!"],
    ["咕噜咕噜…纱雾刚睡醒就看到好签！","去吧猎人酱，今晚加餐吃烤龙肉~"],
    ["哦呀？这只的素材正好能强化你的装备！","纱雾翻了翻攻略书，弱点在头部哦"],
    ["带上秘药带上远古秘药，做好万全准备！","纱雾在帐篷帮你整理好了道具箱~"],
    ["今天的运气真不错呢！蹭蹭好运~","猎人酱凯旋回来纱雾给你膝枕奖励哦"],
    ["听说这只能出宝玉！刷就对了！","纱雾给你画了幸运符，带在身上吧~"],
    ["唔…纱雾觉得你可以试试捕获？","看它瘸腿了就放陷阱，素材更多呢"],
    ["Aibo！出发前检查一下装备耐久度~","纱雾帮你磨好刀了，锋利度MAX"],
    ["注意看它的前摇动作，别贪刀哦！","纱雾在后方给你分析怪物AI中…诶嘿"],
    ["环境生物也可以利用起来！","纱雾看到地图上有落石和麻痹蛙~"],
    ["猫车不可怕，可怕的是不敢再战！","纱雾会一直等你回来的，再出发吧！"],
    ["狩猎前先看看调查据点的资源","纱雾刚刚帮你采了一些蜂蜜回来~"],
]

def pick_cheers(wname):
    wl = WEAPON_CHEERS.get(wname, [])
    if wl and random.random() < 0.7:
        wline = random.choice(wl)
        gline = random.choice(GENERAL_CHEERS)
        return [wline[0], gline[1] if random.random() < 0.5 else wline[1]]
    return random.choice(GENERAL_CHEERS)

# ══════ 配色 ══════
BG      = (255, 251, 235)
WHITE   = (255, 255, 255)
YELLOW  = (254, 190, 13)
BROWN   = (75, 63, 47)
RED_BG  = (254, 242, 242)
RED_BD  = (254, 202, 202)
RED_TXT = (185, 28, 28)
GREEN_BG = (240, 253, 244)
GREEN_BD = (220, 252, 231)
GREEN_TXT = (21, 128, 61)
GRAY_BG = (249, 250, 251)
GRAY_BD = (243, 244, 246)
GRAY_200 = (229, 231, 235)
MUTED   = (150, 140, 130)

def create_card(weapon_file, monster_file, output_path):
    wname = weapon_file.replace(".png", "")
    mname = monster_file.replace(".png", "")
    cheers = pick_cheers(wname)

    wimg = Image.open(os.path.join(WEAPONS_DIR, weapon_file)).convert("RGBA")
    mimg = Image.open(os.path.join(MONSTERS_DIR, monster_file)).convert("RGBA")

    ICON_SZ = 200
    wimg_icon = wimg.resize((ICON_SZ, ICON_SZ), Image.LANCZOS)
    mimg_icon = mimg.resize((ICON_SZ, ICON_SZ), Image.LANCZOS)

    CARD_W = 960
    CARD_PAD = 52
    CONTENT_W = CARD_W - CARD_PAD * 2

    HEADER_H = 180
    PANEL_PAD = 44
    PANEL_H = ICON_SZ + PANEL_PAD * 2
    INPUT_AREA_H = 280
    FOOTER_H = 160
    PAD = 36

    TOTAL_W = CARD_W + PAD * 2
    TOTAL_H = PAD + HEADER_H + PANEL_H*2 + 160 + INPUT_AREA_H + FOOTER_H + PAD

    img = Image.new("RGBA", (TOTAL_W, TOTAL_H), BG + (255,))
    draw = ImageDraw.Draw(img)

    # 白色卡片 + 阴影
    shadow_off = 8
    draw.rounded_rectangle([PAD+shadow_off, PAD+24, PAD+CARD_W+shadow_off, TOTAL_H-PAD+24], 52, fill=(218,178,50,30))
    draw.rounded_rectangle([PAD, PAD, PAD+CARD_W, TOTAL_H-PAD], 52, fill=WHITE, outline=YELLOW, width=6)

    # ── Header ── (无头像)
    hx = PAD + 12
    hy = PAD + 12
    hw = CARD_W - 24
    hh = HEADER_H
    draw.rounded_rectangle([hx, hy, hx+hw, hy+hh], 40, fill=YELLOW)

    ft_title = get_font(52, True)
    ft_header_sub = get_font(26, True)
    draw.text((hx+40, hy+30), "纱雾的怪猎抽签", fill=BROWN, font=ft_title)
    draw.text((hx+40, hy+100), '输入 "怪猎随机" 开始你的狩猎！', fill=(130,105,70), font=ft_header_sub)

    # ── 面板区域 ──
    content_y = hy + hh + 24
    px = PAD + CARD_PAD
    panel_w = CONTENT_W

    # 武器面板 (上)
    wy = content_y
    draw.rounded_rectangle([px, wy, px+panel_w, wy+PANEL_H], 32, fill=GREEN_BG, outline=GREEN_BD, width=4)

    # tag - 居中
    tag2_w = 160
    tag_h = 34
    ft_tag = get_font(18, True)
    tag_label = "武器"
    tag_bbox = draw.textbbox((0,0), tag_label, font=ft_tag)
    tag_pad = 28
    tag_w = tag_bbox[2] - tag_bbox[0] + tag_pad * 2
    tag_x = px + (panel_w - tag_w) // 2
    tag_y = wy - tag_h // 2
    draw.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+tag_h], tag_h//2, fill=GREEN_BD)
    draw.text((tag_x + (tag_w - (tag_bbox[2]-tag_bbox[0]))//2,
               tag_y + (tag_h - (tag_bbox[3]-tag_bbox[1]))//2),
              tag_label, fill=GREEN_TXT, font=ft_tag)

    circ_x = px + PANEL_PAD
    circ_y = wy + PANEL_PAD
    draw.ellipse([circ_x, circ_y, circ_x+ICON_SZ, circ_y+ICON_SZ], fill=WHITE, outline=GREEN_BD, width=3)
    w_small = wimg_icon.resize((ICON_SZ-12, ICON_SZ-12), Image.LANCZOS)
    img.paste(w_small, (circ_x+6, circ_y+6), w_small)

    ft_name = get_font(42, True)
    ft_name_sub = get_font(22, True)
    name_x = circ_x + ICON_SZ + 32
    name_y = wy + PANEL_PAD + 18
    draw.text((name_x, name_y), wname, fill=GREEN_TXT, font=ft_name)
    draw.text((name_x, name_y + 56), "用这个武器大显身手吧！", fill=(100,165,125), font=ft_name_sub)

    # 怪物面板 (下)
    my = wy + PANEL_H + 24
    draw.rounded_rectangle([px, my, px+panel_w, my+PANEL_H], 32, fill=RED_BG, outline=RED_BD, width=4)

    # tag
    tag_label2 = "讨伐目标"
    tag_bbox2 = draw.textbbox((0,0), tag_label2, font=ft_tag)
    tag_w2 = tag_bbox2[2] - tag_bbox2[0] + tag_pad * 2
    tag_x2 = px + (panel_w - tag_w2) // 2
    tag_y2 = my - tag_h // 2
    draw.rounded_rectangle([tag_x2, tag_y2, tag_x2+tag_w2, tag_y2+tag_h], tag_h//2, fill=RED_BD)
    draw.text((tag_x2 + (tag_w2 - (tag_bbox2[2]-tag_bbox2[0]))//2,
               tag_y2 + (tag_h - (tag_bbox2[3]-tag_bbox2[1]))//2),
              tag_label2, fill=RED_TXT, font=ft_tag)

    circ_x2 = px + PANEL_PAD
    circ_y2 = my + PANEL_PAD
    draw.ellipse([circ_x2, circ_y2, circ_x2+ICON_SZ, circ_y2+ICON_SZ], fill=WHITE, outline=RED_BD, width=3)
    m_small = mimg_icon.resize((ICON_SZ-12, ICON_SZ-12), Image.LANCZOS)
    img.paste(m_small, (circ_x2+6, circ_y2+6), m_small)

    name_y2 = my + PANEL_PAD + 18
    draw.text((name_x, name_y2), mname, fill=RED_TXT, font=ft_name)
    draw.text((name_x, name_y2 + 56), "准备好迎接挑战了吗？", fill=(200,130,130), font=ft_name_sub)

    # ── 输入区 ──
    input_y = my + PANEL_H + 24
    input_h = INPUT_AREA_H
    draw.rounded_rectangle([px, input_y, px+panel_w, input_y+input_h], 0, fill=GRAY_BG)
    draw.line([px, input_y, px+panel_w, input_y], fill=GRAY_BD, width=6)

    inp_x = px + 40
    inp_y = input_y + 50
    inp_w = panel_w - 80
    inp_h = 80
    draw.rounded_rectangle([inp_x, inp_y, inp_x+inp_w, inp_y+inp_h], 22, fill=WHITE, outline=GRAY_200, width=3)
    ft_input = get_font(28, True)
    draw.text((inp_x+34, inp_y+(inp_h-ft_input.size)//2),
              '输入 "怪猎随机" 并按回车', fill=(180,175,170), font=ft_input)
    # 搜索按钮 - 画放大镜
    sbtn_sz = 64
    sbtn_x = inp_x + inp_w - sbtn_sz - 12
    sbtn_y = inp_y + (inp_h - sbtn_sz)//2
    draw.rounded_rectangle([sbtn_x, sbtn_y, sbtn_x+sbtn_sz, sbtn_y+sbtn_sz], 16, fill=YELLOW)
    ft_sbtn = get_font(30, True)
    b = draw.textbbox((0,0), "Go", font=ft_sbtn)
    tw, th = b[2]-b[0], b[3]-b[1]
    # 精确居中：用 bbox 高度计算 y 偏移
    draw.text((sbtn_x + (sbtn_sz-tw)//2,
               sbtn_y + (sbtn_sz-th)//2 - b[1]),
              "Go", fill=WHITE, font=ft_sbtn)

    # 随机按钮
    roll_y = inp_y + inp_h + 36
    roll_h = 90
    draw.rounded_rectangle([inp_x, roll_y+8, inp_x+inp_w, roll_y+roll_h+8], 24, fill=(42,35,27))
    draw.rounded_rectangle([inp_x, roll_y, inp_x+inp_w, roll_y+roll_h], 24, fill=BROWN)
    ft_roll = get_font(32, True)
    b = draw.textbbox((0,0), "随机一下", font=ft_roll)
    draw.text((inp_x+(inp_w-(b[2]-b[0]))//2, roll_y+(roll_h-(b[3]-b[1]))//2),
              "随机一下", fill=WHITE, font=ft_roll)

    # ── 应援句 ──
    cheer_y = input_y + input_h + 12
    ft_c1 = get_font(28, True)
    ft_c2 = get_font(22)
    b1 = draw.textbbox((0,0), cheers[0], font=ft_c1)
    draw.text(((TOTAL_W-(b1[2]-b1[0]))//2, cheer_y+20), cheers[0], fill=BROWN, font=ft_c1)
    b2 = draw.textbbox((0,0), cheers[1], font=ft_c2)
    draw.text(((TOTAL_W-(b2[2]-b2[0]))//2, cheer_y+60), cheers[1], fill=MUTED, font=ft_c2)

    credit = "Hunt Lucky · Powered by Palico Logic"
    ft_cr = get_font(18)
    b = draw.textbbox((0,0), credit, font=ft_cr)
    draw.text(((TOTAL_W-(b[2]-b[0]))//2, cheer_y+100), credit, fill=(180,170,160), font=ft_cr)

    img.save(output_path, "PNG", optimize=True)
    return True

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "mhw_result.png")
    w, m = random_items()
    if not w or not m:
        print("ERROR")
        sys.exit(1)
    create_card(w, m, out)
    print(f"OK:{out}:{w.replace('.png','')}:{m.replace('.png','')}")
