import os
for jet in ["calo", "pf"]:
    for var in ["pn","pv"]:
        cmd = ["hadd", 
               "%sJet_%s_T2cc.root" % (jet,var),
               "375_%sJet_ge2j_bn_jn_in_%s_T2cc.root" % (jet,var),
               "375_%sJet_ge2j_bn_jn_in_%s_T2cc_mstw.root" % (jet,var)]
        
        os.system(" ".join(cmd))
