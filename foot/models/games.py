# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class Game(models.Model):
    _name ='game'
    _description = "Games"

    name = fields.Char(string="Name", required="1", readonly="1", compute="_get_game_name")
    home_team_id = fields.Many2one('team', required="1", string="Home Team")
    away_team_id = fields.Many2one('team', required="1", string="Away Team")
    date = fields.Date(string="Date")
    player_ids = fields.Many2many('res.partner', string="Players for this game")
    result = fields.Selection([('won', 'Won'), ('draw', 'Draw'), ('lost', 'Lost')],string="Result for my team")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Validated'), ('done', 'Done')], string="Status", default='draft')
    game_cost = fields.Float(string="Game cost", readonly="1", compute="_get_game_cost")
    invoice_ids = fields.One2many('account.move', 'game_id', string = "Invoices")
    invoice_count = fields.Integer(string="Number of invoices", compute="_get_invoice_count")
    appearance_ids = fields.One2many('appearance', 'game_id', string="Appearances")

    def action_confirm(self):
        self.write({
            'state': 'confirmed',
        })

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

    @api.depends('result', 'appearance_ids')
    def _get_game_cost(self):
        for record in self:
            game_cost = 0
            if record.result == 'won':
                for player in record.appearance_ids:
                    game_cost += player.player_id.win_bonus
            elif record.result == 'draw':
                for player in record.appearance_ids:
                    game_cost += player.player_id.draw_bonus
            elif record.result == 'lost':
                for player in record.appearance_ids:
                    game_cost += player.player_id.lost_bonus       
            record['game_cost'] = game_cost

    @api.depends('invoice_ids')
    def _get_invoice_count(self):
        for record in self:
            record['invoice_count'] = len(record.invoice_ids)

    def create_invoice_game(self):
        for record in self:
            sequence_code = 'account.payment.supplier.invoice'
            for player in record.player_ids:
                bonus = {
                    'won': player.win_bonus,
                    'draw': player.draw_bonus,
                    'lost': player.lost_bonus,
                    }.get(record.result, 0)
            # if record.result == 'won':
            #     game_status = 1
            # elif record.result == "draw":
            #     game_status = 2
            # elif record.result == "lost":
            #     game_status = 3
            
            #     if game_status == 1:
            #         bonus = player.win_bonus
            #     elif game_status == 2:
            #         bonus = player.draw_bonus
            #     elif game_status == 3:
            #         bonus = player.lost_bonus
                invoice = self.env['account.move'].create({
                    'partner_id':player.id,
                    'date':datetime.now(),
                    'journal_id':2,
                    'game_id':record.id,
                    #'name': self.env['ir.sequence'].next_by_code(sequence_code),
                    'state':'draft',
                    'type':'in_invoice',
                    'invoice_line_ids': [(0, 0, {
                        'product_id':self.env.ref('foot.product_product_prime').id,
                        'price_unit':bonus,
                        'quantity': 1,
                        'name':record.name,
                    })],
                })

            # change the game status

            record.write({
                'state': 'done',
            })

                # for invoice_line in invoice.line_ids:
                #     if invoice_line.price_subtotal == 0.0:
                #         invoice_line.unlink()

    def action_view_game_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_in_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'in_invoice',
        }
        # if len(self) == 1:
        #     context.update({
        #         'default_partner_id': self.partner_id.id,
        #         'default_partner_shipping_id': self.partner_shipping_id.id,
        #         'default_invoice_payment_term_id': self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
        #         'default_invoice_origin': self.mapped('name'),
        #         'default_user_id': self.user_id.id,
        #     })
        # action['context'] = context
        return action

        #Set game to draft
    def set_game_draft(self):
        for record in self:
            if len(record.invoice_ids) > 0:
                invoice_confirmed = 0
                for invoice in record.invoice_ids:
                    if invoice.state == 'posted' or invoice.state == 'cancel':
                        invoice_confirmed = 1
                        continue
                if invoice_confirmed == 0:
                    for invoices in record.invoice_ids:
                        invoices.unlink()
                    record.write({
                        'state': 'draft',
                    })
                else:
                    raise ValidationError("At least one invoice linked to this game has been posted")
            else:
                record.write({
                    'state': 'draft',
                })
                        



