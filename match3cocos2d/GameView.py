import time

import cocos
from cocos.director import director
from cocos.scene import Scene
from match3cocos2d.HUD import HUD, BackgroundLayer
from match3cocos2d.GameModel import GameModel
from match3cocos2d.GameController import GameController
from match3cocos2d.db_models import *

__all__ = ['get_newgame']


class GameView(cocos.layer.ColorLayer):
    is_event_handler = True  #: enable director.window events

    def __init__(self, model, hud, bg_layer):
        super(GameView, self).__init__(64, 64, 224, 0)
        model.set_view(self)
        self.hud = hud
        self.model = model
        self.bg_layer = bg_layer
        self.model.push_handlers(self.on_update_objectives,
                                self.on_update_time,
                                self.on_game_over,
                                self.on_game_win,
                                self.on_level_start,
                                self.on_level_completed)
        self.model.start()
        self.hud.set_objectives(self.model.objectives)
        # self.hud.show_message('GET READY')

    def on_update_objectives(self):
        self.hud.set_objectives(self.model.objectives)

    def on_update_time(self, time_percent):
        self.hud.update_time(time_percent)

    def on_game_over(self):
        self.hud.show_message('Вы проиграли', msg_duration=3, callback=lambda: director.pop())

    def on_game_win(self):
        self.hud.show_message('Вы прошли игру', msg_duration=3, callback=lambda: director.pop())

    def on_level_start(self):
        session = Session()
        # level = session.query(Level).filter_by(
        #     id=self.model.level.id + 1).first()
        self.bg_layer.set_image(self.model.level.background)
        session.close()
        self.hud.show_message(self.model.level.name, msg_duration=3, callback=lambda: self.show_description())
        # self.hud.show_message(self.model.level.description, msg_duration=3)

    def show_description(self):
        if self.model.level.description:
            if len(self.model.level.description) > 50:
                self.hud.show_message(self.model.level.description, msg_duration=3, font=13)
            else:
                self.hud.show_message(self.model.level.description, msg_duration=3)


    def on_level_completed(self):

        self.hud.show_message('Уровень пройден!', msg_duration=3,
            callback=lambda: self.model.set_next_level())


def get_newgame():
    scene = Scene()
    model = GameModel()
    controller = GameController(model)
    # view
    hud = HUD()
    bg_layer = BackgroundLayer('backgrounds/bg1.jpg')
    view = GameView(model, hud, bg_layer)

    # set controller in model
    model.set_controller(controller)

    # add controller
    scene.add(controller, z=1, name="controller")
    scene.add(bg_layer, z=0, name="bg")
    scene.add(hud, z=3, name="hud")
    scene.add(view, z=2, name="view")

    return scene
