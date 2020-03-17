# -*- coding: utf-8 -*-

from odoo import models, fields

class Partner(models.Model):

    _inherit = 'account.move'

    game_id = fields.Many2one('game', string="Player")