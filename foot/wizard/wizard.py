from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'playerswizard'
    _description = "Wizard: Quick Registration of Players to games"

    def _default_game(self):
        return self.env['game'].browse(self._context.get('active_id'))

    game_ids = fields.Many2many('game', string="Games", required=True, default=_default_game)
    player_ids = fields.Many2many('res.partner', string="Players")

    def subscribe(self):
        for game in self.game_ids:
           game.player_ids |= self.player_ids
        return {}