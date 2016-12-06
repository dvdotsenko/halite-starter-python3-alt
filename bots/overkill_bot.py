from bots.parts.base_timed import BaseTimedBot

from bots.models import Frame
from bots.models import VectorTransform, Move
from bots.models import Enemy


MAX_CELL_STRENGTH = 255


class OverkillBot(BaseTimedBot):

    @staticmethod
    def find_nearest_enemy_direction(cell, frame):
        max_distance = round(min(frame.w, frame.h) / 2)
        # we are here because we could not find a direct enemy to attack
        # hence 2 steps away to start with.
        for distance in range(2, max_distance):
            for x, y in VectorTransform.DIRECT:
                vector = x*distance, y*distance
                enemy_cell = frame.shift(cell, vector)
                if not frame.is_me(enemy_cell):
                    return vector

    @staticmethod
    def enemy_assessment(enemy, attack_strength, frame):
        # this is supposed to be `heuristic` function from
        # http://forums.halite.io/t/so-youve-improved-the-random-bot-now-what/482
        # but it made little sense when it came to returned value - provided uncomparable values.
        # Massaged it a bit to keep return value in same scale
        # See https://halite.io/rules_game.php Overkill section
        prod = frame.production[enemy.cell]
        if not enemy.is_neutral:
            # pad production gain by enemy's additional loses on the field
            # (it's like if we have produced that much extra strength and
            #  expensed it on destruction of the enemy)
            prod += sum(
                min(frame.strength[neighbor_cell], attack_strength)
                for neighbor_cell in frame.shift_many(enemy.cell, *VectorTransform.DIRECT)
                if frame.ownership[neighbor_cell] == enemy.player_id
            )

        if enemy.strength > 0:
            return prod / enemy.strength
        else:
            return prod


    @classmethod
    def process_move(cls, move, frame):
        """
        don't need to return anything
        just change the `.vector` on the move to some direction.
        don't need to change it to STAY. It's that by default

        :param Move move:
        :param Frame frame:
        """

        attack_strength = frame.strength[move.cell]

        neighbor_enemy_cells = {
            neighbor_cell
            for neighbor_cell in frame.shift_many(move.cell, *VectorTransform.DIRECT)
            if not frame.is_me(neighbor_cell)
        }

        nearby_enemies = [
            Enemy.get_by_cell(cell, frame)
            for cell in neighbor_enemy_cells
            if frame.strength[cell] < attack_strength
        ]

        if nearby_enemies:
            enemy = max(
                nearby_enemies,
                key=lambda e: cls.enemy_assessment(e, attack_strength, frame)
            )
        else:
            enemy = None

        if enemy:
            move.vector = frame.get_vector(move.cell, enemy.cell)
            return # all move objects are changed by reference and are already in the move set

        if not neighbor_enemy_cells and attack_strength > frame.production[move.cell]*4: # produced enough to move to some far-away enemy
            vector = cls.find_nearest_enemy_direction(move.cell, frame)
            if vector:
                move.vector = frame.compute_move_along(move.cell, vector)
                return # all move objects are changed by reference and are already in the move set

    async def calculate_moves(self, frame):
        """
        :param Frame frame:
        :return:
        """
        for move in frame.moves:
            self.process_move(move, frame)

    async def calculate_global_objectives(self, frame):
        # for i in range(20):
        #     await yld(1)
        #     log('Calculate Flags second {}'.format(i))
        return

