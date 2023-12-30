import inquiry_cnps as cnps
import inquiry_kin as kin
import writer_kin as wrk

#inquiry kin
inq_kin = []
inq_kin.extend(kin.inquiry_kin(company='cj', page=1))
inq_kin.extend(kin.inquiry_kin(company='po', page=1))
print('inquiry kin')
#make answers
ans_list = cnps.inquiry_cnps(inq_kin)
print('make image answer')
#answering
wrk.write_kin(ans_list)