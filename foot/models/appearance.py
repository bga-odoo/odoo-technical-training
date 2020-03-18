# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class Game(models.Model):
    _name ='appearance'
    _description = "Appearances"

    is_paid = fields.Boolean(string="Is paid", default = False)
    player_id = fields.Many2one('res.partner', string="Player")
    game_id = fields.Many2one('game', string="Game")
    player_win_bonus = fields.Float(related='player_id.win_bonus', string="Win Bonus")
    player_draw_bonus = fields.Float(related='player_id.draw_bonus', string="Draw Bonus")
    player_lost_bonus = fields.Float(related='player_id.lost_bonus', string="Lost Bonus")
    game_date = fields.Date(related='game_id.date', string="Game date")
