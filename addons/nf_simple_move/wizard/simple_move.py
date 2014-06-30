# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime
import openerp.addons.decimal_precision as dp

class simple_move(osv.osv_memory):
    _name="nf_simple_move.wiz.simple_move"
    _description="simple Move"
    _columns = {
                'name': fields.char('Name', size=64, required=True),
                'journal_id': fields.many2one("account.journal","Journal",required=True,domain=[('journal_type','=','general')]),
                'period_id': fields.many2one("account.period","Period",required=True),
                'date': fields.date("Date",required=True),
                'move_id': fields.many2one("account.move","Move"),
                'tax_id':fields.many2one('account.tax', 'Tax'),
                'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
                'currency_id': fields.many2one('res.currency', 'Currency', help="The optional other currency if it is a multi-currency entry."),
                'credit_account_id': fields.many2one('account.account', 'Credit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                'debit_account_id': fields.many2one('account.account', 'Debit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                
                }
    
    def _get_default_date(self,cr,uid,ids,context={}):
        return None
    
    _defaults = {
        'date': _get_default_date,
        'amount': 0.0,
    }


    def get_period_from_date(self,cr,uid,ids,date,period_id,context={}):
        period_obj=self.pool.get("account.period")
        return period_obj.find(cr,uid,date,context)
        
    def action_validate_close(self,cr,uid,ids,context={}):
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
    
        
simple_move()