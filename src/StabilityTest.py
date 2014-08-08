# coding=utf-8

"""  Android app  stress test tool based on Monkey

     Copyright 2014 Inspur Tester JiTeng.
"""

import os
import time
import logAnalyzer
import testLogger
from subprocess import Popen, PIPE
import ConfigParser

#总运行时间（分钟）
run_time = 60

#如果用此参数指定了一个或几个包，Monkey将只允许系统启动这些包里的Activity。
#如果你的应用程序还需要访问其他包里的Activity（如选取一个联系人），那些包也需要在此同时指定。
#如果不指定任何包，Monkey将允许系统启动全部包里的Activity。
#要指定多个包，需要使用多个-p选项，每个-p选项只能用于一个包。
allowed_package_name = 'com.test.packagename'


#每次发送Event数量
eventsConut = 300

#log显示界别：3为最高，1为最低
log_level = 3

#monkey命令里用于在事件之间插入固定延迟。通过这个选项可以减缓monkey的执行速度。
#如果不指定该选项，monkey将不会被延迟，事件将尽可能快地被产生。
throttle = 500

#设置此选项，Monkey将在应用程序崩溃或发生任何失控异常时继续向系统发送事件，直到计数完成。
ignore_crashes = False

#设置此选项，Monkey将在应用程序发生任何超时错误(如“Application Not Responding”对话框)时，继续向系统发送事件，直到计数完成。
ignore_timeouts = False

#设置此选项，Monkey将在应用程序发生许可错误(如启动一个需要某些许可的Activity)时，继续向系统发送事件，直到计数完成。
ignore_security_exceptions = False

#用于调整触摸事件的百分比(触摸事件是一个down-up事件，它发生在屏幕上的某单一位置)
pct_touch = 21

#用于调整动作事件的百分比(动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
pct_motion = 14

#用于调整轨迹事件的百分比(轨迹事件由一个或几个随机的移动组成，有时还伴随有点击)。
pct_trackball = 2

#基本导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
pct_nav = False

#主要导航事件的百分比(这些导航事件通常引发图形接口中的动作，如：5-way键盘的中间按键、回退按键、菜单按键)
pct_majornav = False

#系统按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)。
pct_syskeys = False

#启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
pct_appswitch = 30

#其他类型事件的百分比。这是一个对其他事件的汇总，比如按键、在设备很少被用到的按钮等等。
pct_anyevent = False

#通常，当 Monkey 由于一个错误而停止时，出错的应用程序将继续处于运行状态。
#当设置了此选项时，将会通知系统停止发生错误的进程。注意，正常的 (成功的)
#结束，并没有停止启动的进程，设备只是在结束事件之后，简单地保持在最后的状态。
kill_process_after_error = True


def executeCmd(s):
    resp = Popen(s, shell=True,stdout=PIPE, stderr=PIPE).stdout.readlines()
    a = []
    for i in resp:
        a.append(i.strip('\r\n'))
    return a

def setPropertiesFromConfig():
    global run_time
    global allowed_package_name
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini") 
    run_time = cf.getint("config", "run_time")
    allowed_package_name = cf.get("config", "allowed_package_name")

def getMonkeyCommandOption():
    adb_command_option = ''

    #设置log显示级别
    if log_level is 3:
        adb_command_option += '-v -v -v '
    elif log_level is 2:
        adb_command_option += '-v -v '
    else:
        adb_command_option += '-v '
    
    #设置seed
    adb_command_option += '-s '+str(current_time('time'))+' '

    #设置allowed_package_name
    if allowed_package_name is False:
        pass
    else:
        adb_command_option += '-p '+str(allowed_package_name)+' '

    #设置throttle
    if throttle is False:
        pass
    else:
        adb_command_option += '--throttle '+str(throttle) +' '

    #设置--ignore-crashes
    if ignore_crashes is True:
        adb_command_option += '--ignore-crashes '
    else:
        pass

    #设置--ignore-timeouts
    if ignore_timeouts is True:
        adb_command_option += '--ignore-timeouts '
    else:
        pass

    #设置--ignore_security-exceptions
    if ignore_security_exceptions is True:
        adb_command_option += '--ignore-security-exceptions '
    else:
        pass

    #设置--pct-touch 
    if pct_touch is False:
        pass
    else:
        adb_command_option += '--pct-touch  '+ str(pct_touch) + " "

    #设置--pct-motion
    if pct_motion is False:
        pass
    else:
        adb_command_option += '--pct-motion  '+ str(pct_motion) + " "

    #设置--pct-trackball
    if pct_trackball is False:
        pass
    else:
        adb_command_option += '--pct-trackball  '+ str(pct_trackball) + " "

    #设置--pct-nav
    if pct_nav is False:
        pass
    else:
        adb_command_option += '--pct-nav  '+ str(pct_nav) + " "

    #设置--pct-majornav
    if pct_majornav is False:
        pass
    else:
        adb_command_option += '--pct-majornav  '+ str(pct_majornav) + " "

    #设置--pct-syskeys
    if pct_syskeys is False:
        pass
    else:
        adb_command_option += '--pct-syskeys  '+ str(pct_syskeys) + " "

    #设置--pct-appswitch
    if pct_appswitch is False:
        pass
    else:
        adb_command_option += '--pct-appswitch  '+ str(pct_appswitch) + " "

    #设置--pct-anyevent
    if pct_anyevent is False:
        pass
    else:
        adb_command_option += '--pct-anyevent  '+ str(pct_anyevent) + " "

    #设置--kill-process-after-error
    if kill_process_after_error is True:
        adb_command_option += '--kill-process-after-error '
    else:
        pass

    return adb_command_option

def current_time(x):
    '''
    date：Get the current date，e.g. 20130808
    time：Get the current time，e.g. 135035
    datetime：Get the current datetime，e.g. 20130808-135035
    '''
    if x is 'date':
        x = time.strftime('%Y%m%d',time.localtime(time.time()))
        return x
    elif x is 'time':
        x = time.strftime('%H%M%S',time.localtime(time.time()))
        return x
    elif x is 'datetime':
        x = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
        return x
    else:
        return False

def main():
    #从配置文件中设置运行时间和所测应用包名
    setPropertiesFromConfig()

    #设置目录存储日志，如果不存在则创建
    now = current_time('datetime')
    current_path=os.path.abspath('.')
    result_path  = current_path+'\\TestResults\\%s' %now
    if not os.path.exists(result_path):
        os.makedirs(result_path)


    #得到开始时间
    start_time = time.time()

    #得到logger
    logger=testLogger.getLogger(result_path,'StressTest','Execution.log')
    logger.info('Stress test begins.')
    logger.info('')

    #开始循环执行
    while int(time.time()-start_time) <= run_time*60:
        logger.info('Single monkey test begins.')
        #获取当前连接的设备号
        r = executeCmd('adb get-serialno')
        #当前没有连接设备
        if r[0] == 'unknown':
            logger.warning('No devices is connected.Please connect one device.')
            # 休眠10秒
            time.sleep(10)
        #当前连接多个设备
        elif len(r) > 1:
            logger.warning('Multiple devices connected.Please connect only one device.')
            # 休眠10秒
            time.sleep(10)
        #当前只有一个设备
        else:
            #得到当前连接的安卓设备号
            logger.info('Connected device serial number: %s' %r[0])
            #每次Monkey运行日志名称
            monkey_test_logname = 'SingleMonkeyTest_%s.log' %current_time('time')
            #每次Monkey Logcat日志名称
            monkey_test_logcatname = 'LogcatOf'+monkey_test_logname
            #创建Logcat日志文件
            logcat_file = open(str(result_path+'\\'+monkey_test_logcatname), 'w')
            #清除logcat信息
            executeCmd('adb logcat -c')
            #保存logcat信息
            process_logcat = Popen('adb logcat -v time', shell=False, stdout=logcat_file)
            #拼接得到最终Monkey命令
            run_monkey = 'adb shell monkey %s%s > %s\\%s' %(getMonkeyCommandOption(),eventsConut,result_path,monkey_test_logname)
            logger.info('%s %s',*('Runing adb command:',run_monkey))
            #运行最终Monkey命令
            os.system(run_monkey)
            #结束logcat日志保存
            process_logcat.terminate()
            
            logger.info('Single monkey test finished.\n')  
            # 休眠2秒
            time.sleep(2)
    logger.info('')
    logger.info('Stress test finished.')
    logger.info('')

    #分析Monkey日志，查看是否有关键字:System appears to have crashed
    swff = logAnalyzer.SearchWordFromFiles()
    logger.info('Start analyzing log for key word:System appears to have crashed')
    keyWordExceptionNum=swff.search(result_path, 'System appears to have crashed')
    if keyWordExceptionNum == 0 :
       logger.info('Logs have no key word:System appears to have crashed.')
       logger.info('There is no app crash happened.')
       MTBF = run_time
       logger.info('The RunTime is '+str(run_time)+' minutes.')
       logger.info('The MTBF is '+str(MTBF)+' minutes.')
    else:
       logger.info('The key word number in all is '+str(keyWordExceptionNum))
       logger.info('The tested app crashed '+str(keyWordExceptionNum)+' times.')
       MTBF = run_time/(keyWordExceptionNum+1)
       logger.info('The RunTime is '+str(run_time)+' minutes.')
       logger.info('The MTBF is '+str(MTBF)+' minutes.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n********* Stress test interrupted by user! ********* \n")