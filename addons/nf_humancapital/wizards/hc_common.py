# file: Unicode1.py
# -*- coding: utf-8 -*-
from osv import fields,osv


class hc_many2many(fields.many2many):    
    def __init__(self,*args):
        super(hc_many2many,self).__init__(*args)
        
class hc_age(fields.date):
    def __init__(self,*args):
        super(hc_age,self).__init__(*args)

class hc_integer(fields.date):
    def __init__(self,*args):
        super(hc_integer,self).__init__(*args)

class hc_dynamicObject(osv.osv):
    def __init__(self,*args):
        if (self._import_columns):
            for k in self._import_columns:
                self._columns[k]=humancapital_fields[k]['object']
        super(hc_dynamicObject,self).__init__(*args)




def compare_many2many(cr,uid,value,baseset):
    score = 0.0
    for id in baseset:
        print "ID : ",id," VALUE: ",value
        if id in value:
            print baseset
            print 1.0/float(len(baseset))
            score+=1.0/float(len(baseset))
    print "many2many score : ", score
    return score

def compare_integer_min(cr,uid,value,limit):
    if limit==0.0:
        return 0.0
    if value >= limit:
        return 1.0
    else:
        return value/limit
def compare_integer_range(cr,uid,value,limit_min,limit_max,range=100.0):
    print limit_max
    print limit_min
    print value
    if limit_min== 0.0 and limit_max==0.0:
        return 0.0
    if value > limit_min:
        if value < limit_max:
            return 1.0
        else:
            return (limit_max-value)/range
    else:
        return (value-limit_min)/range

class autoimport(osv.osv):
    def __init__(self,*args):
#        from wizards.hc_common import humancapital_fields
        for key in self._import_columns:
            self._columns[key]=humancapital_fields[key]['object_class'](*(humancapital_fields[key]['object_contruct_params']))
        super(autoimport,self).__init__(*args)
    
    
humancapital_fields={
                     
        'knownlanguages': {
                'object_class':        fields.many2many ,
                'object_contruct_params' : ['humancapital.languages','rel_knownlanguagescandidate','candidate_id','language_id','Langues maîtrisées'],
                'object_comparison_fct' : compare_many2many,
                           },
                           
        'approxlanguages': fields.float('Langues connues'),
        'sectors': fields.float('Secteurs'),
        'functions': fields.float('Fonctions'),
        'formations': fields.float('Formations'),
        'workpermits': fields.float('Permis de travail'),
        'contracttypes': fields.float('Types de contrat'),
        'nationalities': fields.float('Nationalités'),
        'age_min': fields.float("Age"),
        'experience': fields.float("Années minimum d'expérience"),

}

#                     
#                     
#        'knownlanguages': {
#                           'object': fields.many2many('humancapital.languages','rel_knownlanguagescandidate','candidate_id','language_id','Langues maîtrisées'),
#                           }
#        'approxlanguages': {
#                            'object':fields.many2many('humancapital.languages','rel_approxlanguagescandidate','candidate_id','language_id','Langues connues'),
#                        }
#        'candidatesectors': {
#                             'object':fields.many2many('humancapital.sectors','rel_sectorscandidate','candidate_id','sector_id','Secteurs'),
#                             }
#        'entreprisesectors': {
#                              'object':fields.many2many('humancapital.sectors','rel_sectorsentreprise','entreprise_id','sector_id','Secteurs'),
#                              }
#        'functions': {
#                      'object':fields.many2many('humancapital.functions','rel_functionscandidate','candidate_id','function_id','Fonctions'),
#                      }
#        'formations': {
#                       'object':fields.many2many('humancapital.formations','rel_formationscandidate','candidate_id','formation_id','Formations'),
#                       }
#        'workpermits': {
#                        'object':fields.many2many('humancapital.workpermits','rel_workpermitcandidate','candidate_id','workpermit_id','Permis de travail'),
#                        }
#        'contracttypes': {
#                          'object':fields.many2many('humancapital.contracttypes','rel_contracttypecandidate','candidate_id','contracttype_id','Types de contrat'),
#                          }
#        'nationalities': {
#                          'object':fields.many2many('humancapital.nationalities','rel_nationalitiescandidate','candidate_id','nationalitie_id','Nationalités'),
#                          }
#        'birthdate': {
#                      'object':fields.date("Date de naissance"),
#                      }
#        'experience': {
#                       'object':fields.integer("Années d'expérience"),
#                       }
#        }
#        
        
                             
