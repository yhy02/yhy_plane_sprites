import random

import pygame

#  屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
#  刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FRIE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵类"""

    def __init__(self, image_name, speed=1):
        # 必须调用父类的方法。应为这个类不是继承基类object的
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    # 重写Sprite-父类的方法，每次更新游戏循环内的调用
    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵类"""

    # 创建初始化函数并添加判断形参是否是第一张图片，False表示就是第一张图片
    def __init__(self, is_alt=False):

        # 调用父类方法实现精灵的创建（image/rect/speed)
        super().__init__("./yhy_images/bg_WaterDrop.png")
        # 判断是否是交替图像。如果是，需要指定位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 调用父类（这时他的父类是-GameSprite）的方法来实现向下移动
        super().update()
        # 判断是否移出了屏幕，如果有，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵类"""

    def __init__(self):
        # 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./yhy_images/敌机(1).png")
        # 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)
        # 指定敌机的初始随机位置(x, y)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 调用父类方法，继承垂直方向的移动
        super().update()
        # 判断是否飞出屏幕。如果是，需要从精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            # print("敌机已经飞出屏幕，需要从精灵组中删除")
            # kill方法可以把精灵从所有精灵组中移除，精灵就会自动销毁
            self.kill()

    def __del__(self):
        # print("敌机挂了，%s" % self.rect)
        pass


class Hreo(GameSprite):
    """英雄精灵类"""

    def __init__(self):
        # 调用父类方法，设置image&speed
        super().__init__("./yhy_images/aline_145_160.png", 0)

        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 10

        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄水平方向的移动
        self.rect.x += self.speed

        # 判断和控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹...")

        # for i in (0, 1, 2):
        # 创建子弹精灵
        bullet = Bullet()
        # 设置子弹精灵的位置
        # bullet.rect.bottom = self.rect.y + i * 30
        bullet.rect.bottom = self.rect.y + 30
        bullet.rect.centerx = self.rect.centerx
        # 将子弹精灵添加到子弹精灵组
        self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵类"""

    def __init__(self):
        # 调用父类方法，设置子弹图片和设置初始速度
        super().__init__("./yhy_images/火箭.png", -2)

    def update(self):
        # 调用父类方法，让子弹垂直飞行
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")
