# -*- coding: utf-8 -*-

from odoo import models, fields

class Team(models.Model):
    _name ='team'
    _description = "Teams"

    name = fields.Char(string="Name", required="1")
    coach_id = fields.Many2one('res.partner', string="Coach")
    player_ids = fields.One2many('res.partner', 'foot_team_id', string="Players")
    matricule = fields.Char(string="Matricule")