# file: Unicode1.py
# -*- coding: utf-8 -*-


import wizard
import pooler
from osv import fields,osv
#import hc_common
#from datetime import date,datetime

class wiz_create_link_from_correspondance(osv.osv_memory):
    _name = 'humancapital.createlinkfromcorr'

    _columns = {
    }
    def create_links(self, cr, uid, ids, context=None):
#        print ids
#        print context
        links_obj=self.pool.get('humancapital.linking')
        correspondances=self.pool.get('humancapital.correspondance').browse(cr,uid, context['active_ids'])
        links=[]
        for correspondance in correspondances:
            links.append(links_obj.create(cr,uid,{'request_id':correspondance.request_id.id,'candidate_id':correspondance.candidate_id.id,'state':'d'}))
#        print links
        return {
                    'domain': [('id', 'in', links)],
                    'name': "Liens créés ",
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'humancapital.linking',
    #                'view_id': view_id,
                    'context': "{}" ,
                    'type': 'ir.actions.act_window'
                
                }
    
    

wiz_create_link_from_correspondance()