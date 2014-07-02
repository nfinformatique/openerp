# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime
import openerp.addons.decimal_precision as dp

class simple_move(osv.osv_memory):
    _name="nf_simple_move.wiz.simple_move"
    _description="simple Move"
    _columns = {
                'name': fields.char('Name', size=64, required=True),
                'journal_id': fields.many2one("account.journal","Journal",required=True),#,domain=[('journal_type','=','general')]),
                'period_id': fields.many2one("account.period","Period",required=True),
                'date': fields.date("Date",required=True),
                'move_id': fields.many2one("account.move","Move"),
                'account_tax_id':fields.many2one('account.tax', 'Tax'),
                'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
                'currency_id': fields.many2one('res.currency', 'Currency', help="The optional other currency if it is a multi-currency entry."),
                'credit_account_id': fields.many2one('account.account', 'Credit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                'debit_account_id': fields.many2one('account.account', 'Debit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                'company_id': fields.related('journal_id', 'company_id', type='many2one', relation='res.company', string='Company', store=False, readonly=True),
                }
    
    def _get_default_date(self,cr,uid,context={}):
        date=None
        period_obj=self.pool.get("account.period")
        if 'journal_id' in context and 'period_id' in context:
            cr.execute('''SELECT move_id, date FROM account_move_line
                        WHERE journal_id = %s AND period_id = %s
                         ORDER BY date DESC limit 1''', (context['journal_id'], context['period_id']))
            res = cr.fetchone()
            date = res and res[1] or period_obj.browse(cr, uid, context['period_id'], context=context).date_start
        
        return date
    
    def _get_default_journal(self,cr,uid,context={}):
        if 'journal_id' in context:
            return context['journal_id']
        return False
    
    def _get_default_company(self,cr,uid,context={}):
        if 'journal_id' in context:
            return  self.pool.get("account.journal").browse(cr,uid,context['journal_id'],context=context).company_id.id
        return False
    
    def _get_default_period(self,cr,uid,context={}):
        if 'period_id' in context:
            return context['period_id']
        return False
    
    def _get_default_credit_account(self,cr,uid,context={}):
        return False
    def _get_default_debit_account(self,cr,uid,context={}):
        return False
    
    _defaults = {
        'date': _get_default_date,
        'journal_id': _get_default_journal,
        'period_id': _get_default_period,
        'credit_account_id' : _get_default_credit_account,
        'debit_account_id' : _get_default_debit_account,
        'amount': 0.0,
        'company_id': _get_default_company,
    }


    def get_period_from_date(self,cr,uid,ids,date,period_id,context={}):
        period_obj=self.pool.get("account.period")
        return period_obj.find(cr,uid,date,context)
        
    def basic_check(self,cr,uid,ids):
        return True
        
    def create_entries(self,cr,uid,ids,context={}):
        move_line_obj=self.pool.get("account.move.line")
        for wiz in self.browse(cr,uid,ids,context=context):
            #create entry with debit
            move=wiz.move_id or False
            if move:
                for line in move.line_id:
                    line.unlink(cr,uid) 
            vals={
                  'name': wiz.name,
                  'debit':wiz.amount,
                  'credit':0.0,
                  'account_id':wiz.debit_account_id.id,
                  'move_id':move and move.id or False,
                  'journal_id':wiz.journal_id.id,
                  'period_id':wiz.period_id.id,
                  'date':wiz.date,
                  }
            id=move_line_obj.create(cr,uid,vals,context=context)
            if not move:
                move_line = move_line_obj.browse(cr,uid,id)
                move=move_line.move_id
            #create entry with credit
            vals={
                  'name': wiz.name,
                  'debit':0.0,
                  'credit':wiz.amount,
                  'account_id':wiz.credit_account_id.id,
                  'move_id':move.id,
                  'journal_id':wiz.journal_id.id,
                  'period_id':wiz.period_id.id,
                  'date':wiz.date,
                  'account_tax_id':wiz.account_tax_id.id,
                  }
            id=move_line_obj.create(cr,uid,vals,context=context)
            wiz.unlink(cr,uid)
        return {}
        
    def action_validate_close(self,cr,uid,ids,context={}):
        self.create_entries(cr,uid,ids,context=context)
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
    
    def action_validate_new(self,cr,uid,ids,context={}):
        self.create_entries(cr,uid,ids,context=context)
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
    
    def on_change_date(self,cr,uid,ids,date,context={}):
        period_obj=self.pool.get("account.period")

        return {}
    def on_change_credit_account(self,cr,uid,ids,credit_account_id,account_tax_id,context={}):
        if not account_tax_id:
            move_line_obj=self.pool.get("account.move.line")
            return move_line_obj.onchange_account_id(cr,uid,ids,credit_account_id,context=context)
        return {}
    def on_change_debit_account(self,cr,uid,ids,debit_account_id,account_tax_id,context={}):
        if not account_tax_id:
            move_line_obj=self.pool.get("account.move.line")
            return move_line_obj.onchange_account_id(cr,uid,ids,debit_account_id,context=context)
        return {}
        
simple_move()