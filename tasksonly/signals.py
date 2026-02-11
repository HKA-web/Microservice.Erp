import logging
import os
import sys

from asgiref.sync import async_to_sync
from django import dispatch
from django.dispatch import receiver

from library.sydney import SydneyClient

os.environ['BING_COOKIES'] = 'SRCHUSR=DOB=20240229&T=1709226032000&TPC=1709226032000&POEX=W;_Rwho=u=d;SRCHHPGUSR=SRCHLANG=en&IG=F7DF05D4F21847019F72532095471AB4&PV=15.0.0&BRW=XW&BRH=M&CW=1920&CH=945&SCW=1920&SCH=112&DPR=1.0&UTC=420&DM=0&WTS=63844822832&HV=1709226049&PRVCW=1920&PRVCH=945&CIBV=1.1600.1;ANON=A=D8F33DAE678597EB819962CFFFFFFFFF&E=1d67&W=1;_SS=SID=1066E349DFA962021D1AF77DDEFE63BA&R=24&RB=24&GB=0&RG=0&RP=3;ipv6=hit=1709229636580&t=4;dsc=order=News;_U=1Vu87egX4HFKDNRtkClAlz1rghqnrzbGTpsFEZU4k-LKFANYBVp76iICmfnTYny-Fa0e6qCK-9Hexc-lxjQV3ipGmCZeRwkScx8b49N11Bd-bNgx15CqmflcP5igjXz0URQICt3BKPWLujfIZTHWtkWQgaXGzaSP9H2Q1Y131r4XjavhXN_WtqknTf0Hx3tBLILcdR38aogHVmr6AVK4U4aypeZj_Sk4q3sr7h2Kpmeo;SRCHD=AF=MG0AUO;PPLState=1;_EDGE_V=1;NAP=V=1.9&E=1d0d&C=WOS3xHHbtvJEbeS3Snx_aNGJhikV7_fS1eHmpSMkLjXk0ZWSbGrbgg&W=1;vidbh=1;_RwBf=r=0&ilt=1&ihpd=0&ispd=1&rc=24&rb=24&gb=0&rg=0&pc=3&mtu=0&rbb=0&g=0&cid=&clo=0&v=2&l=2024-02-29T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&rwflt=2024-02-29T08:21:11.4220110-08:00&o=0&p=sapphire&c=true&t=3921&s=2023-04-10T11:20:27.9179498+00:00&ts=2024-02-29T17:00:49.6944741+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=qq2osS1wcepsUuE-mXAOjn3y1tNMY4dH5yo1ZnivZ9aF2tkVsEpBiqV5AIglHWDJq1X44w4-mdzKAvqK3hGzZv06BPzj0qNAgkFPLo4dTX4&A=D8F33DAE678597EB819962CFFFFFFFFF;_EDGE_S=F=1&SID=1066E349DFA962021D1AF77DDEFE63BA&mkt=en-id&ui=en-us;MUIDB=03721131BD7662B8314E0505BC2163AB;KievRPSSecAuth=FAByBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACDJy9QuLXaHjMATIgTT5/9TWbOTBoYzfNWKtjFSp/PGyYjFiX1/0HTIm0ElwvBsVJRGTC5070eFnx7Nyyy8h29+dhoQpSavI5SC/APYzLn1RYqjo0t7gFB7YdxrwrgWHymPoZigGF9JehiCd7VYebnkjcpsRbfdiXNad+HG6VSKUna/35HZjGODgLTC0YXzshjcf/ut4p/un0IKVcKBA8JhKCZZrtLVwuTufsyXSLNcXUJNuWbhSo0aoI365W1oQ0rR8ksQY/9D543qcDO71FSH5sQ63y6ZXV6tgOO7R9afI+k+sOF7zXlFuArYNdAbAIVFuyO9XVzBGAaZpGDstK4HrZ/8B8Ts5b/H4gFRAYW1U7EKtkVY4BPK/YhialZzE0ZbF8jvk3u1Ic1SYoVf9X6z56pCp18cahTnBtcV3rhL279EgVxoghXp5I9ovL0rG4FZvpCPD9PmdhbymBUtS1upDPmSAjTui71NWxlm2lt6nPZcAC35VTBv3BGXM9Cw2+uKBPCEc8JGWwk4CIUXZdsSki3qCmmTEnW4VRBbl5rEDMdSDiws/vCgteOOmp+UiTrrXtzX4HzzzXjkpiApUoXU2qLpt9qjPVMC/lQIHeD3DysxoQ8S6na1/8f9J3JC0WtgEHnsFpSTOlxBCX4wUg+ybGKpsOc2TKsRsXlaUpl2h9d/Q6uRCZ/h+C9l7meM3Hwr088+LafUjgpdk/24tKlgeOnt0oxEIxzA1tR9MsqvTc187zwaSEfQiLFthaRHsKErqKsAeCcAONJNh7qBNzOeJ+dyX+aidcamiYZIhp2BlUYvrjGbI22ZoIlIPqoaoUmZi2U35GwbK1063OFCwy/CD0Yh9TJdFTFrcfJDqykr3A41jkWnHECOJE8kOyvSLdOc+UgrTVK+jx5yb6uyMDHymFPHAB2JlC18dXktS0UG5TsS3bXBessDOaz6zpUpHyigOOzXmM9CV+XMvxIgFv3mYleDDJkGNjnksaqSqNsnj9h2Lax4ZRM6L+yilAIhxq1T8RITK8B2iwQbTt7lc6EaimRf4H4i0AkLNvuAsK6V/4WTiXdwcGercjb4/pXsWRkdEmo49BjvNm6tEJPhTposjP50C1BnuJ83eoW8aUpXxiBLwjIokolZ+m85J5GElp6oJ1GCoLDWP5/Zwpv8/LWnJFzwXrPFQOP/Oul2fgFbF78FNsN7Idw1prxHpOrBfospaVv8vNgb2IEPWKnqbthc/M1nuNw9lVrko4jMxRyIljIc9rHdDC7sdlYhT/3Hb+plG/Xn1uVOHVX9s6pEsilChzKBI6oKMHT6DaxHU4e3sbxMlEcGuXxYGDFpW7kri5yqWEfPgvL/TTvF2bWIagQwBDWdsM4b68vV4OjL+0ulGlSYYNYDKccwTu9b7vSsKmTn4IuvNAukOrWJz4rMiysZa+ZHKMqk+ZrWQFACHz37VdH82w1MuI90LEJm65uOKwg==;MUID=03721131BD7662B8314E0505BC2163AB;SRCHUID=V=2&GUID=20916254B86A4245A28A518E2BB7D438&dmnchg=1;svidbh=1;WLID=mIz5nv6gBD3jNIqEFF4dSCySkAzzF24f7Ro9+xnR8o1KQskwOXmplNXV+bG4sTFeNQZjPgdbRxva2LDWntl2l6d4VAfq1FFRD0gMat7qmvo=;WLS=C=96aeb3ecb92cce0e&N=Rahmat'

logger = logging.getLogger(__name__)
demo = dispatch.Signal()

sydney = SydneyClient(style='precise')


logging.getLogger('websockets.client').setLevel(logging.ERROR)

@async_to_sync
async def mainan(ask):
    await sydney.start_conversation()
    response = await sydney.ask(ask, )
    print(response, end='\n', flush=True)


@receiver(demo)
def asks(sender, ask, **kwargs):
    try:
        mainan(ask)
    except Exception as e:
        logger.error(e)


# use :
# from tasksonly import signals
# signals.demo.send(sender=98765678,ask='Apa Kepanjangan dari indonesia raya ?')
