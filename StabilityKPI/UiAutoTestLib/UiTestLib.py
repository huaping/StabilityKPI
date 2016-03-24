#!/usr/bin/env python
# -*- coding: utf-8 -*-
from robot.api import logger
import uiautomator
from uiautomator import Adb, Device
import subprocess
import os
import time
import datetime
from robot.libraries.BuiltIn import BuiltIn
import re
import GoogleTTS
import urllib2


"""
UI Test Library for android
@author: Huaping Qi
@version 0.2
"""

class UiTestLib(object):
    """Ui Test Lib

    """
    def __init__(self, serial = None):
        """
        """
        logger.info('<p>Device=%s>' % serial, html=True)
        print '<p>Device=%s>' % serial
        self._result = ''
        self.starttime = 0
        self.d = Device(serial)
        self.adb = Adb(serial)
        self.debug = 'True'

    def set_debugable(flag):
        self.debug = flag

    def set_serial(self, serial):
        """Specify given *serial* device to perform test.
        or export ANDROID_SERIAL=CXFS42343 if you have many devices connected but you don't use this
        interface

        When you need to use multiple devices, do not use this keyword to switch between devices in test execution.
        And set the serial to each library.
        Using different library name when importing this library according to
        http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.8.5.

        Examples:
        | Setting | Value |  Value |  Value |
        | Library | UiTestLib | WITH NAME | Mobile1 |
        | Library | UiTestLib | WITH NAME | Mobile2 |

        And set the serial to each library.
        | Test Case        | Action             | Argument           |
        | Multiple Devices | Mobile1.Set Serial | device_1's serial  |
        |                  | Mobile2.Set Serial | device_2's serial  |
        """
        self.d = Device(serial)
        self.adb = Adb(serial)
    def logmsg(self, msg):
        if self.debug == 'True':
            print msg

    def exe_adb_command(self, cmd):
        """ Execute adb *cmd*
         Examples:
        | Exe Adb Command | shell getprop  |
        """
        return self.adb.cmd(cmd).wait()

    def exe_adb_and_result(self, cmd):
        """Execute adb *cmd* and return lines of the command"""
        lproc = self.adb.cmd(cmd)
        lproc.poll()
        lines = lproc.stdout.readlines()
        return lines

    def get_device_info(self):
        """Get Device information
        return info dictionary
        """
        return self.d.info

    def light_screen(self):
        """Light screen by wakeup.

        Examples:
        | Action     |
        |Light screen|

        Use `Light screen` to light screen.
        """

        self.d.wakeup()
        self._result = self.d.press.home()

    def open_application(self, appname):
        """Open application by it name `appname`.

        Example:
        | Action           | Argument      |
        | Open application | "com.android.settings/com.android.settings.Settings" |
        """
        appname = 'shell am start -n ' + appname
        print 'Open Application:', appname
        self._result = self.exe_adb_command(appname)

    def click_text(self, text, instance=0):
        """Click text label on screen
        instance=0 is default, change when you needed.

        Example:
        | Action     | Argument   |  Argument  |
        | Click Text | text | instance |
        """

        return self.d(text = text, instance = instance).click.wait()

    def long_click_text(self, text, instance=0):
        """
        Long Click text label on screen, *text* and *instance=0*

        Example:
        | Action     | Argument   |  Argument  |
        | Long Click Text | text | instance |
        """

        return self.d(text = text, instance=instance).long_click()

    def long_click_ui(self, **selectors):
        """
        Long Click on **selectors**
        Selector supports below parameters. Refer to UiSelector java doc for detailed information.

            text, textContains, textMatches, textStartsWith
            className, classNameMatches
            description, descriptionContains, descriptionMatches, descriptionStartsWith
            checkable, checked, clickable, longClickable
            scrollable, enabled,focusable, focused, selected
            packageName, packageNameMatches
            resourceId, resourceIdMatches
            index, instance
        Example:
        | Action     | Argument   |  Argument  |  Argument  |
        | Long Click UI | text=XXXX | className=XXX.xxxx | resourceId=xxxxxx |
        """

        return self.d(**selectors).long_click()

    def text_display_on_screen_contains(self, text):
        """Verify text display on screen

        Example:
        | Action     | Argument   |
        |Text display on screen is| text |
        """

        if self.d(text=text).exists:
            self._result = True
            return True
        else:
            self._result = False
            return False

    def object_display_on_screen(self, obj, timeout=5000):
        """ Verify *obj* UiObject display on screen
        return to self._result

        Example:
        | Action     | Argument   |
        |Object display on screen | obj |
        """
        if obj.wait.exists(timeout):
            self._result = True
            return True
        else:
            self._result = False
            return False

    def assert_expectation(self, expect, actual):
        """
        Assert Expectation and actual value
        Example:
        | Action             |   args   |   args      |
        | Assert Expectation |   324324 |  ${actual}  |
        """
        if str(expect) != str(actual) :
            raise AssertionError('Actual result is = %s, but expectation is: %s' %(str(actual), str(expect)))

    def assert_true(self, condition):
        """
        Assert True of *condition

        Example:
        |Assert True | condition |
        """
        if str(condition) != 'True':  #because only string from robotframework
            raise AssertionError('Result is = %s' % str(condition))

    def assert_result_true(self):
        """
        Assert True of *self._result

        Example:
        |Assert True |
        """
        if self._result != True:
            raise AssertionError('Result is = %s' % str(self._result))

    def wait_for_ui_exists(self, timeout, **selectors):
        """
        Return True if
          Selector is to identify specific ui object in current window.

        # To seleted the object ,text is 'Clock' and its className is 'android.widget.TextView'
        wait_for_ui_exists(text='Clock', className='android.widget.TextView')

        Selector supports below parameters. Refer to UiSelector java doc for detailed information.

            text, textContains, textMatches, textStartsWith
            className, classNameMatches
            description, descriptionContains, descriptionMatches, descriptionStartsWith
            checkable, checked, clickable, longClickable
            scrollable, enabled,focusable, focused, selected
            packageName, packageNameMatches
            resourceId, resourceIdMatches
            index, instance

        Examples:
        | Action     | Argument   |  Argument  |  Argument  |  Argument  |
        |Wait For UI Exists | timeout | text=XXXX | className=XXX.xxxx | resourceId=xxxxxx |
        """
        self._result = self.d(**selectors).wait.exists( timeout = int(timeout))
        return self._result

    def wait_and_click(self, timeout, **selectors):
        """Wait for uiselector and click"""
        if self.d(**selectors).wait.exists( timeout = int(timeout)):
            self.d(**selectors).click()

    def assert_ui_exists(self, **selectors ):
        """
        Assert UiObject appear on the screen

        Examples:
        | Action     | Argument   |  Argument  |  Argument  |  Argument  |
        |Assert UI Exists | timeout | text=XXXX | className=XXX.xxxx | resourceId=xxxxxx |
        """
        if not self.d(**selectors).wait.exists():
            raise AssertionError('UiObject does not exists %s' % selectors.items())

    def result_should_be(self, expected):
        """Verifies that the current result is `expected`.

        Example:
        | Action     | Argument   |
        |  Open application    | com.android.settings/com.android.settings.Settings |
        |  Result Should Be    | 0       |
        """
        print ( 'result is: %s\n', self._result)
        print ( 'ex is: %s\n', expected)
        if str(self._result)  != expected:
            raise AssertionError('%s != %s' % (self._result, expected))

    def click_at_coordinates(self, x, y):
        """ Click at (x,y) coordinates.
        Example:
        | Action     | Argument   |  Argument  |
        | Click At Corrdinates | x | y |
        """
        return self.d.click(int(x), int(y))

    def long_click_at_coordinates(self, x, y):
        """
        # long click (x, y) on screen
        """
        return self.d.long_click(int(x), int(y))

    def swipe(self, sx, sy, ex, ey, steps=20):
        """
        Swipe from (sx,sy) to (ex,ey)
        """
        return self.d.swipe(int(sx),int(sy), int(ex),int(ex), int(steps))

    def drag(self, sx, sy, ex, ey, steps=20):
        """
        Drag from (sx,sy) to (ex,ey)
        """
        return self.d.drag(int(sx),int(sy), int(ex),int(ex), int(steps))

    def freeze_rotation(self, rotation=True):
        """
        Freeze rotation,
        *rotation*, True is default,
        """
        return self.d.freeze_rotation(rotation)

    def set_rotation(self, rotation):
        """
        # retrieve orientation,
        # it should be "natural" or "left" or "right" or "upsidedown"

        Example:
        | Action       | Argument   |
        | Set Rotation | nature      |
        | Set Rotation | left        |
        | Set Rotation | right       |
        | Set Rotation | upsidedown  |

        """
        orientation = self.d.orientation
        if rotation == "nature" :
            self.d.orientation = "n" # or "natural"
        elif rotation == "left":
            self.d.orientation = "l" # or "left"
        elif rotation == "right":
            self.d.orientation = "r" # or "right"
        elif rotation == "upsidedown":
            self.d.orientation = "upsidedown" # or "upsidedown"
        else:
            self.d.rotation="n"

    def take_screenshot(self, scale=None, quality=None):
        """
        Take a screenshot of device and log in the report with timestamp, scale for screenshot size and quality for screenshot quality
        default scale=1.0 quality=100

        Example:
        | Action     | Argument   |  Argument  |
        | Take Screenshot | 0.5 | 80 |
        """
        output_dir = BuiltIn().get_variable_value('${OUTPUTDIR}')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        screenshot_path = '%s%s%s.png' % (output_dir, os.sep, st)
        screenshot_name = '%s%s.png' % (os.sep, st)
        self.d.screenshot(screenshot_path, scale, quality)
        logger.info('\n<a href="%s">%s</a><br><img src="%s">' % (screenshot_path, st, screenshot_name), html=True)

    def open_notification(self):
        """
        Open notification of the phone
        """
        self.d.open.notification()

    def wait_window_update(self):
        """
        wait for window update
        """
        return self.d.wait.update()

    def wait_window_idle(self):
        """
        wait for window idle
        """
        return self.d.wait.idle()

    def remove_watchers(self):
        """
        Remove UI watchers
        """
        self.d.watchers.remove()

    def get_device(self):
        """
        Get device object, you can do any command using this
        """
        return self.d

    def click_id(self, id, instance=0):
        """
        Click *id* with *instance*=0
        """
        return self.d(resourceId = id, instance = instance).click.wait()

    def long_click_id(self, id, instance=0):
        """
        Long click *id* with *instance*=0
        """
        return self.d(resourceId = id, instance=0).long_click()

    def click_description(self, description, instance=0):
        """
        Click *description* with *instance*=0
        """
        return self.d(description = description, instance = instance).long_click()

    def click_class(self, className, instance=0):
        """
        Click *className* with *instance*=0
        """
        return self.d(className =className, instance=instance).long_click()


    def type_text(self, textStr, **selectors):
        """
        type text on selectors
        like text=EditName
        """
        self.d(**selectors).set_text(textStr)

    def press_key(self, key):
        """ Press Key of following value
            home
            back
            left
            right
            up
            down
            center
            menu
            search
            enter
            delete(or del)
            recent(recent apps)
            volume_up
            volume_down
            volume_mute
            camera
            power

            Examples:
            | Action     | Argument   |
            | Press Key | home |
            | Press Key | back |
            | Press Key | left |
            | Press Key | right |
            | Press Key | recent |
            | Press Key | volume_up |
            | Press Key | camera |
        """
        if key.isdigit():
            return self.d.press(int(key))
        return self.d.press(key)

    def phone_sleep(self, timeout):
        """
        android device sleep with timeout in ms, don't use for executor sleep,
        """
        return self.d.wait(int(timeout))

    def execute_command(self, cmd, block_parent_process = True):
        """
        Execute shell *cmd* command, with block_parent_process = True

        If block_parent_process = False, kill_command is needed to terminal the child process

        Example:
        | Execute Command | ping -c 5 127.0.0.1 |
        """
        if str(block_parent_process) == str(True):
            return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        else:
            return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def kill_command(self, process, timeout=0):
        """ Kill child *process* in timeout seconds
        Some bugs after process teminated
        """
        time.sleep( float(timeout))
        process.terminate()

    def wait_for_logcat(self, log, timeout=30):
        """ Wait log exists in given timeout, return True if have, otherwise will return False
        log is your want to search, log can be a regular expression
        time in seconds, default value is 30 seconds

        Example:
        | Wait For Logcat | .*ActivityManager.*cmp=com.sonyericsson.album/com.sonyericsson.album.Main.* |
        """
        start = time.time()
        while (time.time() - start) < int(timeout):
            log_proc = self.adb.cmd("logcat -d -v time")
            returncode = log_proc.poll()
            lines = log_proc.stdout.readlines()
            for line in lines:
                rlt = re.search(log, line.rstrip())
                if rlt is not None:
                    print rlt.group(0)
                    self._result = True
                    return True
            time.sleep(2)  #sleep 2s to wait
        self._result = False
        return False

    def clear_logcat(self):
        """
        Clear logcat, it's often used before you want to use *wait_for_logcat()*
        """
        print "Clear logcat before test"
        return self.exe_adb_command("logcat -c")

    def click_object(self, obj):
        """ Click UiObject *obj*

        Exmaple:
        | ${result}    | Get UI Object | text=XXX | className=xxxx |
        | Click Object |   ${result}   |
        """
        obj.click()

    def click_ui(self, **selectors):
        """
        Click selector

        click_selector(text="Home", resourceId = "android:id/title")
        for **selector, please refer *get_ui_object()*
        Selector supports below parameters. Refer to UiSelector java doc for detailed information.

            text, textContains, textMatches, textStartsWith
            className, classNameMatches
            description, descriptionContains, descriptionMatches, descriptionStartsWith
            checkable, checked, clickable, longClickable
            scrollable, enabled,focusable, focused, selected
            packageName, packageNameMatches
            resourceId, resourceIdMatches
            index, instance
        Operation for a UiObjects:
        click, clear_text, drag(obj).to(**selector), gesture, exists, set_text, long_click
        pinch.In(percent=100, steps=10), pinch.Out(percent=100, steps=100),.swipe.right(),
        .swipe.left(steps=10),.swipe("right", steps=20),.wait.gone(),.wait.exists()
        """
        print "selectors:", selectors
        return self.d(**selectors).click()

    def get_ui_object(self, **selectors):
        """
        Get UI object with *selectors*
        you can do anything on UiObject, like click(), long_click(),wait.exists(timeout)
        examples: get_ui_object(text="Home", resourceId = "android:id/title")

        Selector supports below parameters. Refer to UiSelector java doc for detailed information.

            text, textContains, textMatches, textStartsWith
            className, classNameMatches
            description, descriptionContains, descriptionMatches, descriptionStartsWith
            checkable, checked, clickable, longClickable
            scrollable, enabled,focusable, focused, selected
            packageName, packageNameMatches
            resourceId, resourceIdMatches
            index, instance
        Operation for a UiObjects:
        click, clear_text, drag(obj).to(**selector), gesture, exists, set_text, long_click
        pinch.In(percent=100, steps=10), pinch.Out(percent=100, steps=100),.swipe.right(),
        .swipe.left(steps=10),.swipe("right", steps=20),.wait.gone(),.wait.exists()

        Exmaple:
        | ${result}    | Get UI Object | text=XXX | className=xxxx |

        """
        self._result =  self.d(**selectors)
        return self._result

    def wait_for_object_exists(self, obj, timeout=0):
        """
        Wait for UiObject *obj* exists in *timeout*= 0

        Example:
        | ${result}    | Get UI Object | text=XXX | className=xxxx |
        | Wait For Object Exists | ${result} | timeout |
        """
        self._result = obj.wait.exists(timeout = int(timeout))
        return self._result

    def wait_for_ui_gone(self, timeout=0, **selectors):
        """
        Wait for UiObject *obj* gone in *timeout*= 0

        Example:
        | ${result}    | Get UI Object | text=XXX | className=xxxx |
        | Wait For Object Gone | ${result} | timeout |

        """
        self._result = self.d(**selectors).wait.gone(timeout = int(timeout))
        return self._result

    def get_key_value(self, key, dictionary):
        """
        Get key value of dictionary
        """
        return dictionary(key)

    def get_tts(self, input_text, delete_file = False, **args ):
        """
        Get TTS voice mp3 from Google
        get_tts(input_text='tunnel snakes rule apparently', args = {'language':'en','output':'outputto.mp3'})

        Robot Framework:
        Examples:
        | Action     | Argument   |  Argument  |  Argument  |  Argument  |
        | UiTestLib.Get TTS    |   Hello world    |   False   |    output=ooo.mp3   |   language=en |
        """
        print "Get text to speech: ", input_text
        downloaded = False
        if str(delete_file) == 'True':
            if os.path.exists(args['output']):
                os.remove(args['output'])
        if os.path.exists(args['output']):
            if os.path.getsize(args['output']) <= 0:
                os.remove(args['output'])
        if args['output'] is not None:
            if not os.path.exists(args['output']):
                print 'Generating mp3 file......', args['output']
                downloaded = GoogleTTS.audio_extract(input_text, args)
            else:
                print 'Have same local file'
                downloaded = True
        if not downloaded:
            print "Downloaded TTS from Google failed, trying to download from local FTP..."
            mp3file=open(args['output'], 'w')
            mp3url = 'ftp://cnbjlx9548/atautomation/Test-Content/Croft/' + args['output']
            try:
                resp = urllib2.urlopen(mp3url, timeout=40)
                mp3file.write(resp.read())
                time.sleep(.05)
            except Exception, e:
                print e
                return False
            mp3file.close()
        return True

    def play_sound_on_pc(self, input_file):
        """
        Play sound file *input_file*

        Examples:
        | Action     | Argument   |
        | Play Sound | input_file |
        """
        return self.execute_command('mplayer %s' % input_file)

    def make_phone_call(self, number):
        """
        Make phone call to number

        | Action | args |
        | Make Phone Call | number |
        """
        cmd = "shell am start -a android.intent.action.CALL tel:%s -n com.android.incallui/com.android.incall.InCallActivity" % number
        self.exe_adb_command(cmd)
        if self.wait_for_ui_exists(1000, text="Complete action using"):
            self._result = self.click_ui(text='Phone')
            return self._result


    def end_phone_call(self):
        """
        End phone call by press end_call key, return true if successfull.
        """
        if p.get_call_status() == "2":
            p.press_key("6")
        return p.get_call_status() == "0"


    def receive_call_on_phone(self):
        """
        Receive phone calls in 20s
        """
        if self.get_call_status().find('1') >= 0:
            self.press_key(5) #KEYCODE_CALL
            time.sleep(1)
            return self.get_call_status().find('2') >= 0
        return False

    def install_apk(self, apkPath):
        """
        Install Apk
        | Action | args |
        | Install Apk | /home/xxx/bin/DrmTestActivity.apk |
        """
        return self.exe_adb_command("install -r %s" % apkPath)

    def swipe_on_ui(self, nav, **selectors):
        """
        Swipe on UI(selector), swipe right or left on selectors

        Examples:
        | Action     | args  | args              | args       |
        |Swipe on ui | right | resourceId=xxxxxx | text=xxxxx |
        Selector supports below parameters. Refer to UiSelector java doc for detailed information.

            text, textContains, textMatches, textStartsWith
            className, classNameMatches
            description, descriptionContains, descriptionMatches, descriptionStartsWith
            checkable, checked, clickable, longClickable
            scrollable, enabled,focusable, focused, selected
            packageName, packageNameMatches
            resourceId, resourceIdMatches
            index, instance
        """
        if nav == 'left':
            self.get_ui_object(**selectors).swipe.left(steps=20)
        elif nav == 'right':
            self.get_ui_object(**selectors).swipe.right(steps=20)

    def get_music_playing_status(self):
        """
        Get music playing status, 2 is playing, and 0/1 is not playing
        2 : PLAYSTATE_PLAYING
        0 : PLAYSTATE_STOPPED
        1 : PLAYSTATE_PAUSED
        """
        au_proc = self.adb.cmd("shell dumpsys audio")
        returncode = au_proc.poll()
        lines = au_proc.stdout.readlines()
        for line in lines:
            playing = re.search('PLAYSTATE_PLAYING', line.rstrip())
            stop = re.search('PLAYSTATE_STOPPED', line.rstrip())
            pause = re.search('PLAYSTATE_PAUSED', line.rstrip())
            if playing is not None:
                return 2
            elif stop is not None:
                return 0
            elif pause is not None:
                return 1

    def get_playing_music(self):
        """
        """
        au_proc = self.adb.cmd("shell dumpsys media.player")
        returncode = au_proc.poll()
        lines = au_proc.stdout.readlines()
        s = lines[-2].split('->')
        return os.path.basename(s[1].strip())

    def phone_ongoing_call_operation(self, operation):
        """
        Phone operations during ongoing call
        operations: 'mute', 'unmute', 'volumeUp', 'volumeDown','endCall'
        | Action | Args |
        | Phone Ongoing Call Operation  | mute |
        """
        opts = ['mute', 'unmute', 'volumeUp', 'volumeDown','endCall']
        def _call_operate(op):
            resourceId1='com.android.phone:id/icbp_btn_icon'
            resourceId2='com.android.incallui:id/muteButton'
            if op == opts[0] or op == opts[1]:
                if self.wait_for_ui_exists(1000, resourceId=resourceId1):
                    return self.click_ui(resourceId=resourceId1, instance=2)
                elif self.wait_for_ui_exists(1000, resourceId=resourceId2):
                    return self.click_ui(resourceId=resourceId2)
                else:
                    print op, ' is not executed correctly'
                    return False
            elif op == opts[2]:
                for i in range(1,3):
                    self.exe_adb_command("shell input keyevent --longpress KEYCODE_VOLUME_UP")
                    time.sleep(0.3)
                return True
            elif op == opts[3]:
                for i in range(1,3):
                    self.exe_adb_command("shell input keyevent --longpress KEYCODE_VOLUME_DOWN")
                    time.sleep(0.3)
                return True
            elif op == opts[4]:
                self.press_key('6')
                return True
            else:
                print "No '%s' argments" % operation
                return False

        call_status = self.get_call_status()
        if call_status.find('2') >=0:
            return _call_operate(operation)
        else:
            print "No ongoing call"
            return False



    def get_call_status(self):
        """
        Get music playing status, 0 is idle, 1 is incoming call, 2 is ongoing call
        return -1 if error happen
        'telephony.registry'
        CALL_STATE_IDLE = 0
        CALL_STATE_RINGING = 1
        CALL_STATE_OFFHOOK = 2
        """
        au_proc = self.adb.cmd("shell dumpsys telephony.registry")
        returncode = au_proc.poll()
        lines = au_proc.stdout.readlines()
        for line in lines:
            state = re.search('mCallState=', line.rstrip())
            if state is not None:
                return line.split('=')[1].strip('\r\n')

        return -1



    def send_sms(self, number, text='This is an example text body.'):
        """
        Send SMS to *number*, with *text*
        Example:
        |   Action  |   Args    |   Args    |
        | Send SMS  | 1341020138 | Hello world text message |
        """
        cmd = "shell am start -n com.android.mms/.ui.ComposeMessageActivity -a android.intent.action.SENDTO -d sms:%s --es sms_body \"%s\"" % \
              (number, text)
        self.exe_adb_command(cmd)
        if self.wait_for_ui_exists(2000, resourceId="com.android.mms:id/send_button_sms"):
            return self.click_ui(resourceId="com.android.mms:id/send_button_sms")
        else:
            print "Can't send SMS"
            return False

    def get_voice_recognision_status(self, text='updateRecipeFunctionState', timeout=40):
        """
        Get Voice Recognision result
        """
        return self.wait_for_logcat(text, int(timeout))

    def play_music_from_intent(self, music_file):
        """
        Play music from intent, file is in sdcard path
        """
        cmd = "shell am start -a android.intent.action.VIEW --activity-clear-top -n com.sonyericsson.music/.PlayerActivity -t audio/* -d file:///mnt/sdcard/" + music_file
        log_proc = self.adb.cmd(cmd)
        returncode = log_proc.wait()
        lines = log_proc.stdout.readlines()
        print returncode, lines
        return returncode

    def push_file(self, local_file, remote_file = '/sdcard/'):
        """
        Push local_file to remote_file
        """
        cmd = "push %s %s" % (local_file, remote_file)
        log_proc = self.adb.cmd(cmd)
        returncode = log_proc.wait()
        lines = log_proc.stdout.readlines()
        print lines
        print "return value:", returncode

    def scroll_to_find(self, **args):
        """
        scroll to find object
        """
        return self.d(scrollable=True).scroll.to(**args)

    def start_timer(self):
        """
        Start timer and wait end_timer to stop
        """
        self.starttime = time.time()

    def end_timer(self):
        """
        Return time in seconds
        """
        return "%.2f" % (time.time() - self.starttime)

    def get_adb_return_str(self, cmd):
        """
        run adb command and return result
        """
        log_proc = self.adb.cmd(cmd)
        returncode = log_proc.wait()
        return log_proc.stdout.readlines()

    def play_music_by_phone(self):
        """
        Play music by phone
        """
        playing_status = self.get_music_playing_status()
        if playing_status == 2 :
            return True

        self.open_application("com.sonyericsson.music/com.sonyericsson.music.MusicActivity --activity-clear-top -W")
        if self.wait_for_ui_exists(1500, resourceId='android:id/up'):
            self.click_ui(resourceId='android:id/up')
        elif self.wait_for_ui_exists(1500, description='Open navigation menu'):
            self.click_ui(description='Open navigation menu')

        if self.wait_for_ui_exists(1500, text="Songs"):
            self.click_ui(text="Songs")
        elif self.wait_for_ui_exists(1500, text='My Library'):
            self.click_ui(text='My Library')
            self.click_ui(text='Songs')

        return self.click_ui(text='Shuffle all')

    def goto_home(self):
        self.press_key('back')
        self.press_key('back')
        self.press_key('back')
        self.press_key('home')

    def scroll_forward(self, oritation='vert', steps=20):
        if oritation == 'horiz':
            self.d(scrollable=True).scroll.horiz.forward(steps)
        else:
            self.d(scrollable=True).scroll(steps)

    def scroll_backward(self, oritation='vert', steps=10):
        if oritation == 'horiz':
            self.d(scrollable=True).scroll.horiz.backward(steps)
        else:
            self.d(scrollable=True).scroll.backward(steps)
    def fling_forward(self, oritation='vert', max_swipes=5):
        if oritation == 'horiz':
            self.d(scrollable=True).fling.horiz.forward(max_swipes=max_swipes)
        else:
            self.d(scrollable=True).fling.forward(max_swipes=max_swipes)

    def fling_backward(self, oritation='vert', max_swipes=5):
        if oritation == 'horiz':
            self.d(scrollable=True).fling.horiz.backward(max_swipes=max_swipes)
        else:
            self.d(scrollable=True).fling.backward(max_swipes=max_swipes)

    def fling_toBeginning(self, oritation='vert', max_swipes=5):
        if oritation == 'horiz':
            self.d(scrollable=True).fling.horiz.toBeginning(max_swipes=max_swipes)
        else:
            self.d(scrollable=True).fling.toBeginning(max_swipes=max_swipes)

    def fling_toEnd(self, oritation='vert', max_swipes=5):
        if oritation == 'horiz':
            self.d(scrollable=True).fling.horiz.toEnd(max_swipes=max_swipes)
        else:
            self.d(scrollable=True).fling.toEnd(max_swipes=max_swipes)

    def get_uptime(self):
        """up time: 1 days, 23:50:32, idle time: 4 days, sleep time: 1 days 03:54:24"""
        line = self.exe_adb_and_result('shell uptime')
        if not len(line):
            return -1
        #line = "up time: 1 days, 23:50:32, idle time: 4 days, sleep time: 1 days 03:54:24"
        #line = "up time: 00:39:34, idle time: 03:47:15, sleep time: 00:00:00"
        line = line[0]
        uptime = line[0:line.find('idle time')]
        uptime = uptime.replace('up time: ','')
        uptime = uptime.split(',')
        day = 0
        h = 0
        if uptime[0].find('days')>0:
            day = uptime[0].split()[0]
            h = uptime[1]
            h = h.split(':')
            hr = int(h[0])
            m = int(h[1])
            s = int(h[2])
            h = hr*3600+m*60+s
        else:
            h = uptime[0]
            h = h.split(':')
            hr = int(h[0])
            m = int(h[1])
            s = int(h[2])
            h = hr*3600+m*60+s
        uptime = int(day)*24*3600 + h
        return uptime
        
    def run_instrument_case(self, runner, package, clz = "", testName = ""):
        # adb install ./out/target/product/eagle/data/app/wifitoggletest.apk 
        # adb shell am instrument -w com.example.wifitoggle.tests/android.test.InstrumentationTestRunner
        if len(testName) or len(clz):
            print self.exe_adb_and_result('shell am instrument -c %s.%s#%s -w %s/%s' %(package, clz, testName, package, runner))
        else:
            print self.exe_adb_and_result('shell am instrument-w %s/%s' %(package, runner))
    def run_uiautomator_case(self, jarName, clazz, testcaseName=""):
        if len(testcaseName):
            print self.exe_adb_and_result('shell uiautomator runtest %s -c %s#%s' % (jarName, clazz, testcaseName) )
        else:
            print self.exe_adb_and_result('shell uiautomator runtest %s -c %s' % (jarName, clazz) )
            
if __name__ == "__main__":
    #pass
    p = UiTestLib('ec88c23e')
    print p.get_uptime()
    #print p.get_device_info
    #p.click_ui(text='WPS Office')
    #p.make_phone_call('10086')
    #p.send_sms('10086')
    #print p.wait_for_logcat("Exception")
    ##time.sleep(8)
    #if p.get_call_status() == "2":
    #    p.press_key("6")
    #p = UiTestLib('CB51246PTS')
    #print p.play_music_by_phone()
    #print p.phone_ongoing_call_operation('mute')
    #time.sleep(5)
    #print p.phone_ongoing_call_operation('unmute')




