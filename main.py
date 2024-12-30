from pyray import *
import math
from data import *



class Game(Engine):
    def init(self, window_size_x, window_size_y, name, use_y_index = False):
        super().init(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)

        self.scena = Scena("Cartas")
        self.scena.use_y_index = False


        self.player = ModelBasic(parent=self.scena, position=Vector2(400, 400))

    def Update(self, dt):

        if self.player : 
            dir = Vector2(
                int(is_key_down(KEY_D)) - int(is_key_down(KEY_A)), 
                int(is_key_down(KEY_S)) - int(is_key_down(KEY_W)), 
            )

            dir = vector2_normalize(dir)

            self.player.position.x += dir.x * 200 * dt
            self.player.position.y += dir.y * 200 * dt

            if is_key_pressed(KEY_X) : 
                self.player.Delect()
                self.player = None

        return super().Update(dt)

    def Draw(self):


        return super().Draw()

    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()


app = Game(window_size_x=800, window_size_y=800, name="Hola Mundo", use_y_index=True)
app.Run()