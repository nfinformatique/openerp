# file: Unicode1.py
# -*- coding: utf-8 -*-

import wizard
import pooler
import random
from osv import fields,osv
import hc_common
from datetime import date,datetime

def calculate_age(born,date_format = "%Y-%m-%d"):
    if born==False:
        return 0
    else:
        born = datetime.strptime(born,date_format)        
    today = datetime.today()
    try: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

class wiz_match_quests(osv.osv_memory):
    _name = 'humancapital.matchquests'

    _columns = {
        'comparison': fields.many2one('humancapital.comparison','Barême à appliquer',required=True),  
        'get_all': fields.boolean('Inclure tous les résultats '),
    }
    def get_score(self,cr,uid,candidate,request,comparison):
        score=0.0
        
#        print candidate.name
        for key in hc_common.humancapital_fields:
            print "scoring ",key
            tmpscore=0.0
            if key=="experience":
#                print comparison.__dict__
#                print candidate.__dict__
#                print request.__dict__
                tmpscore=eval("comparison.%s"%key)*hc_common.compare_integer_min(cr,uid,eval("candidate.%s"%key),eval("request.%s"%key))
                if request.fix_experience and eval("request.%s"%key)>0 and tmpscore < 1.0:
                    print "unfixed : ",key
                    return False
#                tmpscore=comparison.__dict__[key]*compare_integer_min(cr,uid,candidate.__dict__[key],request.__dict__[key])
            elif key=="age_min":
                age=calculate_age(candidate.birthdate)
                if age!=0.0:
                    tmpscore=eval("comparison.%s"%key)*hc_common.compare_integer_range(cr,uid,age,request.age_min,request.age_max)
                if request.fix_age and (eval("request.%s"%key)>0 or request.age_max>0) and tmpscore < 1.0:
                    print "unfixed : ",key
                    return False
            else:#many2many fields
                if (key=="sectors"):
                    print "SECTORS IN CAND : ",candidate.sectors
                tmpscore=eval("comparison.%s"%key)*hc_common.compare_many2many(cr,uid,eval("candidate.%s"%key),eval("request.%s"%key))
                if eval("request.fix_%s"%key) and tmpscore<1.0:
                    print "unfixed : ",key
                    return False
            score+=tmpscore
            print "TMPSCORE : ",tmpscore
        return score
    def match_quests(self, cr, uid, ids, context=None):
        
#        print "trying to match quests", hc_common.humancapital_fields
        
        wiz=self.browse(cr,uid,ids)[0]
#        print context['active_ids']
        requests=self.pool.get('humancapital.request').browse(cr,uid,context['active_ids'])
#        print requests
        if (len(requests)!=1):
            raise osv.except_osv(('Attention !'), ('Vous devez sélectionner qu\'une et une seule demande' ))
        request=requests[0]
        
        #remove old correspondances
        correspondance_obj=self.pool.get('humancapital.correspondance')
        oldcorr_ids=correspondance_obj.search(cr,uid,[('request_id','=',request.id)])
        correspondance_obj.unlink(cr,uid,oldcorr_ids)
        #Select candidates that are currently actives
        candidate_obj=self.pool.get('res.partner')
        candidates_ids = candidate_obj.search(cr, uid, [('candidate_state', '=', 'q'),('candidate','=',True)])
#        print candidates_ids
        candidates = candidate_obj.browse(cr,uid,candidates_ids)
        correspondances=[]
        for candidate in candidates:
            score = self.get_score(cr,uid,candidate,request,wiz.comparison)
            if (score>0.0 or wiz.get_all):
                correspondances.append(correspondance_obj.create(cr,uid,{'request_id':request.id,'candidate_id':candidate.id,'score':score}))
#        print correspondances;
        if (len(correspondances)>0 or True):
            return {
               #'domain': "[('type','=','%s'), ('state','=','%s'), ('period_id','in',%s)]" % (form['type'], form['state'], periods),
                    'domain': [('id', 'in', correspondances)],
                    'name': "Correspondances pour "+request.name,
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'humancapital.correspondance',
    #                'view_id': view_id,
                    'context': "{}" ,
                    'type': 'ir.actions.act_window'
            }
        
        else:          
            return {}
        
        return {
                'type': 'ir.actions.act_window_close',
         }    




















wiz_match_quests()

