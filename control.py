import inquiry_cnps as cnps
import inquiry_kin as kin
import writer_kin as wrk

#inquiry kin
inq_kin = []
inq_kin.append(kin.inquiry_kin(company='cj'))
inq_kin.append(kin.inquiry_kin(company='lg'))
inq_kin.append(kin.inquiry_kin(company='po'))
print('inquiry kin')
#remove duplication
#make merge list
merge = []
for page in inq_kin:
    value = cnps.inquiry_cnps(number=page['number'], company=page['company'])
    if not value['success']: continue
    merge.append({'url': page['url'], 'msg': value['msg']})
print('make merge list')

#answering
wrk.write_kin(merge)