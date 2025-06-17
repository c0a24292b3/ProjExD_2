import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数
    """
    blackscreen = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackscreen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))#黒い四角を作る。
    blackscreen.set_alpha(200)#半透明にする。
    screen.blit(blackscreen, (0, 0))#貼り付ける。

    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))#白文字でゲームオーバー
    text_rct = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))#中心の座標を取る。
    screen.blit(text, text_rct)#画面中央に文字を貼り付ける。

    crying_kk = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)#泣いているこうかとん画像
    left_rct = crying_kk.get_rect(center=(text_rct.left - 60, HEIGHT // 2))#文字の左側の座標を取る。
    right_rct = crying_kk.get_rect(center=(text_rct.right + 60, HEIGHT // 2))#文字の右側の座標を取る。
    screen.blit(crying_kk, left_rct)
    screen.blit(crying_kk, right_rct)#それぞれを配置する。
    pg.display.update()#画面の更新
    time.sleep(5)#5秒停止

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceのリストと、それに対応する加速度のリストを返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):#10段階
        bb_img = pg.Surface((20*r, 20*r))#正方形
        bb_img.set_colorkey((0, 0, 0))#透明化
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)#赤い円
        bb_imgs.append(bb_img)#リストに追加
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        level = min(tmr // 150, 9)## 時間に応じて爆弾の加速＆拡大
        avx = vx // abs(vx) * bb_accs[level]#速度を段階的に増やす。
        avy = vy // abs(vy) * bb_accs[level]

        # 爆弾画像と位置の更新
        old_center = bb_rct.center#中心座標を記憶
        bb_img = bb_imgs[level]#レベルに応じた爆弾を選ぶ
        bb_rct = bb_img.get_rect(center=old_center)#新しい形を取得するが、座標は変えない。

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
