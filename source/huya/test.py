import json

s = str({'level': 'INFO', 'message': '{"message":{"method":"Network.responseReceived","params":{"frameId":"361D7DEC4E1430E529FC7CE5919B12D8","hasExtraInfo":true,"loaderId":"DDBA8B25B585ED537E34968309EC1FBC","requestId":"14852.9397","response":{"alternateProtocolUsage":"unspecifiedReason","connectionId":0,"connectionReused":false,"encodedDataLength":0,"fromDiskCache":true,"fromPrefetchCache":false,"fromServiceWorker":false,"headers":{"accept-ranges":"bytes","access-control-allow-origin":"*","age":"0","ali-swift-global-savetime":"1682251661","content-length":"54879","content-md5":"oYEXehF5VmEDzqVBkXdA/Q==","content-type":"image/png","date":"Sun, 23 Apr 2023 12:07:41 GMT","eagleid":"dd82c09c16822516615003479e","etag":"\\"A181177A1179566103CEA541917740FD\\"","last-modified":"Thu, 12 Jan 2023 10:21:22 GMT","server":"Tengine","timing-allow-origin":"*","via":"cache34.l2cn1827[68,33,304-0,C], cache35.l2cn1827[35,0], vcache21.cn4618[48,27,200-0,C], vcache8.cn4618[31,0]","x-cache":"HIT TCP_MEM_HIT dirn:-2:-2","x-oss-cdn-auth":"success","x-oss-hash-crc64ecma":"9514582908015113992","x-oss-object-type":"Normal","x-oss-request-id":"64451F8D490ACB36320A337F","x-oss-server-time":"3","x-oss-storage-class":"Standard","x-swift-cachetime":"3600","x-swift-savetime":"Sun, 23 Apr 2023 12:07:41 GMT"},"mimeType":"image/png","protocol":"h2","remoteIPAddress":"221.130.192.181","remotePort":443,"responseTime":1.682251666149843e+12,"securityDetails":{"certificateId":0,"certificateTransparencyCompliance":"unknown","cipher":"AES_128_GCM","encryptedClientHello":false,"issuer":"GeoTrust CN RSA CA G1","keyExchange":"ECDHE_RSA","keyExchangeGroup":"X25519","protocol":"TLS 1.2","sanList":["v.huya.com","sd.huya.com","eadmin.huya.com","agency.huya.com","ad.huya.com","open.huya.com","cmsstatic.huya.com","v-cms-img.huya.com","download.huya.com","wup.hooya.msstatic.com","iframe.huya.com","smartclip.huya.com","v-huya-img-internal.huya.com","cdnfile.huya.com","m.huya.com","cdn.wup.huya.com","online.huya.com","www2.huya.com","layer.huya.com","hd.huya.com","stat.wup.huya.com","cdnws.api.huya.com","wsapi.huya.com","games.huya.com","app-agreements.huya.com","p.huya.com","pre-dev.huya.com","dev.huya.com","ow.huya.com","gp.huya.com","kiwistatic.huya.com","xy-hydlpcdn.huya.com","*.web.huya.com","*.va.huya.com","*.msstatic.com","*.cdn.huya.com","*.peiwanlu.com","*.v.huya.com"],"serverSignatureAlgorithm":2052,"signedCertificateTimestampList":[],"subjectName":"v.huya.com","validFrom":1666569600,"validTo":1700697599},"securityState":"secure","status":200,"statusText":"","timing":{"connectEnd":-1,"connectStart":-1,"dnsEnd":-1,"dnsStart":-1,"proxyEnd":-1,"proxyStart":-1,"pushEnd":0,"pushStart":0,"receiveHeadersEnd":2.694,"requestTime":76824.070264,"sendEnd":1.008,"sendStart":1.008,"sslEnd":-1,"sslStart":-1,"workerFetchStart":-1,"workerReady":-1,"workerRespondWithSettled":-1,"workerStart":-1},"url":"https://diy-assets.msstatic.com/hyys/activity/20230112sx_10.png"},"timestamp":76824.07984,"type":"Image"}},"webview":"A768ED91FDC2A21B4DB1C97B8273202D"}', 'timestamp': 1682252449955})

idx = s.find()
print(s[idx + 57:idx + 59])