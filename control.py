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
#make text answers
ans_list = []
for page in inq_kin:
    value = cnps.inquiry_cnps(number=page['number'], company=page['company'])
    if not value['success']: continue
    ans_list.append({'url': page['url'], 'docId': page['docId'],'msg': value['msg']})
print('make text answer')
#make image answers
cnps.image_cnps(inq_kin)
print('make image answer')

#answering
wrk.write_kin(ans_list)