from aliyunsdkcore.client import AcsClient
from http.client import HTTPConnection
import config

config.set_config('ddns')


def getClient():
    user = config.read_config('user')
    client = AcsClient(user['AccessKeyId'], user['AccessKeySecret'], 'cn-hangzhou')
    return client


def getIP():
    con = HTTPConnection('whatismyip.akamai.com')
    con.request('GET', '/')
    ip = con.getresponse()
    return ip.read().decode('ascii')


def getDomainAndRecord():
    return config.read_config('domains')
