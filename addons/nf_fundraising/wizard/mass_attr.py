# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import pooler

class wiz_mass_attr(osv.osv_memory):
    _name="nf_fundraising.wiz.massattr"
    _description="Ajouter une attribution"
    
    def action_attr(self,cr, uid, ids, context):
        context['import_mode']=True
        myself=self.browse(cr,uid,ids)[0]
        pool_obj=pooler.get_pool(cr.dbname)
        partner_obj=pool_obj.get("res.partner")
        cat_ids=[]
        for tag in myself.attribution_ids:
            cat_ids.append((4,tag.id))
        partner_obj.write(cr,uid,context['active_ids'],{'attribution_ids':cat_ids},context=context)
        return {}
    
    def action_unattr(self,cr, uid, ids, context):
        context['import_mode']=True
        myself=self.browse(cr,uid,ids)[0]
        pool_obj=pooler.get_pool(cr.dbname)
        partner_obj=pool_obj.get("res.partner")
        cat_ids=[]
        for tag in myself.attribution_ids:
            cat_ids.append((3,tag.id))
        partner_obj.write(cr,uid,context['active_ids'],{'attribution_ids':cat_ids},context=context)
        return {}
    
    _columns = {
        'attribution_ids': fields.many2many('nf_fundraising.attribution','wiz_massattr_attr_rel','attr_id','wiz_id', 'Attributions', required=True),
               }
    _defaults = {
                  }
    
wiz_mass_attr()


