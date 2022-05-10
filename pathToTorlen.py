import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty,BooleanProperty
)
import math
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Rotate
from kivy.graphics.context_instructions import PopMatrix,PushMatrix
import random
from kivy.config import Config
from kivy.clock import Clock
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#room= stage->[room->[vragi->[],walls->[]]]
rooms=[
       [[(100,100),(150,150)],[(100,100,200,200),(300,140,300,300)]],[[(150,200),(200,200),(250,200),(300,200),(350,200)],[]],[[(100,200),(200,100),(290,123)],[(200,100,532,211)]],
       [[],[],[]],
       [[],[],[]]
       ]
enimies = [["Archer","Spider"],
           [],
           []]
bosses = [["Boss_spider"],
          [],
          []]
shields = [["Bastion",500,"Активка: ограждает гг стенами, во время активки нельзя передвигаться"]]
magick_items = [["Revive_amulet",200,"После смерти восстанавливает фулл хп"],
                ["Boots_of_speed",50,"Немного ускоряет гг"],
                ["Bots_of_unstoppble",100,"Гг не стопается разными эффектами"]]
class KnightGame(Widget):
    is_win = BooleanProperty(True)
    number_of_room=NumericProperty(0)
    number_of_stage=NumericProperty(0)
    control_knight = ObjectProperty(None)
    control_zone_knight = ObjectProperty(None)
    control_shield = ObjectProperty(None)
    control_zone_shield = ObjectProperty(None)
    
    knight=ObjectProperty(None)
    hp_indicate = ObjectProperty(None)
    coins = NumericProperty(0)
    items_collection = ObjectProperty(None)
    shield=ObjectProperty(None)
    shield_effects=ObjectProperty(None)
    archers = ObjectProperty(None)
    arrows = ObjectProperty(None)

    walls = ObjectProperty(None)
    fake_exit=ObjectProperty(None)
    true_exit=ObjectProperty(None)

    effects = ObjectProperty(None)

    windows = ObjectProperty(None)

    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    def on_start(self,dt):
        for x in range(1,self.knight.hp+1):
            self.hp_indicate.add_widget(Builder.load_string('''
Heart:
    pos:'''+str(x*31)+''','''+str(self.height-self.height/8)+'''
'''))
    def rebuilding(self):
        self.is_win=False
        while(self.archers.children):
            for archer in self.archers.children:
                self.archers.remove_widget(archer)
        while(self.items_collection.children):
            for coin in self.items_collection.children:
                self.items_collection.remove_widget(coin)
        while(self.effects.children):
            for effect in self.effects.children:
                self.effects.remove_widget(effect)
        while(self.arrows.children):
            for arrow in self.arrows.children:
                self.arrows.remove_widget(arrow)
        for wall in self.walls.children[:-4]:
            self.walls.remove_widget(wall)
        global rooms, enimies, bosses
        self.number_of_room+=1
        if self.number_of_room>22:
            self.number_of_room=1
            self.number_of_stage+=1
            if self.number_of_stage>1:
                return print('WIN')    
        self.knight.center=self.width/2,self.height/10;
        if self.number_of_room == 21:
            boss = bosses[self.number_of_stage][random.randint(0,len(bosses[self.number_of_stage])-1)]
            builder_string='''
'''+str(boss)+'''
    center:300,300
'''
            self.archers.add_widget(Builder.load_string(builder_string))
        elif self.number_of_room%10!=0:
            self.num_of_room = random.randint(0,len(rooms[0]))
            for ps in rooms[self.num_of_room][0]:
                self.pos_x=ps[0]
                self.pos_y=ps[1]
                builder_string = '''
'''+str(enimies[self.number_of_stage][random.randint(0,len(enimies[self.number_of_stage])-1)])+'''
    pos:'''+str(self.pos_x)+''','''+str(self.pos_y)+'''
        
    '''
                self.archers.add_widget(Builder.load_string(builder_string))
            for ps in rooms[self.num_of_room][1]:
                self.pos_x=ps[2]
                self.pos_y=ps[3]
                self.size_x=ps[0]
                self.size_y=ps[1]
                builder_string = '''
Wall:
    size:'''+str(self.size_x)+''','''+str(self.size_y)+'''
    pos:'''+str(self.pos_x)+''','''+str(self.pos_y)+'''
        
    '''
                self.walls.add_widget(Builder.load_string(builder_string))
        else:
            global magick_items
            self.is_win = True
            self.archers.add_widget(Builder.load_string('''
Trader:
    size:100,300
    center_x:'''+str(self.width)+'''-self.width/2
    center_y:'''+str(self.center_y)+'''
'''))
            for n in range(3):
                for trader in self.archers.children:
                    if random.randint(0,100)>=80:
                        item = shields[random.randint(0,len(shields)-1)]
                        item_type="s"
                    else:
                        item = magick_items[random.randint(0,len(magick_items)-1)]
                        item_type="i"
                    trader.add_widget(Builder.load_string('''
Run_zone:
    size:150,100
    pos:'''+str(trader.pos[0])+'''-self.width,'''+str(trader.pos[1])+'''+'''+str(n)+'''*self.height
    item:"'''+item[0]+'''"
    cost:'''+str(item[1])+'''
    description:"'''+item[2]+'''"
    item_type:"'''+item_type+'''"
    not_touched:True
    not_kuplen:True
'''))
    def on_touch_down(self,touch):
        if touch.x < self.width / 2:
            self.control_zone_knight.center_x = touch.x
            self.control_zone_knight.center_y = touch.y
            self.control_knight.center_x = touch.x
            self.control_knight.center_y = touch.y
        else:
            self.shield.is_pressed = True
            self.control_zone_shield.center_x = touch.x
            self.control_zone_shield.center_y = touch.y
            self.control_shield.center_x = touch.x
            self.control_shield.center_y = touch.y
            self.shield.children[0].effect_down(self)
    def on_touch_move(self, touch):
        if touch.x < self.width / 2:
            if (( (touch.x-self.control_zone_knight.center_x)**2 +
                  (touch.y-self.control_zone_knight.center_y)**2 ) <=
                    (self.control_zone_knight.width/2)**2):
                self.control_knight.center_x = touch.x
                self.control_knight.center_y = touch.y
            else:
                if touch.x>self.control_zone_knight.x+self.control_zone_knight.width:
                    self.control_knight.center_x=self.control_zone_knight.x+self.control_zone_knight.width
                elif touch.x<self.control_zone_knight.x:    
                    self.control_knight.center_x=self.control_zone_knight.x
                else:
                    self.control_knight.center_x=touch.x
                if touch.y>self.control_zone_knight.y+self.control_zone_knight.height:
                    self.control_knight.center_y=self.control_zone_knight.y+self.control_zone_knight.height
                elif touch.y<self.control_zone_knight.y:    
                    self.control_knight.center_y=self.control_zone_knight.y
                else:
                    self.control_knight.center_y=touch.y
        else:
            self.shield.is_pressed = True
            self.shield.children[0].effect_up(self)
            if (( (touch.x-self.control_zone_shield.center_x)**2 +
                  (touch.y-self.control_zone_shield.center_y)**2 ) <=
                    (self.control_zone_shield.width/2)**2):
                self.control_shield.center_x = touch.x
                self.control_shield.center_y = touch.y
            else:
                if touch.x>self.control_zone_shield.x+self.control_zone_shield.width:
                    self.control_shield.center_x=self.control_zone_shield.x+self.control_zone_shield.width
                elif touch.x<self.control_zone_shield.x:    
                    self.control_shield.center_x=self.control_zone_shield.x
                else:
                    self.control_shield.center_x=touch.x
                if touch.y>self.control_zone_shield.y+self.control_zone_shield.height:
                    self.control_shield.center_y=self.control_zone_shield.y+self.control_zone_shield.height
                elif touch.y<self.control_zone_shield.y:    
                    self.control_shield.center_y=self.control_zone_shield.y
                else:
                    self.control_shield.center_y=touch.y
            
    def on_touch_up(self,touch):
        if touch.x < self.width/2:
            self.control_zone_knight.center_x = self.width/4
            self.control_zone_knight.center_y = self.height/5
            self.control_knight.center_x = self.control_zone_knight.center_x
            self.control_knight.center_y = self.control_zone_knight.center_y
        else:
            self.control_zone_shield.center_x = self.width - self.width/4
            self.control_zone_shield.center_y = self.height/5
            self.control_shield.center_x = self.control_zone_shield.center_x
            self.control_shield.center_y = self.control_zone_shield.center_y
            self.shield.is_pressed = False
            self.shield.children[0].effect_up(self)
    def update(self,dt):
        
        if self.knight.hp<=0:
            return print("LOSE")
        self.knight_chek_na_collide_wall = False
        for wall in self.walls.children:
            if wall.collide_widget(self.knight):
                self.knight_chek_na_collide_wall=True
                break
        for archer in self.archers.children:
            if archer.collide_widget(self.knight):
                self.knight_chek_na_collide_wall=True
                break
        if self.knight_chek_na_collide_wall:
            self.knight.center_x=self.knight_back_center_x
            self.knight.center_y=self.knight_back_center_y
            self.knight.speed_x=0
            self.knight.speed_y=0
        else:
            self.knight_back_center_x=self.knight.center_x
            self.knight_back_center_y=self.knight.center_y
            self.knight.speed_x=(self.control_knight.center_x-self.control_zone_knight.center_x)//15
            self.knight.speed_y=(self.control_knight.center_y-self.control_zone_knight.center_y)//15
        for archer in self.archers.children:
            archer.update(self)
        for arrow in self.arrows.children:
            arrow.update(self)
        for effect in self.effects.children:
            effect.update(self)
        for coin in self.items_collection.children:
            coin.update(self)
        if self.shield.is_pressed:
            self.shield.move(self.control_shield,self.control_zone_shield)    
        self.shield.children[0].update(self)
        for item in self.knight.equip_items.children:
            item.update(self)
        
        self.knight.center_x+=self.knight.speed_x
        self.knight.center_y+=self.knight.speed_y
        
        self.shield.center_x=self.knight.x+(self.knight.width*self.shield.knight_pos_x)
        self.shield.center_y=self.knight.y+(self.knight.height*self.shield.knight_pos_y)

        for window in self.windows.children:
            window.update(self)
        
        if (self.knight.collide_widget(self.true_exit)):
            if self.is_win:
                self.rebuilding()

class Gamepad(Widget):
    pass

class GamepadZone(Widget):
    pass

class Trader(Widget):
    def chek_move(self,some_object,game):
        pass
    def self_collide_shield(self,game):
        pass
    def buy(self,item,item_type,cost,game):
        if game.coins>=cost:
            game.coins-=cost
            if item_type=="i":
                game.knight.equip_items.add_widget(Builder.load_string('''
Item_'''+str(item)+''':
'''))
            else:
                game.shield.remove_widget(game.shield.children[:])
                game.shield.add_widget(Builder.load_string('''
Shield_'''+item+''':
'''))
                game.shield.type = item
        else:
            print("Милорд ваша казна пуста")
    def update(self,game):
        chek_palatok = 0
        for shop_zone in self.children:
            if shop_zone.collide_widget(game.knight):
                if shop_zone.not_touched:
                    for window in game.windows.children:
                        game.windows.remove_widget(window)
                    game.windows.add_widget(Builder.load_string('''
Info_window:
    size:300,200
    pos:'''+str(game.center_x)+'''-self.width//2,'''+str(game.height/8)+'''
    canvas:
        Color:
            rgb:0,.2,.1
        Rectangle:
            pos:self.pos
            size:self.size

    layout_1:layout_1_id
    layout_2:layout_2_id
    layout_3:layout_3_id
    AnchorLayout:
        id:layout_1_id
        size:300,200
        pos:'''+str(game.center_x)+'''-self.width//2,'''+str(game.height/8)+'''
        anchor_x:'left'
        anchor_y:'top'
    AnchorLayout:
        id:layout_2_id
        size:300,200
        pos:'''+str(game.center_x)+'''-self.width//2,'''+str(game.height/8)+'''
        anchor_x:'center'
        anchor_y:'center'

    AnchorLayout:
        id:layout_3_id
        size:300,200
        pos:'''+str(game.center_x)+'''-self.width//2,'''+str(game.height/8)+'''
        anchor_x:'right'
        anchor_y:'bottom'   
'''))
                    button_n = Button(text = str(shop_zone.item), size_hint = (.5,.1))
                    button_d = TextInput(text = str(shop_zone.description),size_hint=(.9,.7))
                    button_c = Button(text = str(shop_zone.cost), size_hint = (.01,.01),)
                    game.windows.children[-1].layout_1.add_widget(button_n)
                    game.windows.children[-1].layout_2.add_widget(button_d)
                    game.windows.children[-1].layout_3.add_widget(button_c)
                    print("предметек = "+shop_zone.item)
                    shop_zone.not_touched = False
            else:
                chek_palatok+=1
                shop_zone.not_touched = True
            if game.shield.collide_widget(self):
                if not(shop_zone.not_touched):
                    if shop_zone.not_kuplen:
                        self.buy(shop_zone.item,shop_zone.item_type,shop_zone.cost,game)
                        shop_zone.not_kuplen = False
                    else:
                        print('товар куплен')
        if chek_palatok==3:
            for window in game.windows.children:
                game.windows.remove_widget(window)
            
class Info_window(Widget):
    def update(self,game):
        pass
class Knight(Widget):
    pass
class Item_on_ground(Widget):
    def create(self,item,game):
        self.item = item
    def update(self,game):
        if self.collide_widget(game.knight):
            global magick_items
            game.knight.equip_items.add_widget(Builder.load_string('''
Item_'''+self.item+''':   
'''))
            game.items_collection.remove_widget(self)
class Item_Revive_amulet(Widget): 
    def update(self,game):
        if game.knight.hp <= 0:
            game.knight.hp = game.knight.max_hp
            game.knight.equip_items.remove_widget(self)
            for x in range(1,game.knight.hp+1):
                game.hp_indicate.add_widget(Builder.load_string('''
Heart:
    pos:'''+str(x*31)+''','''+str(game.height-game.height/8)+'''
'''))
class Item_Boots_of_speed(Widget):
    def update(self,game):
        game.knight.speed_x*=1.5
        game.knight.speed_y*=1.5
class Item_Bots_of_unstoppble(Widget):
    def update(self,game):
        if game.knight.speed_x == 0 and game.knight.speed_y == 0:
            game.knight.speed_x=(game.control_knight.center_x-game.control_zone_knight.center_x)//15
            game.knight.speed_y=(game.control_knight.center_y-game.control_zone_knight.center_y)//15
class Hp_indicate(Widget):
    pass
class Heart(Widget):
    pass
class Collection_of_items(Widget):
    pass
class Coin(Widget):
    def update(self,game):
        if self.collide_widget(game.knight):
            game.coins+=self.cost
            game.items_collection.remove_widget(self)
class Shield(Widget):
    def move(self,gamepad,zone):
        if (gamepad.center_x==zone.x):
            if(gamepad.center_y==zone.y+zone.height):
                self.angle=135
                self.knight_pos_x=0
                self.knight_pos_y=1
            elif(gamepad.center_y==zone.y):
                self.angle=45
                self.knight_pos_x=0
                self.knight_pos_y=0
            else:
                self.angle=0
                self.knight_pos_x=-0.1
                self.knight_pos_y=0.5
        elif (gamepad.center_x==zone.x+zone.height):
            if(gamepad.center_y==zone.y+zone.height):
                self.angle=45
                self.knight_pos_x=1
                self.knight_pos_y=1
            elif(gamepad.center_y==zone.y):
                self.angle=135
                self.knight_pos_x=1
                self.knight_pos_y=0
            else:
                self.angle=0
                self.knight_pos_x=1.1
                self.knight_pos_y=0.5
        else:
            if(gamepad.center_y>=zone.center_y):
                self.angle=90
                self.knight_pos_x=0.5
                self.knight_pos_y=1.1
            else:
                self.angle=90
                self.knight_pos_x=0.5
                self.knight_pos_y=-0.1
    def effect(self,game):
        pass
class Shield_effects(Widget):
    pass
class Shield_on_ground(Widget):
    def update(self,game):
        if self.collide_widget(game.knight):
            global shields
            self.type=shields[0]
            game.shield.remove_widget(game.shield.children[:])
            game.shield.add_widget(Builder.load_string('''
Shield_'''+str(self.type)+''':
'''))
            game.shield.type = self.type
            game.items_collection.remove_widget(self)
class Shield_Classic(Widget):
    is_pressed = BooleanProperty(False)
    def effect_down(self,game):
        pass
    def effect_up(self,game):
        pass
    def update(self,game):
        pass
class Shield_Bastion(Shield_Classic):
    def effect_down(self,game):
        self.is_pressed = True
        for x in range(4):
            if x == 0:
                angle = 0
                knight_pos_x=-0.1
                knight_pos_y=0.5
            elif x==1:
                angle = 0
                knight_pos_x=1.1
                knight_pos_y=0.5
            elif x==2:
                angle = 90
                knight_pos_x=0.5
                knight_pos_y=1.1
            elif x==3:
                angle = 90
                knight_pos_x=0.5
                knight_pos_y=-0.1
            game.shield_effects.add_widget(Builder.load_string('''
Shield:
    center_x:'''+str(game.knight.x+game.knight.width*knight_pos_x)+'''
    center_y:'''+str(game.knight.y+game.knight.height*knight_pos_y)+'''
    angle:'''+str(angle)+'''
    knight_pos_x:'''+str(knight_pos_x)+'''
    knight_pos_y:'''+str(knight_pos_y)+'''
    canvas.before:
        PushMatrix
        Rotate:
            angle:self.angle
            origin:self.center
    canvas.after:
        PopMatrix
'''))
    def effect_up(self,game):
        self.is_pressed = False
        while(game.shield_effects.children):
            for shield in game.shield_effects.children:
                game.shield_effects.remove_widget(shield)
    def update(self,game):
        if self.is_pressed:
            game.knight.speed_x=0
            game.knight.speed_y=0
            game.shield.angle = 0
            game.shield.knight_pos_x=1.1
            game.shield.knight_pos_y=0.5
            for shield in game.shield_effects.children:
                shield.center_x=game.knight.x+(game.knight.width*shield.knight_pos_x)
                shield.center_y=game.knight.y+(game.knight.height*shield.knight_pos_y)
                for archer in game.archers.children:
                    if shield.collide_widget(archer):
                        archer.self_collide_shield(game)
                    archer.chek_move(shield,game)
                for arrow in game.arrows.children:
                    if shield.collide_widget(arrow):
                        arrow.collide_shield(game)
            
class Archer(Widget):
    run_zone = ObjectProperty(None)
    def chek_move(self,some_object,game):
        if (self.run_zone.collide_widget(game.knight))or(self.run_zone.collide_widget(some_object)):
            if(Clock.get_time()-self.start_move)>=self.move_reload:
                self.move(game)
    def move(self,game):
        direct=random.randint(0,1)
        if direct:
            direct_=random.randint(0,1)
            self.speed_x=5+(-10*direct_)
            self.speed_y=1
        else:
            direct_=random.randint(0,1)
            self.speed_x=1
            self.speed_y=5+(-10*direct_)
        self.start_move = Clock.get_time()
    def attack(self,game):
        self.true_attack(game)
    def true_attack(self,game):
        arrow_center=self.center
        arrow_angle=math.degrees(math.atan2(game.knight.center_x-self.center_x,self.center_y-game.knight.center_y))
        arrow_speed_x = math.sin(math.radians(arrow_angle))*self.tipical_speed
        arrow_speed_y = math.cos(math.radians(arrow_angle))*-1*self.tipical_speed
        game.arrows.add_widget(Builder.load_string('''
'''+str(self.type_of_arrow)+'''
    center:'''+str(self.center)+'''
    speed_x:'''+str(arrow_speed_x)+'''
    speed_y:'''+str(arrow_speed_y)+'''
    canvas.before:
        PushMatrix
        Rotate:
            angle:'''+str(arrow_angle)+'''
            origin:self.center
    canvas.after:
	    PopMatrix
'''))
    def update(self,game):
        self.touch_wall=False
        for wall in game.walls.children:
            if wall.collide_widget(self):
                self.speed_x*=-1
                self.speed_y*=-1
                self.touch_wall = True
                break
        if (Clock.get_time()-self.start_move)<=self.move_time:
            if self.touch_wall:
                self.center_x=self.back_x+self.speed_x
                self.center_y=self.back_y+self.speed_y
            else:
                self.back_x=self.center_x
                self.back_y=self.center_y
                self.center_x+=self.speed_x
                self.center_y+=self.speed_y
        self.chek_move(game.shield,game)
        if (Clock.get_time()-self.last_attack_time)>=self.reload:
            self.last_attack_time=Clock.get_time()
            self.attack(game)

        if (self.collide_widget(game.knight)):
            self.self_collide_knight(game)
        if (self.collide_widget(game.shield)):
            self.self_collide_shield(game)
            if game.archers.children==[]:
                game.is_win=True
    def self_collide_knight(self,game):
        if (Clock.get_time()-self.self_last_attack_time)>=self.reload:
            game.hp_indicate.remove_widget(game.hp_indicate.children[0])
            game.knight.hp-=1
            self.self_last_attack_time=Clock.get_time()
    def self_collide_shield(self,game):
        if random.randint(0,100) <= self.coins_chance:
            game.items_collection.add_widget(Builder.load_string('''
Coin:
    center:'''+str(self.center)+'''
    cost:+'''+str(random.randint(self.cost_min,self.cost_max))+'''
'''))
        game.archers.remove_widget(self) 
class Run_zone(Widget):
    pass
class Arrow(Widget):
    def update(self,game):
        self.center_x+=self.speed_x
        self.center_y+=self.speed_y
        for wall in game.walls.children:
            if self.collide_widget(wall):
                self.collide(game)
        if self.collide_widget(game.shield):
            self.collide_shield(game)
        if self.collide_widget(game.knight):
            self.collide_knight(game)
    def collide(self,game):
        game.arrows.remove_widget(self)
    def collide_shield(self,game):
        self.collide(game)
    def collide_knight(self,game):
        game.hp_indicate.remove_widget(game.hp_indicate.children[0])
        game.knight.hp-=1
        self.collide(game)
class Spider(Archer):
    pass
class Web(Arrow):
    def collide(self,game):
        self.speed_x=0
        self.speed_y=0
    def collide_knight(self,game):
        self.collide(game)
        game.knight.speed_x=0
        game.knight.speed_y=0
    def collide_shield(self,game):
        game.arrows.remove_widget(self)
class Wall(Widget):
    pass
class Collection_of_effects(Widget):
    pass
class Poison_puddle(Widget):
    def knight_collide(self,game):
        if (Clock.get_time()-self.last_attack_time)>=self.reload:
            self.last_attack_time=Clock.get_time()
            self.true_attack(game)
    def update(self,game):
        if self.collide_widget(game.knight):
            self.knight_collide(game)
        if(Clock.get_time()-self.spawn_time)>=self.life_time:
            game.effects.remove_widget(self)
    def true_attack(self,game):
        game.knight.hp-=1
class Collection_of_archers(Widget):
    pass
class Collection_of_arrows(Widget):
    pass
class Collection_of_walls(Widget):
    pass
class Boss_spider(Archer):
    def attack(self,game):
        self.choose_attack(game)
    def choose_attack(self,game):
            self.type_attack = random.randint(1,3)
            if self.type_attack == 1:
                self.true_attack(game)
            elif self.type_attack == 2:
                self.web_spawn(game)
            else:
                self.spider_spawn(game)
    def web_spawn(self,game):
        self.web_speed_x=5
        self.web_speed_y=5
        for x in range(4):
            if x==1:
                web_speed_x=5
                web_speed_y=0
            elif x==2:
                web_speed_x=0
                web_speed_y=5
            elif x==3:
                web_speed_x=-5
                web_speed_y=0
            else:
                web_speed_x=0
                web_speed_y=-5
            web_builder_string = '''
Web:
    speed_x:'''+str(web_speed_x)+'''
    speed_y:'''+str(web_speed_y)+'''
    center:'''+str(self.center)+'''
'''
            game.arrows.add_widget(Builder.load_string(web_builder_string))
    def spider_spawn(self,game):
        while(self.available_spiders>0):
            game.archers.add_widget(Builder.load_string('''
Spider:
    center:'''+str(self.available_spiders*75)+''','''+str(self.available_spiders*75)+'''
'''))
            self.available_spiders-=1
        self.available_spiders=3
    def update(self,game):
        if (Clock.get_time()-self.last_attack_time)>=self.reload:
            self.last_attack_time=Clock.get_time()
            self.attack(game)
        if (self.collide_widget(game.knight)):
            self.self_collide_knight(game)
        if (self.collide_widget(game.shield)):
            self.self_collide_shield(game)
    def self_collide_shield(self,game):
        if game.shield.is_posioned:
            if random.randint(0,100) <= self.coins_chance:
                game.items_collection.add_widget(Builder.load_string('''
Coin:
    center:'''+str(self.center)+'''
    cost:+'''+str(random.randint(self.cost_min,self.cost_max))+'''
'''))
            game.archers.remove_widget(self) 
            if not(game.archers.children):
                game.is_win = True
        else:
            game.knight_chek_na_collide_wall=True
            game.knight.center_x=game.knight_back_center_x
            game.knight.center_y=game.knight_back_center_y
    def self_collide_knight(self,game):
        if (Clock.get_time()-self.self_last_attack_time)>=self.reload:
            game.hp_indicate.remove_widget(game.hp_indicate.children[0])
            game.knight.hp-=1
            self.self_last_attack_time=Clock.get_time()

class Poison_arrow(Arrow):
    def collide(self,game):
        game.effects.add_widget(Builder.load_string('''
Poison_puddle:
    center:'''+str(self.center)+'''
    spawn_time:'''+str(Clock.get_time())+'''
'''))
        game.arrows.remove_widget(self)
    def collide_shield(self,game):
        game.shield.is_posioned=True
        game.arrows.remove_widget(self)
class Web_collection(Widget):
    pass
class PathToTorlenApp(App):
    def build(self):
        game = KnightGame()
        Clock.schedule_once(game.on_start,0.1)
        Clock.schedule_interval(game.update,1.0/60.0)
        return game
if __name__=='__main__':
    PathToTorlenApp().run()
