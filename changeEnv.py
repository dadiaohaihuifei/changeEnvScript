# encoding=utf8
# 为了解决打包环境配置问题 
'''
edit by wsj
'''
import os, sys
from biplist import *

# 处理 python 2.7 默认字节流
reload(sys)
sys.setdefaultencoding('utf-8')
#-------------------   切换参数  ----------------------
'''
No_up 表示 是否版本号更新 +1
=> true +1  False 不加
'''
No_up = False

'''
isDebug True 表示测试环境
'''
isDebug = True
#-------------------——   ####   ----------------------

# 当前文件的路径
url = os.path.dirname(os.path.realpath(__file__))

# 找到需要修改的几个文件 <kdweibo_conf.plist, Info.plist,(分享的 Info.plist) 
#	InfoPlist.strings>

xthost = 'http://weixin.hongkun.com.cn/'
tsqhost = 'http://tsq.hongkun.com.cn/'
wbhost = 'http://weibo.hongkun.com.cn'
wbbase = 'http://weibo.hongkun.com.cn/snsapi'
suitname = 'group.com.hkdc.kdweibo.HKSystemShareExtension'
kd_ID = 'com.hkdc.kdweibo.client'
share_ID = 'com.hkdc.kdweibo.client.HKSystemShareExtension'
display_name = '鸿信'
# 切换固定参数
if isDebug:
	xthost = 'http://xttest.hongkun.com.cn/'
	tsqhost = 'http://tsqtest.hongkun.com.cn/'
	wbhost = 'http://weibotest.hongkun.com.cn'
	wbbase = 'http://weibotest.hongkun.com.cn/snsapi'
	suitname = 'group.com.hongkun.test.www'
	kd_ID = 'com.hongkun.test.www'
	share_ID = 'com.hongkun.test.www.HKShareTestExtension'
	display_name = '鸿信测试'

# 获取当前 bundle 路径 
bundle_path = os.path.join(url,'鸿信 V_1.0 版本','kdweibo_for_iPhone')

# 1.kdweibo_conf.plist
kdweibo_path = os.path.join(bundle_path, 'kdweibo_conf.plist')
kdweibo_conf = readPlist(kdweibo_path)
# HKXTV_2.BaseURL HKCC.BaseURL kdweibo.pref.serverBaseURL kdweibo.pref.restBaseURL suitName
kdweibo_conf['HKXTV_2.BaseURL'] = xthost
kdweibo_conf['HKCC.BaseURL'] = tsqhost
kdweibo_conf['kdweibo.pref.serverBaseURL'] = wbhost
kdweibo_conf['kdweibo.pref.restBaseURL'] = wbbase
kdweibo_conf['suitName'] = suitname

# 写入文件
try:
	writePlist(kdweibo_conf,kdweibo_path)
except Exception, e:
	print '写入的时候发生了意外'
	raise

# 2.kdweibo 的 Info.plist
kd_info_path = os.path.join(bundle_path, 'Info.plist')
kd_info = readPlist(kd_info_path)
# BuildNo/Bundle display name/Bundle identifier/Bundle versions string, short/
# Bundle version
kd_info['CFBundleIdentifier'] = kd_ID
kd_info['CFBundleDisplayName'] = display_name

# 这是处理版本号增加的函数 1.1.1 升级版本号
def handle_version(vers):
	'''这是处理版本号增加的函数'''
	ver_array = vers.split('.')
	ver_0 = int(ver_array[0])
	ver_1 = int(ver_array[1])
	ver_2 = int(ver_array[2])
	if ver_2 >= 9:
		ver_2 = 0
		if ver_1 >= 9:
			ver_1 = 0
			ver_0 = ver_0 + 1
		else:
			ver_1 = ver_1 + 1
	else:
		ver_2 = ver_2 + 1
	return '%d.%d.%d' % (ver_0, ver_1, ver_2)
if No_up:
	# 这里版本号 类似 3.1.2 需要特殊处理
	# version
	short_version = kd_info['CFBundleShortVersionString']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
	kd_info['CFBundleShortVersionString'] = handle_version(short_version)
	#build version
	bundle_version = kd_info['CFBundleVersion']
	kd_info['CFBundleVersion'] = handle_version(bundle_version)

	kd_info['BuildNo'] = str(int(kd_info['BuildNo']) + 1)
# 写入文件
try:
	writePlist(kd_info, kd_info_path)
except Exception, e:
	raise e

# 3.InfoPlist.strings (这个格式真是不会读)
kd_en_Info_string = os.path.join(bundle_path, 'en.lproj', 'InfoPlist.strings')
kd_zh_Info_string = os.path.join(bundle_path, 'zh_CN.lproj', 'InfoPlist.strings')

# 4.修改 extension 的info.plist
kd_share_info_path = os.path.join(bundle_path, 'HKSystemShareExtension','Info.plist')
share_plist = readPlist(kd_share_info_path)
share_plist['CFBundleIdentifier'] = share_ID
share_plist['CFBundleDisplayName'] = display_name
share_plist['CFBundleShortVersionString'] = kd_info['CFBundleShortVersionString']
share_plist['CFBundleVersion'] = kd_info['CFBundleVersion']
try:
	writePlist(share_plist,kd_share_info_path)
except Exception, e:
	raise e


# 5.修改 HKSystemShareExtension
kdweibo_entitlements = os.path.join(bundle_path,'kdweibo.entitlements')
kd_entit = readPlist(kdweibo_entitlements)
kd_entit['com.apple.security.application-groups'] = [suitname,]
try:
	writePlist(kd_entit,kdweibo_entitlements)
except Exception, e:
	raise e

share_entitlements = os.path.join(bundle_path,'HKSystemShareExtension','HKSystemShareExtension.entitlements')
sh_entit = readPlist(share_entitlements)
sh_entit['com.apple.security.application-groups'] = [suitname,]
try:
	writePlist(sh_entit,share_entitlements)
except Exception, e:
	raise e



# print kd_info




