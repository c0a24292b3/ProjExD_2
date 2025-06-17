import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面内
    if rct.left < 0 or WIDTH < rct.right:  # 横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向の画面外判定
        tate = False
    return yoko, tate  # 横方向，縦方向の画面内判定結果を返す

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数
    """
    # 画面を半透明の黒で覆う
    blackscreen = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackscreen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))#画面を覆う黒い四角を作成
    blackscreen.set_alpha(200)  # 半透明にする
    screen.blit(blackscreen, (0, 0))#貼り付ける。

     # Game Over テキストの描画
    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))#白文字でgameover
    text_rct = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rct)#中央にgameoverをはりつけ

    # 泣いているこうかとん画像の表示
    crying_kk = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)#泣いているこうかとん
    left_rct = crying_kk.get_rect(center=(text_rct.left - 60, HEIGHT // 2))#ゲームオーバーの左側にこうかとんを配置
    screen.blit(crying_kk, left_rct)
    right_rct = crying_kk.get_rect(center=(text_rct.right + 60, HEIGHT // 2))#ゲームオーバーの右側にこうかとんを配置
    screen.blit(crying_kk, right_rct)
    pg.display.update()  # 画面更新
    time.sleep(5)  # 5秒待つ
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    bb_imgs = []
    bb_accs = [i for i in range(1, 11)]  # 加速度リスト（1〜10）

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)  # リストに追加

    return bb_imgs, bb_accs
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs,bb_accs=init_bb_imgs()#爆弾の大きさ、加速度
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明色に設定
    bb_rct = bb_imgs[0].get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  # 爆弾の移動速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
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
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()