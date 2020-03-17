# -*- coding: utf-8 -*-

from odoo import models, fields

class Partner(models.Model):

    _inherit = 'res.partner'

    player = fields.Boolean(string="Player")
    coach = fields.Boolean(string="Coach")
    foot_team_id = fields.Many2one('team', ondelete='set null', string="Team")
    win_bonus = fields.Float(string="Win bonus")
    draw_bonus = fields.Float(string="Draw bonus")
    lost_bonus = fields.Float(string="Lost bonus")
    game_ids = fields.Many2many('game', string="Games")
