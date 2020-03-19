# -*- coding: utf-8 -*-

from odoo import models, fields

class Partner(models.Model):

    _inherit = 'account.move.line'

    appearance_id = fields.Many2one('appearance', string="Appearance")
    game_id = fields.Many2one('game', string="Game")