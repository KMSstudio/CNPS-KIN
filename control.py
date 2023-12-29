import inquiry_cnps as cnps
import inquiry_kin as kin

inq_kin = kin.inquiry_kin()
for page in inq_kin:
    value = cnps.inquiry_cnps(number=page['number'], company=page['company'])
    print(value)