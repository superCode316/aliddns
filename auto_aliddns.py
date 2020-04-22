from aliyunsdkcore.acs_exception.exceptions import ClientException

from utils import *
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from json import loads
from time import asctime, localtime, time, sleep

log = open('logs.log', 'a')
ip = ''
client = getClient()


def task():
    global ip
    ip = getIP()
    data = getDomainAndRecord()
    for domain_name, rrs in data.items():
        response = loads(get_record_by_domain(domain_name))
        records = response['DomainRecords']['Record']
        requests = do_get_update(rrs, domain_name, records)
        for request in requests:
            request.set_Type('A')
            request.set_Value(ip)
            try:
                client.do_action_with_exception(request)
            except ClientException as ee:
                log.write('无法更新/添加记录\n')
                log.write(ee.message)
                log.write('域名' + request.get_DomainName() + '|rr : ' + request.get_RR() + '|request_id : ' +
                          request.get_RecordId())
                log.flush()


def do_get_update(rrs, domain_name, records):
    def update_domain_record(record):
        if record['Value'] == ip:
            return
        log.write('\n')
        log.write(asctime(localtime(time())))
        log.write('\n解析记录' + record['RR'] + ' -> \t当前IP：' + ip)
        log.write('\n记录IP: \t' + record['Value'])
        log.write('\n当前ip和记录不一致，将被替换\n')
        log.flush()
        request = UpdateDomainRecordRequest()
        request.set_RecordId(record['RecordId'])
        request.set_accept_format('json')
        request.set_RR(record['RR'])
        return request

    def add_domain_record(domain, RR):
        log.write('\n')
        log.write(asctime(localtime(time())))
        log.write('\n添加记录')
        log.write('\n记录IP: \t' + ip)
        log.flush()
        request = AddDomainRecordRequest()
        request.set_DomainName(domain)
        request.set_accept_format('json')
        request.set_RR(RR)
        return request

    result = []
    for _record in [x for x in records if x['RR'] in rrs]:
        result.append(update_domain_record(_record))
    for rr in [x for x in rrs if x not in [m['RR'] for m in records]]:
        result.append(add_domain_record(domain_name, rr))

    return result


def get_record_by_domain(domain):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    return client.do_action_with_exception(request)


if __name__ == "__main__":
    print('start')
    count = 0
    while True:
        if count == 3:
            count = 0
            sleep(30)
        try:
            task()
            sleep(180)
        except BaseException as e:
            count += 1
            print('pending error')
            print(e)
            log.write(str(e))
            log.flush()
