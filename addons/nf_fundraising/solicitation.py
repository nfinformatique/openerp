# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime

    
class solicitation(osv.osv):
    _name = 'nf_fundraising.solicitation'
    
    def onchange_type(self,cr,uid,ids,type_id):
        res={}
        if not type_id is None:
            type_obj=self.pool.get("nf_fundraising.solicitation.type")
            type=type_obj.browse(cr,uid,type_id)
            res['value']={'debit_account_id':type.debit_account_id}
        return res
    
    def close(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'closed'})
        return {}
    
    def reopen(self,cr,uid,ids,context={}):
        assert len(ids)==1
        self.write(cr,uid,ids,{'state':'listed'})
        return {}

    def list_partners(self,cr,uid,ids,context={}):
        assert len(ids)==1
        context['import_mode']=True
        id=ids[0]
        sol = self.browse(cr,uid,id)
        #select all partners with any of the attribution
        partner_obj=self.pool.get("res.partner")
        attr_ids=[]
        for attr in sol.attribution_ids:
            attr_ids.append(attr.id)
        partner_ids=partner_obj.search(cr,uid,[('active','=',True),('attribution_ids','in',attr_ids)])
        for partner in partner_obj.browse(cr,uid,partner_ids):
            partner.write({'solicitation_ids':[(4,id)]},context=context)
        self.write(cr,uid,ids,{'state':'listed'})
        return {}
    
    def open_list(self,cr,uid,ids,context={}):
        assert len(ids)==1
        id=ids[0]
        sol = self.browse(cr,uid,id)
        attr_ids=[]
        for attr in sol.attribution_ids:
            attr_ids.append(attr.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Liste d\'envoi pour %s'%sol.name,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'res.partner',
            'src_model': 'nf_fundraising.solicitation',
            'nodestroy': 'true',
            'domain':[('active','=',True),('attribution_ids','in',attr_ids)],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
    

    def get_all_gifts(self,cr,uid,ids,field_names,arg,context):
        ret={}
        for solicitation in self.browse(cr,uid,ids):
            last_date=False
            total=0.0
            for gift in solicitation.gift_ids:
                if gift.state=="valid":
                    total+=gift.amount
                    if not last_date or last_date < gift.date:
                        last_date=gift.date
            ret[solicitation.id]={'total_dons':total,'dernier_don':last_date}
        return ret
    
    
    def is_gift_solicitation(self,cr,uid,ids,context={}):
        #get all partners
        gift_obj=self.pool.get("nf_fundraising.gift")
        solicitation_ids=[]
        for gift in gift_obj.browse(cr,uid,ids):
            if gift.solicitation_id.id not in solicitation_ids:
                solicitation_ids.append(gift.solicitation_id.id) 
        return solicitation_ids
    
    store_gifts = {
                   'nf_fundraising.gift':(
                                  is_gift_solicitation,
                                  ['state','amount','date','partner_id'],
                                  5
                                  )
                   }    
    
    _columns = {
        'description': fields.text('Description'),
        'state': fields.selection((("draft","Brouillon"),("listed","Listée"),("closed","Fermé")),u"État"),
        
#        'listed': fields.boolean('Liste créée'),
        'name': fields.char('Nom',required=True),
        'date': fields.date(u"Date",required=True),
        'partner_ids': fields.many2many('res.partner','nf_fundraising_solicitation_partner_rel','solicitation_id','partner_id','Donateurs',domain="[]"),
        'attribution_ids': fields.many2many("nf_fundraising.attribution","nf_fundraising_attribution_solicitation_rel","solicitation_id","attribution_id",u'Attributions',ondelete="restrict",select=True, required=True),
#        'journal_id': fields.many2one("account.journal","Journal",ondelete="restrict",select=True, required=True),
        'gift_ids': fields.one2many("nf_fundraising.gift","solicitation_id","Dons"),
        'total_dons': fields.function(get_all_gifts,string=u'Total des dons',method=True,type="float",multi="pgift",store=store_gifts),
        'dernier_don': fields.function(get_all_gifts,string=u'Dernier don',method=True,type="date",multi="pgift",store=store_gifts),

    }
    _defaults ={
                'state':'draft',
                }
    

    def open_gift_view(self,cr,uid,ids,context={}):
        if "search_default_unclosed" in context:
            del(context['search_default_unclosed'])
        context['search_default_closed']=1
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dons',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift',
            'src_model': 'nf_fundraising.solicitation',
            'nodestroy': 'true',
            'domain':[('solicitation_id','=',ids[0])],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
    def open_attribution_view(self,cr,uid,ids,context={}):
        if "search_default_unclosed" in context:
            del(context['search_default_unclosed'])
        context['search_default_closed']=1
        context['search_default_gbyattribution']=1
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attribution',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift.attribution',
            'src_model': 'nf_fundraising.solicitation',
            'nodestroy': 'true',
            'domain':[('gift_id.solicitation_id','=',ids[0])],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
    
solicitation()    