# Scrapy settings for realstate project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "realstate"

SPIDER_MODULES = ["realstate.spiders"]
NEWSPIDER_MODULE = "realstate.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "realstate (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'nl_id=1f0a2746-3b3d-4d02-8e04-151857a648a3; l_id=78895f0b-4c22-4db3-bd69-19e3dea0051d; AdoptVisitorId=OwBgTARgHAhlAsBaGAzAbGR81oIzOBgGZEUQzcooiUBTEYIA; _cc_id=eb2076cfa040e574b9e34b3ff70bf340; _lr_env_src_ats=false; _gcl_au=1.1.1123668472.1723156495; __spdt=8dc16833f19a4de194fd4bda9cc9e995; _tt_enable_cookie=1; _ttp=TsMs5ZgfI6UDXTfC-L9CN2TrBb3; _fbp=fb.2.1723156500946.385841382790232015; mf_b837e449-83ee-457f-9ef5-8f976953f2bc=||1723680372247||0||||0|0|58.35494; r_id=ba248cb9-da45-4e71-bd45-535f0f17a6b1; __gsas=ID=452d977be9137845:T=1724782914:RT=1724782914:S=ALNI_MaQRY8--tLpR_tuGNlKo_7ZHLSlaQ; pbjs_sharedId=1709b693-489d-4e1d-81a8-76b4f89ea158; _pbjs_userid_consent_data=3524755945110770; cto_bundle=6UxlNl94dEV6NE9TaTVUMTFqJTJCZklDMzlWQm16SUF4anNybUxoQ1BuQVZRVDF3cHJ5Y2pXd1AxQlpvYlhaeWlvTnhDY0V6OGhPcW44UjlPJTJGM2p1WiUyRkJzVUsxbjBQT3AlMkZ0VVJ4VTBESyUyRkh3NzJWWDc3UUxKZCUyQk0wQnVzcDhQS08zU2NkbktOZGFvaFpURWR2a0k4SW4wVktpRXclM0QlM0Q; cto_bidid=FzBqzl9zNDdJVVBIWkpKd05SR1pzcVdkcGFnVzM3d3E3JTJGVWtSVkhkNHlNOEFNT0VRbnVUYTk0c3hJMFVRc3ViRm5KZFRNd1FoeGpJUHJnUW05aFpjY1NSUlFqZXBlajMxRHp6UHNBaVFaNmY5TWh3JTNE; TestAB_Groups=moto-steps_control.rp-img_control.cmod-security-central-my-ads_ytdicas.cnt-rating_v3.payg-discount-re-julius_ml-ranges.sanityweb50_A.adv-cookieless-ppid_enabled.cnt-scchat_configA.prf-authV2_enabled.pay-opt_v2.apsbundles_enabled.adv-li60f8_enabled.autospp-notshow-modal-hv-myads_enabled.trp-comp_control.payg-discount-julius_ml-c-mab.menu-v1_vrtcal.acrc-myacc_control.aps-motos_control.fe-bst-gll_control.um-device_control.must-optin_optin.cta-gem_control.card-mrp_control.adv-ha23ef_enabled.adfacelift-goods-web_asis.auto-placa_control.ck-ai-req_enabled.sxp-adopt_enabled.adcard-vid_control.acc-phones_enabled.cta-adview_control.ppffere_enabled.pass-lvl_enabled.swautprice_control.con-optin_A.ppfncvch_enabled.app-loc_control.swtautnc_enabled.ck-refpric_enabled.con-msgbff_A.semcaptcha_enabled.ai-img-up_enabled.txpAddCard_enabled.posinsrec_control.bjTPZ-gext_enabled.ck-fipe_control.fernwcars_enabled.fernwautnc_enabled.opt-renew_enabled.sxp-year-f_control.myads-date_enabled.posfrire_enabled.febautncvb_enabled.acc-full_enabled.rec-hfipe_enabled.ai-ggl-inf_control.ppffinjs_control.posfeecars_enabled.cdrel-vec3_control.fincnewbt_enabled.pass-chang_enabled.ppffedjs_control.vbcstdvhs_enabled.nv1-rating_enabled.udfloan_enabled.adv-li4261_enabled.finmodadvw_control; __cf_bm=OJxZPR0kL95cFrhjNz37nHV0XGl7ixMoR7yWQPK2M8M-1730485842-1.0.1.1-a2wOqAVPe12IVkd75K8PncBR.F0skdzgWf5jJbz3_Ls3yYaTppghKto4OcI3y9.H7q_kj47vhTI0ceoSC_uuiA; _cfuvid=JEy.6wW4n14SoLFtl2WdeYbJgM_mBjRhfZpp30SkAwA-1730485842894-0.0.1.1-604800000; s_id=ef78dac1-749f-43ab-a2b5-7401b33f7b9d2024-11-01T18:30:44.301379Z; sf_utm_source=direct; sf_utm_medium=none; _gid=GA1.3.425151531.1730485847; _lr_geo_location_state=RS; _lr_geo_location=BR; fp_id=WEB:3894d6e945656ad093c3c00103d42cc0; session_id=WEB:3894d6e945656ad093c3c00103d42cc0; _lr_retry_request=true; _lr_sampling_rate=100; ___iat_ses=17DA09CA598D1809; nvg83482=14dc6e2784080b77ddfb403dd210|0_307; cf_clearance=bQ1jCC7N0hgwp_RwJraxTcAZx89BBziXT1L_6mh1bWU-1730486293-1.2.1.1-Nr2qpNgK5M4F3lumOcf_vsQe4Nml3_Jeu9EM3akdKmSdlm6eYqZKtnfkD.1gikyDm3SE6fwTrGaZcF0yWt4x_79Dr9j0M.ZawUl3SbltwPnse18jSjDWXElonXThIHn9fBqd0SW35aXUVMu.IZGORs4yjpzJF9THUREXG.Q13zAQx3ckGrWssE7gs9WpBFj6.jPWpEmchEhyaKmLa4ybsWor.numgDolK6jNz3ig8sUrC66XajSobxd0l74vPEj2CJFFCGvUiFBp20_c39_Rb5YNzPfZVaPK7gtxFlrl6yckZFKEi8ovdXNwbTjqJyvs4SOYt5xw_RkOinM0icMIOkIBBWYsoK0bBne4tRDNHOlVMImQaKcPl76IP.UefJoxumY7dmkuRsCT_0wNgjtiIL9ayj2pKVEZ_3hz4PeYzP0; ___iat_vis=17DA09CA598D1809.f3bdc661a0c09cdd4c0ffb146bc44a2e.1730486301370.036f41357753da1420853b75c18515a0.UIZMJMMMAA.11111111.1-0.75be7653c218de7bb4f436911abbe149; pbjs_sharedId_cst=kSylLAssaw%3D%3D; FCNEC=%5B%5B%22AKsRol8Deb-26PcWVCOechLkhDEPkWKedZAYSXA5HbbpwYXXm5mnqTJ5BYUT1ATXkzMliPeVSINq76Y3_Ry6b8o_Fd1thfSbMCMBfdInWt_PMaN03_U9nYKPUGxGhySyuUc_AB6d3c1LSEAM368eixnbxTQK9nGu7g%3D%3D%22%5D%5D; _pubcid=9ed62674-d0fc-46de-8d23-bbaf52ead3dc; __gads=ID=ec43e29590e61fe1:T=1723156480:RT=1730486697:S=ALNI_MY1yoRYtnEf5heKQH53pYWrixwoqQ; __gpi=UID=00000ec875b7fe3c:T=1723156480:RT=1730486697:S=ALNI_MZoFbus7vxtCY-Jh7MRD8SxDKR_-A; __eoi=ID=70abfe5fde43e933:T=1723156480:RT=1730486697:S=AA-AfjYx0NO3isf9SFv7ZEv5dVFe; _ga_50C013M2CC=GS1.1.1730485847.25.1.1730486729.29.0.0; _ga=GA1.3.1415100262.1723156480; _gat_UA-70177409-2=1; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22undefined%22%2C%22hash%22%3A%22wBiML0Lv0cEh18cEd5DU%22%2C%22expiryDate%22%3A%222025-11-01T18%3A45%3A29.887Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22YEgq4sS5PAV0w9gszG02%22%2C%22expiryDate%22%3A%222025-11-01T18%3A45%3A29.888Z%22%7D; _dd_s=rum=0&expire=1730487623418',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.youtube.com',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0 (Edition std-1)',
}


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "realstate.middlewares.RealstateSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "realstate.middlewares.RealstateDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "realstate.pipelines.RealstatePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
