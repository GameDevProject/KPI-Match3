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
                                self.on_level_completed)
        self.model.start()
        self.hud.set_objectives(self.model.objectives)
        self.hud.show_message('GET READY')

    def on_update_objectives(self):
        self.hud.set_objectives(self.model.objectives)

    def on_update_time(self, time_percent):
        self.hud.update_time(time_percent)

    def on_game_over(self):
        self.hud.show_message('GAME OVER', msg_duration=3, callback=lambda: director.pop())

    def on_level_completed(self):
        session = Session()
        level = session.query(Level).filter_by(id=self.model.level.id + 1).first()
        self.bg_layer.set_image(level.background)
        session.close()
        self.hud.show_message('LEVEL COMPLETED', msg_duration=3,
            callback=lambda: self.model.set_next_level())



def get_newgame():
    scene = Scene()
    model = GameModel()
    controller = GameController(model)
    # view
    hud = HUD()
    bg_layer = BackgroundLayer('bg1.jpg')
    view = GameView(model, hud, bg_layer)

    # set controller in model
    model.set_controller(controller)

    # add controller
    scene.add(controller, z=1, name="controller")
    scene.add(bg_layer, z=0, name="bg")
    scene.add(hud, z=3, name="hud")
    scene.add(view, z=2, name="view")

    return scene
