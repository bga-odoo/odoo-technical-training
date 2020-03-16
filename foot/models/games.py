# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Game(models.Model):
    _name ='game'
    _description = "Games"

    name = fields.Char(string="Name", required="1", readonly="1", compute="_get_game_name")

    @api.depends('home_team_id', 'away_team_id')
    def _get_game_name(self):
        for record in self:
            if record.home_team_id and record. away_team_id:
                name = record.home_team_id.name + " VS " + record.away_team_id.name
            elif record.home_team_id:
                name = record.home_team_id.name
            elif record.away_team_id:
                name = record.away_team_id
            else:
                name = "No team defined"
            record['name'] = name
    


    home_team_id = fields.Many2one('team', required="1", string="Home Team")
    away_team_id = fields.Many2one('team', required="1", string="Away Team")
    date = fields.Date(string="Date")
    player_ids = fields.Many2many('res.partner', string="Players for this game")
    result = fields.Selection([('won', 'Won'), ('draw', 'Draw'), ('lost', 'Lost')],string="Result for my team")