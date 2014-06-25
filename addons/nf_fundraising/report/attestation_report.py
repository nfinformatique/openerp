from openerp.report import report_sxw
from openerp.osv.osv import except_osv
import pooler



class Attestation_Report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context={}):
        super(Options_Report,self).__init__(cr,uid,name,context)
        pool_obj=pooler.get_pool(cr.dbname)
        print "Hello !!! ",context
#         attestation_obj=pool_obj.get("nf_fundraising.attestation")
#         option_objs=[]
#         for o in option_obj.browse(cr,uid,context['option_ids']):
#             option_objs.append(o)
#         self.localcontext={}
#         self.localcontext.update({
# #             'time': time,
#              'cr': cr,
#              'uid': uid,
#              'option_objs':option_objs,
#              'camp':option_objs[0].camp_id,
#              'print_options': context['print_options'],
#              'print_children': context['print_children'],
#              'print_monitors': context['print_monitors'],
#              
#  #            'company_vat': self._get_company_vat,
#          })

report_sxw.report_sxw('report.nf_fundraising.attestation_report',
                       'nf_fundraising.attestation',
                       'addons/nf_fundraising/report/attestation.mako.html',
                       parser=Attestation_Report)
