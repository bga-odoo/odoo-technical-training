# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError

from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class Appearance(models.Model):
    _name ='appearance'
    _description = "Appearances"

    is_paid = fields.Boolean(string="Is paid", default = False)
    player_id = fields.Many2one('res.partner', string="Player")
    game_id = fields.Many2one('game', string="Game")
    player_win_bonus = fields.Float(related='player_id.win_bonus', string="Win Bonus")
    player_draw_bonus = fields.Float(related='player_id.draw_bonus', string="Draw Bonus")
    player_lost_bonus = fields.Float(related='player_id.lost_bonus', string="Lost Bonus")
    game_date = fields.Date(related='game_id.date', string="Game date")
    game_state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Validated'), ('done', 'Done')], related="game_id.state", string="Game status")


    def action_create_appearance_invoice(self):
        #context = dict(env.context) 
        #appearances = env['appearance'] 
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return ''

        else:
            for record in self.env['appearance'].browse(self._context.get('active_ids')):
                if record.is_paid is False and record.game_state == 'confirmed':
                    bonus = {
                        'won': record.player_id.win_bonus,
                        'draw': record.player_id.draw_bonus,
                        'lost': record.player_id.lost_bonus,
                        }.get(record.game_id.result, 0)

                    invoice = self.env['account.move'].create({
                        'partner_id': record.player_id.id,
                        'date': datetime.now(),
                        'journal_id': 2,
                        'game_id': record.game_id.id,
                        #'name': self.env['ir.sequence'].next_by_code(sequence_code),
                        'state': 'draft',
                        'type': 'in_invoice',
                        'invoice_line_ids': [(0, 0, {
                            'product_id': self.env.ref('foot.product_product_prime').id,
                            'price_unit': bonus,
                            'quantity': 1,
                            'name': record.game_id.name,
                            'game_id': record.game_id.id
                        })],
                    })

                    record.write({
                        'is_paid': True,
                    })
                else:
                    raise ValidationError("At least an appearance is paid or a game is not confirmed")
                all_paid = 1
                for appearance in record.game_id.appearance_ids:
                    if appearance.is_paid is False:
                        all_paid = 0
                        break
                if all_paid == 1:
                    record.game_id.write({
                        'state': 'done',
                    })