# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime


class gift_attribution(osv.osv):
    _name = "nf_fundraising.gift.attribution"
    _table = "nf_fundraising_gift_attribution"
   
    def _get_store_ids(self,cr,uid,ids,context={}):
        gift_attr_obj = self.pool.get("nf_fundraising.gift.attribution")
        if self._name=="nf_fundraising.gift":
            return gift_attr_obj.search(cr,uid,[('gift_id','in',ids)])
        if self._name=="account.move":
            gift_obj = self.pool.get("nf_fundraising.gift")
            gift_ids = gift_obj.search(cr,uid,[('move_id','in',ids)])
            return gift_attr_obj.search(cr,uid,[('gift_id','in',gift_ids)])

#     def create(self,cr,uid,values,context={}):
#         if 'bygift' not in context:
#             raise osv.except_osv('Erreur!', u"Vous devez créer un don pour créer une attribution")
#         return super(res_partner,self).create(cr,uid,vals,context)

    
    _columns = {
                'amount': fields.float("montant",required=True),
                'gift_id': fields.many2one("nf_fundraising.gift","Don",ondelete="restrict",select=True, required=True),
                'attribution_id': fields.many2one("nf_fundraising.attribution","Attribution",ondelete="restrict",select=True, required=True),
                'partner_id': fields.related("gift_id","partner_id",type='many2one', string='Partner', relation='res.partner',readonly=True,store={
                                                                                                                                                   'nf_fundraising.gift': (_get_store_ids,['partner_id'],10)
                                                                                                                                                   }),
                'date':  fields.related('gift_id','date', type='date', string="Date", readonly=True,store={
                                                                                                                   'nf_fundraising.gift': (_get_store_ids,['date'],10)
                                                                                                                   }),
                'journal_id':  fields.related('gift_id','journal_id', type='many2one', string="Journal",relation="account.journal", readonly=True,store={
                                                                                                                   'nf_fundraising.gift': (_get_store_ids,['journal_id'],10)
                                                                                                                   }),
                'solicitation_id': fields.related('gift_id','solicitation_id', type='many2one', string="Solicitation",relation="nf_fundraising.solicitation", readonly=True,store={
                                                                                                                   'nf_fundraising.gift': (_get_store_ids,['solicitation_id'],10)
                                                                                                                   }),
                'period_id':  fields.related('gift_id','move_id','period_id', type='many2one', string=u"Période",relation="account.period", readonly=True,store={
                                                                                                                   'account.move': (_get_store_ids,['period_id'],10)
                                                                                                                   }),
                'state': fields.related('gift_id', 'state', type='selection', selection=[('draft', 'Brouillon'), ('valid', 'Validé')], string=u'État', readonly=True,store={
                                                                                                                   'nf_fundraising.gift': (_get_store_ids,['state'],10)
                                                                                                                   }),
                
                }
    
gift_attribution()

class attribution(osv.osv):
    _name = 'nf_fundraising.attribution'


    def state_closed(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'closed'})
        return {}

    def state_draft(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'draft'})
        return {}

    def state_open(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'open'})
        return {}



    def get_all_gifts(self,cr,uid,ids,field_names,arg,context):
        ret={}
        giftattr_obj=self.pool.get("nf_fundraising.gift.attribution")
        for attribution in self.browse(cr,uid,ids):
            last_date=False
            total=0.0
            giftattr_ids=giftattr_obj.search(cr,uid,[('attribution_id','=',attribution.id),('gift_id.state','=','valid')])
            for giftattr in giftattr_obj.browse(cr,uid,giftattr_ids):
                total+=giftattr.amount
                if not last_date or last_date < giftattr.date:
                    last_date=giftattr.date
            ret[attribution.id]={'total_dons':total,'dernier_don':last_date}
        return ret
    
    
    def is_gift_attribution(self,cr,uid,ids,context={}):
        #get all partners
        gift_obj=self.pool.get("nf_fundraising.gift")
        attribution_ids=[]
        for gift in gift_obj.browse(cr,uid,ids):
            for gattr in gift.attribution_ids:
                if gattr.attribution_id.id not in attribution_ids:
                    attribution_ids.append(gattr.attribution_id.id) 
        return attribution_ids

    store_gifts = {
                   'nf_fundraising.gift':(
                                  is_gift_attribution,
                                  ['state','amount','date','partner_id'],
                                  5
                                  )
                   }

    _columns = {
        'state': fields.selection((("draft","Brouillon"),("open","Ouverte"),("closed","Fermée")),u"État",readonly=True),
        'name': fields.char('Nom',required=True),
        'description': fields.text('Description'),
        'active': fields.boolean("Active"),
        'account_id': fields.many2one('account.account','Compte de débit',ondelete="restrict",select=True, required=True),
        'partner_ids': fields.many2many("res.partner","nf_fundraising_attribution_partner_rel","attribution_id","partner_id",u'Attributions à solliciter',ondelete="restrict",select=True, required=True),
        'total_dons': fields.function(get_all_gifts,string=u'Total des dons',method=True,type="float",multi="pgift",store=store_gifts),
        'dernier_don': fields.function(get_all_gifts,string=u'Dernier don',method=True,type="date",multi="pgift",store=store_gifts),

    }
    _defaults ={
                'active':True,
                'state':'draft',
                }
    

    def open_attribution_view(self,cr,uid,ids,context={}):
        if "search_default_unclosed" in context:
            del(context['search_default_unclosed'])
        context['search_default_closed']=1
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attribution',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift.attribution',
            'src_model': 'nf_fundraising.attribution',
            'nodestroy': 'true',
            'domain':[('attribution_id','=',ids[0])],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
        
attribution()
