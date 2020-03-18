# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):

    _inherit = 'res.partner'

    player = fields.Boolean(string="Player")
    coach = fields.Boolean(string="Coach")
    foot_team_id = fields.Many2one('team', ondelete='set null', string="Team")
    win_bonus = fields.Float(string="Win bonus")
    draw_bonus = fields.Float(string="Draw bonus")
    lost_bonus = fields.Float(string="Lost bonus")
    game_ids = fields.Many2many('game', string="Games")
    appearance_ids = fields.One2many('appearance', 'player_id', string="Appearances")
    appearance_count = fields.Integer(string="Number of Appearances", compute="_get_appearance_count")

    @api.depends('appearance_ids')
    def _get_appearance_count(self):
        for record in self:
            record['appearance_count'] = len(record.appearance_ids)

    def action_view_appearance(self):
        appearance = self.mapped('appearance_ids')
        action = self.env.ref('foot.action_appearance').read()[0]
        if len(appearance) > 1:
            action['domain'] = [('id', 'in', appearance.ids)]
        elif len(appearance) == 1:
            form_view = [(self.env.ref('foot.appearance_form_view').id, 'form')]
            action['views'] = form_view
            action['res_id'] = appearance.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


