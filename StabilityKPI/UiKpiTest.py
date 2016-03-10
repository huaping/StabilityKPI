#!/usr/bin/env python
# -*- coding: utf-8 -*-

from UiAutoTestLib import UiTestLib
import time
import re
import random

class UiKpiTest(UiTestLib):
    """
    Test Lib for Ui Automation test
    """
    def __init__(self, Serial = None):
        UiTestLib.__init__(self, Serial)
    #################################################
    #
    #       Telephony and phonebook
    #################################################
    def dial_number(self, number):
        try:
            self.open_application("com.android.dialer/.DialtactsActivity --activity-clear-top")
            self.wait_for_ui_exists(1500, resourceId="com.android.dialer:id/floating_action_button")
            self.click_ui(resourceId="com.android.dialer:id/floating_action_button")
            self.type_text(number, resourceId="com.android.dialer:id/digits")
            time.sleep(1)
            self.click_ui(resourceId="com.android.dialer:id/dialpad_floating_action_button")
            return True
        except Exception, e:
            print Exception, ":", e
            print "Exception happens"
            return False

    def add_new_contact(self, name, number):
        """Add contact with name and number"""
        add_btn = 'com.android.contacts:id/floating_action_button'
        save_btn = 'com.android.contacts:id/save_menu_item'
        if self.wait_for_ui_exists(1000, resourceId=add_btn):
            self.click_ui(resourceId=add_btn)
        else:
            return False
        if self.wait_for_ui_exists(300, textContains='You can synchronize your'):
            self.click_text('PHONE')
        self.wait_for_ui_exists(1000, text='Add new contact')
        self.type_text(name, text='Name', className='android.widget.EditText')
        self.type_text(number, text='Phone', className='android.widget.EditText')
        self.click_ui(resourceId=save_btn)

    def delete_contact(self, name):
        """delete contacts"""
        large_icon = 'com.android.contacts:id/photo_touch_intercept_overlay'
        if self.scroll_to_find(text=name):
            self.click_ui(text=name)
            self.wait_for_ui_exists(1000, resourceId=large_icon)
            self.press_key('menu')
            self.click_ui(text='Delete')
            self.click_ui(text="OK")
        else:
            return False

    def wait_and_connection(self, timeout=8):
        """Wait 5 seconds to end call when connected."""
        start = time.time()
        while (time.time() - start) < int(timeout):
            status = self.get_call_status()
            print 'wait_and_connection call status:', status
            if status == '2':
                return True
            else:
                time.sleep(1)
        return False

    def wait_end_call(self, timeout = 4):
        """Wait call established and end call after timeout"""
        try:
            if self.wait_and_connection(8):
                self.wait_for_ui_gone(15000, textContains="Calling via")
                self.logmsg("Calling via end")
                self.wait_for_ui_exists(8000, resourceId='com.android.dialer:id/elapsedTime')
                time.sleep(int(timeout))
                status = self.get_call_status()
                if status == '2':
                    self.logmsg("End call because it in calling")
                    self.press_key('6')   #end call key
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            print "Exception happens"
            return False

    def background_call(self):
        """press home key during call"""
        try:
            if self.wait_and_connection(8):
                self.wait_for_ui_gone(15000, textContains="Calling via")
                self.wait_for_ui_exists(8000, resourceId='com.android.dialer:id/elapsedTime')
                status = self.get_call_status()
                print 'call status:', status
                if status == '2':
                    self.logmsg("press Home key because it in calling")
                    self.press_key('home')
                status = self.get_call_status()
                return status == '2'
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            print "Exception happens"
            return False

    def end_call(self):
        """press end call key"""
        status = self.get_call_status()
        if status == '2':
            self.logmsg("End call because it in calling")
            self.press_key('6')   #end call key

    ##################################
    #
    #       Messaging
    #
    ##################################
    def open_message_app(self):
        self.open_application('com.android.mms/.ui.ConversationList')
        return self.wait_for_ui_exists(3000, packageName='com.android.mms')

    def create_new_message(self):
        #com.android.mms:id/floating_action_button
        #com.android.mms:id/recipients_editor
        #com.android.mms:id/embedded_text_editor  Type message
        #send com.android.mms:id/send_button_sms
        #com.android.mms:id/send_button_mms  MMS
        pass

    def open_message(self, content):
        """open message by content"""
        try:
            if not self.wait_for_ui_exists(500, textContains=content):
                if self.scroll_to_find(textContains=content):
                    self.click_ui(textContains=content)
                    return True
            else:
                self.click_ui(textContains=content)
                return True
        except Exception, e:
            print Exception, ":", e
            self.logmsg("open message failed.")
            return False

    def forward_message(self, phoneNum, content, mms):
        """preconditon: open message
        phoneNum: to send to
        content: message to find and forward.
        """
        print 'mms:',mms
        try:
            if not self.wait_for_ui_exists(500, textContains=content):
                self.scroll_to_find(textContains=content)
            self.long_click_ui(textContains=content)
            #wait for com.android.mms:id/forward
            forward_btn = 'com.android.mms:id/forward'
            if self.wait_for_ui_exists(2000, resourceId=forward_btn):
                self.click_ui(resourceId=forward_btn)
                recipt_editor = 'com.android.mms:id/recipients_editor'
                self.wait_for_ui_exists(1000, resourceId=recipt_editor)
                self.type_text(phoneNum, resourceId=recipt_editor)
                if mms == 'True':
                    self.click_ui(resourceId='com.android.mms:id/send_button_mms')
                    time.sleep(5)
                else:
                    self.click_ui(resourceId='com.android.mms:id/send_button_sms')
                time.sleep(1)
                self.press_key('back')  #input method
                self.press_key('back')  #msg list
                self.open_message_app()
                if mms == 'True':
                    return self.wait_for_ui_exists(2000, textContains='Fwd:')
                else:
                    return self.wait_for_ui_exists(2000, textContains='Me:')
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Forward message exception happens.")
            return False

    def delete_msg_by_phoneNum(self, contact):
        """precondition: conversation mode
        long press phone number/contact name to delete conversation
        """
        try:
            self.open_message_app()
            self.long_click_ui(textContains=contact)
            delete_btn = 'com.android.mms:id/delete'
            if self.wait_for_ui_exists(2000, resourceId=delete_btn):
                self.click_id(delete_btn)
                self.click_ui(resourceId="android:id/button1")  #confirm delete
                return True
            return not self.wait_for_ui_exists(300, text=contact)
        except Exception, e:
            print Exception, ":", e
            return False

    def play_slideshow_mms(self):
        """precondition: the mms is opened"""
        id_slideshow = 'com.android.mms:id/play_slideshow_button'
        try:
            if self.wait_for_ui_exists(2000, resourceId=id_slideshow):
                self.click_id(id_slideshow)
                return self.wait_for_ui_exists(1000, text="Message details")
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Play slide show exception happens.")
            return False

    #################################################
    #
    #  Browser test cases
    #
    #################################################
    def open_browser_app(self):
        """Open browser application"""
        self.open_application('com.android.swe.browser/com.android.browser.BrowserLauncher')
        if self.wait_for_ui_exists(3000, text='Quit'):
            self.press_key('back')
        return self.wait_for_ui_exists(3000, packageName='com.android.swe.browser')

    def close_browser_app(self):
        moreBtn = 'com.android.browser:id/more_browser_settings'
        self.press_key('menu')
        self.scroll_to_find(text='Exit')
        self.click_text('Exit')
        self.click_id("android:id/button1") #Quit
        return not self.wait_for_ui_exists(300, packageName='com.android.swe.browser')

    def clear_browser_privacy(self):
        """preconditon: in browser main window
        postcondition: in browser main window"""
        moreBtn = 'com.android.browser:id/more_browser_settings'
        try:
            if self.wait_for_ui_exists(500, resourceId=moreBtn):
                self.click_id(moreBtn)
                self.click_text('Settings')
                self.click_text("Privacy & security")
                self.click_text('Clear stored data')
                self.click_text('Clear selected items')
                self.click_id("android:id/button1") #OK
                #go to browser main window
                self.press_key('back')
                self.press_key('back')
                self.press_key('back')
                return self.wait_for_ui_exists(800, resourceId=moreBtn)
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Clear browser privacy exception happens")
            return False

    def open_page(self,  url='http://news.baidu.com', containsVerifiy='m.baidu.com/news'):
        """precodtion: in browser main window"""
        try:
            self.type_text(url, resourceId='com.android.browser:id/url')
            time.sleep(0.5)
            self.press_key('enter')
            time.sleep(2)
            return self.wait_for_ui_exists(6000, textContains=containsVerifiy)
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open Page Failed.')
            return False

    def open_download_file(self, fileName, timeout=1000):
        """Download file"""
        try:
            self.open_application('com.android.providers.downloads.ui/.DownloadList')
            downList = self.wait_for_ui_exists(1000, resourceId='com.android.documentsui:id/toolbar')
            if downList:
                if not self.wait_for_ui_exists(int(timeout), textContains=fileName):
                    return False
                self.click_ui(textContains=fileName)
                print time.time()
                if self.open_with('HTML Viewer'):
                    print "HTML viewer"
                elif self.open_with('VideoPlayer'):
                    print "video player"
                print time.time()
                return True
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open failed.')
            return False

    def verify_open(self, appName, **selectors):
        """Verify intent open files, try to use appName to open and verify **selectors"""
        try:
            self.open_with(appName)
            return self.wait_for_ui_exists(3000, **selectors)
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Verified Failed")
            return False

    def open_with(self, appName):
        """popup Open with  *appName"""
        print 'open with %s' % appName
        try:
            if self.wait_for_ui_exists(300, textContains="Open with"):
                if self.d(resourceId='android:id/button_once').enabled:
                    self.click_id('android:id/button_once')
                    return True
                if self.wait_for_ui_exists(300, text=appName):
                    self.click_text(appName)
                else:
                    return False
                time.sleep(1)
                if self.wait_for_ui_exists(500, resourceId='android:id/button_once'):
                    self.click_id('android:id/button_once')
                    return True
            else:
                return True
        except Exception, e:
            print Exception, ":", e
            self.logmsg("open_with Failed")
            return False

    def delete_file_in_downloads(self, fileName, delete_all='False'):
        try:
            self.open_application('com.android.providers.downloads.ui/.DownloadList')
            if self.wait_for_ui_exists(300, text='No items'):
                print "No file exits"
                return True
            downList = self.wait_for_ui_exists(2000, resourceId='com.android.documentsui:id/toolbar')
            print downList
            if delete_all=='True':
                trytime=10
                while trytime>0:
                    if self.wait_for_ui_exists(300, resourceIdMatches='.*icon_mime'):
                        self.long_click_ui(resourceIdMatches='.*icon_mime')
                        self.click_ui(description='More options')  #delete button
                    if self.wait_for_ui_exists(300, text='No items'):
                        return True
                    trytime = trytime - 1
            if downList:
                self.wait_for_ui_exists(800, textContains=fileName)
                self.long_click_ui(textContains=fileName)
                self.click_ui(description='More options')  #delete button
                return self.wait_for_ui_gone(2000, textContains=fileName)
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('delete failed.')
            return False

    def download_save_file(self, timeout):
        """Precondition: On Download settings UI, press OK to download"""
        status = self.wait_for_ui_exists(int(timeout), resourceIdMatches=".*download_settings_title")
        if not status:
            print "timeout %s when download file" % timeout
            return False
        if self.wait_for_ui_exists(3000, resourceIdMatches='.*download_start'):
            self.click_ui(resourceIdMatches='.*download_start')
            if self.wait_for_ui_exists(500, textContains='File already exists'):
                self.click_text('OK')
            return True
        else:
            return False

    def refesh_page(self):
        if not self.wait_for_ui_exists(2000, resourceIdMatches='.*more_browser_settings'):
            return False
        self.click_ui(resourceIdMatches='.*more_browser_settings')
        #Refresh
        self.click_ui(resourceIdMatches='.*button_three')
    #############################################
    #
    #       Home Icon Open
    #
    #############################################
    def open_app_from_Home(self, appName, packageName):
        """open Application from Home Launcher3"""
        try:
            self.press_key('home')
            # try 5 times to find app name on home
            if self.wait_for_ui_exists(500, text=appName):
                self.click_text(appName)
                return self.wait_for_ui_exists(5000, packageName=packageName)
            self.fling_toBeginning(oritation='horiz')
            for i in range(5):
                if self.wait_for_ui_exists(800, text=appName):
                    self.click_text(appName)
                    break
                else:
                    self.fling_forward(oritation='horiz')
                    time.sleep(0.3)
            result=self.wait_for_ui_exists(5000, packageName=packageName)
            if not result:
                self.logmsg('Open App %s Failed' % appName)
            return result
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open application %s exception' % appName)
            return False

    ################## Multimedia ###################
    def open_recorder_app(self):
        """open recorder"""
        try:
            self.open_application('com.cloudminds.soundrecorder/.SoundRecorderActivity')
            ckId='com.cloudminds.soundrecorder:id/bg_recorder_home_mike_nor'
            return self.wait_for_ui_exists(2000, resourceId=ckId)
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open Recorder Failed in 2sec')
            return False
    def delete_record_files(self):
        try:
            lstHome='com.cloudminds.soundrecorder:id/btn_recorder_home_list'
            ckb = 'com.cloudminds.soundrecorder:id/select_checkbox'
            deleteBtn = 'com.cloudminds.soundrecorder:id/delectOrShare'

            uiStatus = self.check_record_ui_status()
            if uiStatus == 0:
                self.click_id(lstHome)
            elif uiStatus == 1:
                pass
            elif uiStatus == 3:
                self.press_key('back')
            elif uiStatus == 4:
                pass
            else:
                return False
            if self.wait_for_ui_exists(1000, text='The recording file is empty'):
                self.logmsg('There is no files to delete')
                return True
            self.click_ui(description='More options')  #more button
            self.click_text('delete')
            self.click_id(ckb)
            time.sleep(0.2)
            self.click_text('delete')
            self.click_id('android:id/button1')
            time.sleep(0.2)
            return not self.wait_for_ui_exists(1000, textMatches=".*\d{8}\d+\..*")
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Delete failed.')
            return False

    def check_record_ui_status(self):
        """return status 0, 1, 2, 3
        0  --- main window
        1   -- saved recordings window
        2   -- search window
        3   --- Select voice recordings
        4   --- play record window
        """
        if self.wait_for_ui_exists(300, text='Sound Recorder'):
            return 0
        elif self.wait_for_ui_exists(300, text='Saved Recordings'):
            return 1
        elif self.wait_for_ui_exists(300, text='Select voice recordings'):
            return 3
        elif self.wait_for_ui_exists(200, resourceIdMatches='.*seekBar'):
            return 4
        elif self.wait_for_ui_exists(300, resourceIdMatches='.*/search_text'):
            return 2

        else:
            return 255

    def record_voice(self, duration):
         #com.cloudminds.soundrecorder:id/text_time
         #com.cloudminds.soundrecorder:id/btn_recorder_home_recording
         #com.cloudminds.soundrecorder:id/btn_recorder_home_list
         #com.cloudminds.soundrecorder:id/ico_recorder_home_circle_3
         #org.codeaurora.snapcam:id/preview_thumb
         """stauts"""
         try:
             status = self.check_record_ui_status()
             if status == 0:
                self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             elif status == 1:
                 self.click_ui(resourceIdMatches='.*btn_recorder_list_recording')
             elif status == 3:
                 self.press_key('back')
                 self.press_key('back')
                 self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             else:
                 return False

             self.wait_for_ui_exists(3000, resourceIdMatches='.*ico_recorder_home_circle_3')
             time.sleep(int(duration))
             self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             time.sleep(1)
             return self.wait_for_ui_exists(1000, textMatches=".*\d{8}\d+\..*")

         except Exception, e:
             print Exception, ":", e
             self.logmsg('Record voice failed.')
             return False

    def play_recorded_voice(self):
        #com.cloudminds.soundrecorder:id/seekBar
        try:
            uiStatus = self.check_record_ui_status()
            if uiStatus == 0:
                self.click_ui(resourceIdMatches='.*btn_recorder_home_list')
            elif uiStatus == 1:
                pass
            elif uiStatus == 3:
                self.press_key('back')
            else:
                return False
            if self.wait_for_ui_exists(1000, text='there is no file'):
                self.logmsg('There is no files to delete')
                return False
            self.click_ui(resourceIdMatches='.*recording_name')
            time.sleep(4)
            return self.wait_for_ui_exists(3000, resourceIdMatches='.*seekBar')
        except:
            self.logmsg('Play sound error')
            return False

    def open_music_app(self):
        """"""
        try:
            self.open_application('com.cloudminds.music2/.ui.activities.HomeActivity')
            return self.wait_for_ui_exists(3000, packageName='com.cloudminds.music2')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Exception when open music app')
            return False

    def play_music_shuffle_all(self):
        #audio_player_current_time
        #action_button_play
        #music name: bottom_action_bar_line_one
        #playing UI: action_button_previous, action_button_next
        try:
            self.click_ui(description='More options')
            self.click_text('Shuffle all')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Play music shuffle all Exception happens')
            return False

    def open_ongoing_music(self):
        try:
            self.click_ui(resourceIdMatches='.*/bottom_action_bar_line_one')
            return self.wait_for_ui_exists(2000, resourceIdMatches='.*/action_button_previous')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('open ongoing music failed, exception happens.')
            return False

    def play_next_music(self, duration):
        try:
            if not self.wait_for_ui_exists(800, resourceIdMatches='.*/action_button_previous'):
                return False
            self.click_ui(resourceIdMatches='.*/action_button_next')
            time.sleep(int(duration))
            return self.wait_for_ui_exists(300, resourceIdMatches='.*/action_button_previous')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Playing next music failed, exception happens.')
            return False
    def pause_music_playing(self):
        try:
            self.open_notification()
            if self.wait_for_ui_exists(3000, description='Pause', resourceIdMatches='.*action0'):
                self.click_ui(description='Pause', resourceIdMatches='.*action0')
            return self.wait_for_ui_exists(3000, description='Play', resourceIdMatches='.*action0')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Stop music playing failed or no playing music')
            return False

    ##### Camera  #####
    def open_camera_app(self):
        """"""
        #org.codeaurora.snapcam:id/filmstrip_bottom_controls   --video mode
        #org.codeaurora.snapcam:id/shutter_button
        #org.codeaurora.snapcam:id/camera_switcher
        #org.codeaurora.snapcam:id/mdp_preview_content ---still mode
        #org.codeaurora.snapcam:id/preview_thumb
        try:
            if self.wait_for_ui_exists(300, resourceIdMatches='.*shutter_button'):
                return True
            self.open_application('org.codeaurora.snapcam/com.android.camera.CameraLauncher')
            if self.wait_for_ui_exists(200, textContains="Remember photo location"):
                self.click_text('Yes')
            return self.wait_for_ui_exists(8000, resourceIdMatches='.*shutter_button')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Exception happens when openning camera app')
            return False

    def open_camera_mode(self, mode):
        """
        still --- still mode
        video --- video mode
        """
        #Switch to photo
        #Switch to video
        #Switch to panorama
        try:
            #film = self.wait_for_ui_exists(1000, resourceIdMatches='.*filmstrip_bottom_controls')
            mdp = self.wait_for_ui_exists(1000, resourceIdMatches='.*mdp_preview_content')
            if mode == 'still':
                if self.wait_for_ui_exists(300, resourceIdMatches='.*camera_switcher'):
                    self.click_ui(resourceIdMatches='.*camera_switcher')
                    time.sleep(1)
                self.click_description('Switch to photo')
                time.sleep(1)
                return self.wait_for_ui_exists(1000, resourceIdMatches='.*mdp_preview_content')
            elif mode == 'video':
                if self.wait_for_ui_exists(300, resourceIdMatches='.*camera_switcher'):
                    self.click_ui(resourceIdMatches='.*camera_switcher')
                    time.sleep(1)
                self.click_description('Switch to video')
                time.sleep(1)
                return self.wait_for_ui_exists(2000, resourceIdMatches='.*filmstrip_bottom_controls')
            else:
                self.logmsg('Please give correct video, still parameter')
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Switch camera Exception')
            return False

    def capture_picture_video(self, mode, duration=60):
        """Capture video/picture
        mode = still    is for photo
        mode = video    is for video
        """
        try:

            if mode=='still':
                self.open_camera_mode('still')
                self.click_ui(resourceIdMatches='.*shutter_button')
                time.sleep(3)
                return True
            elif mode=='video':
                self.open_camera_mode('video')
                self.click_ui(resourceIdMatches='.*shutter_button')
                time.sleep(int(duration))
                self.click_ui(resourceIdMatches='.*shutter_button')
                return True
            else:
                self.logmsg('cannot switch to still mode')
                return False
        except Exception, e:
            print Exception, ":", e
            return False
    def open_file_from_camera(self, delete='False'):
        #com.android.gallery3d:id/photopage_bottom_controls
        #com.android.gallery3d:id/photopage_bottom_controls
        #com.android.gallery3d:id/gl_root_view
        try:
            self.click_ui(resourceIdMatches='.*preview_thumb')
            self.press_key('menu')
            #double press menu if menu is not there
            if not self.wait_for_ui_exists(400, text='Delete'):
                self.press_key('menu')
            if self.wait_for_ui_exists(400, text='Mute'):
                self.logmsg('it is a movie')
                self.press_key('back')
                self.click_ui(resourceIdMatches='.*gl_root_view')
                self.verify_open('VideoPlayer', resourceIdMatches='.*videoProgress')
                #MTBF playing for 10s
                time.sleep(10)
                if not self.wait_for_ui_exists(1000, resourceIdMatches='.*photopage_bottom_controls'):
                    self.press_key('back')
                self.delete_files_gallery_view(delete)
                return True

            elif self.wait_for_ui_exists(400, text='Slideshow'):
                self.logmsg('it is a photo')
                self.press_key('back')
                self.delete_files_gallery_view(delete)
                return True

        except Exception, e:
            print Exception, ":", e
            self.logmsg('no picture or exception happens')
            return False

    def delete_files_gallery_view(self, delete):
        """delete file on gallery"""
        try:
            if delete == 'True':
                self.press_key('menu')
                #double press menu if menu is not there
                if not self.wait_for_ui_exists(400, text='Delete'):
                    self.press_key('menu')
                self.click_text('Delete')
                self.click_id('android:id/button1')
                return True
            else:
                return True
        except Exception, e:
            print Exception, ":", e
            return False

    def crash_watchers(self):
        self.d.watcher('AUTO_FC_WHEN_ANR').when(textMatches='.*is.*responding.*').click(resourceIdMatches='.*button1')
        self.d.watcher('Auto_FC_CRASH').when(textMatches='Unfortunately.*stopped.*').click(resourceIdMatches='.*button1')
        self.d.watchers.run()

    ### File manager handling  ####
    def open_file_manager(self):
        #Folder, Category
        #Storage information
        self.open_application('com.cloudminds.filemanager/.MainActivity')
        return self.wait_for_ui_exists(2000, packageName='com.cloudminds.filemanager')

    def filemanager_tab(self, tab):
        if tab == 'folder':
            self.click_text('Folder')
            return self.wait_for_ui_exists(2000, textMatches='Phone storage.*')
        else:
            self.click_text('Category')
            return self.wait_for_ui_exists(2000, text='Storage information')

    def filemanager_create_folder(self, folderName, storage='internal'):
        try:
            self.filemanager_tab('folder')
            self.click_ui(textMatches='Phone storage.*')
            time.sleep(0.3)
            self.press_key('menu')
            self.click_text('New folder')
            self.type_text(folderName, resourceIdMatches='.*text_ed')
            time.sleep(0.3)
            self.click_ui(resourceIdMatches='.*button1')
            return True
        except Exception, e:
            print Exception, ':', e
            return False

    def filemanager_check_file_exists(self, fileName):
        try:
            toFind = fileName+'.*'
            self.scroll_to_find(textMatches=toFind)
            return self.wait_for_ui_exists(1000, textMatches=toFind)
        except Exception, e:
            return False
            print Exception, ':', e

    def filemanager_delete_file(self, fileName):
        try:
            toFind = fileName+'.*'
            self.scroll_to_find(textMatches=toFind)
            self.long_click_ui(textMatches=toFind)
            self.click_ui(resourceIdMatches='.*action_delete')
            self.click_ui(resourceIdMatches='.*button1')
            return True
        except Exception, e:
            print Exception, ':', e
            return False

    ########################################################
    #           PIM
    #########################################################
    def open_callendar_app(self):
        """"""
        self.open_application('com.android.calendar/.AllInOneActivity')
        return self.wait_for_ui_exists(3000, resourceIdMatches='.*action_today')

    def create_callendar_events(self, title):
        self.calendar_main_window()
        self.click_ui(resourceIdMatches='.*floating_action_button')
        self.wait_for_ui_exists(2000, resourceIdMatches='.*title')
        self.type_text(title, resourceIdMatches='.*title')
        self.type_text('Wangjing SOHU A, Beijing, China', resourceIdMatches='.*location')
        self.click_text('Done')

    def check_callendar_events(self, title):
        self.calendar_main_window()
        self.press_key('menu')
        self.click_text('Delete events')
        return self.wait_for_ui_exists(3000, textContains=title)

    def delete_callendar_events(self):
        self.calendar_main_window()
        self.press_key('menu')
        self.click_text('Delete events')
        if self.wait_for_ui_exists(2000, resourceIdMatches='.*checkbox'):
            chkbox = self.d(resourceIdMatches='.*checkbox')
            for i in range(chkbox.count):
                self.click_ui(resourceIdMatches='.*checkbox', instance=i)

            self.click_ui(resourceIdMatches='.*action_delete')
            self.click_ui(resourceIdMatches='.*button1')
            return True
        else:
            return False

    def callendar_status(self):
        """
        0       --- Main window
        1       --- All events
        2       --- Create Events
        """
        if self.wait_for_ui_exists(300, resourceIdMatches='.*action_today'):
            return 0
        elif self.wait_for_ui_exists(300, text='All events'):
            return 1
        elif self.wait_for_ui_exists(300, resourceIdMatches='.*location'):
            return 2

    def calendar_main_window(self):
        status =self.callendar_status()
        if status == 0:
            return True
        elif status == 1:
            self.press_key('back')
        elif status == 2:
            self.press_key('back')
        else:
            self.press_key('back')
        return self.wait_for_ui_exists(300, resourceIdMatches='.*action_today')

    def open_alarm_app(self):
        """Open alarm application"""
        self.open_application('com.android.deskclock/.DeskClock')
        return self.wait_for_ui_exists(1000, packageName='com.android.deskclock')

    def clock_open(self, mode):
        """
        mode = alarm
        mode = clock
        mode = timer
        mode = stopwatch
        """
        if mode == 'alarm':
            if self.wait_for_ui_exists(1000, resourceIdMatches='.*alarms_list'):
                return True
            self.click_ui(description='Alarm')
            return self.wait_for_ui_exists(1000, resourceIdMatches='.*alarms_list')
        elif mode == 'clock':
            if self.wait_for_ui_exists(1000, resourceIdMatches='.*cities'):
                return True
            self.click_ui(description='Clock')
            return self.wait_for_ui_exists(1000, resourceIdMatches='.*cities')
        elif mode == 'timer':
            if self.wait_for_ui_exists(1000, resourceIdMatches='.*timer_time_text'):
                return True
            self.click_ui(description='Timer')
            return self.wait_for_ui_exists(1000, resourceIdMatches='.*timer_time_text')
        elif mode == 'stopwatch':
            if self.wait_for_ui_exists(1000, resourceIdMatches='.*stopwatch_time_text'):
                return True
            self.click_ui(description='Stopwatch')
            return self.wait_for_ui_exists(1000, resourceIdMatches='.*stopwatch_time_text')
        else:
            return False

    def delete_all_alarms(self):
        """delete all alarms"""
        try:
            while self.wait_for_ui_exists(400, resourceIdMatches='.*arrow'):
                if not self.wait_for_ui_exists(300, resourceIdMatches='.*delete'):
                    self.click_ui(resourceIdMatches='.*arrow')
                self.click_ui(resourceIdMatches='.*delete')
                if self.wait_for_ui_exists(300, text='Alarm deleted.'):
                    print 'Delete alarm successfully.'
            return self.wait_for_ui_exists(3000, textContains='No Alarms')
        except Exception, e:
            print Exception, ':', e
            return False

    def add_default_alarm(self):
        try:
            if not self.wait_for_ui_exists(1000, resourceId='com.android.deskclock:id/fab'):
                print "not in add alarm UI"
                return False
            self.click_id('com.android.deskclock:id/fab')
            self.click_id('android:id/button1')
            return self.wait_for_ui_exists(2000, resourceIdMatches='.*digital_clock')
        except Exception, e:
            print Exception, ':', e
            return False
    ########### Email ##########
    def open_email_app(self):
        self.open_application('com.android.email/.activity.Welcome')
        return self.wait_for_ui_exists(3000, resourceIdMatches='.*conversation_list_view')

    def email_navigation(self, where):
            """
            Inbox
            Starred
            Unread
            Drafts
            Outbox
            Sent
            Trash
            """
            try:
                self.email_goto_main()
                if self.d(resourceIdMatches='.*mail_toolbar').child(text=where).exists:
                    print 'alreayd in %s ' % where
                    return True
                self.click_ui(description='Navigate up')
                time.sleep(0.5)
                self.click_ui(resourceIdMatches='.*name', text=where)
                time.sleep(0.5)
                return self.d(resourceIdMatches='.*mail_toolbar').child(text=where).exists
            except Exception, e:
                print Exception, ':', e
                return False

    def open_email_subject(self, title):
        try:
            if self.wait_for_ui_exists(2000, resourceIdMatches='.*conversation_list_view'):
                self.click_ui(descriptionMatches='.*%s.*'%title)
                return self.wait_for_ui_exists(2000, resourceIdMatches='.*subject_and_folder_view', descriptionMatches='.*%s.*'%title)
            else:
                return False
        except Exception, e:
            print Exception, ':', e
            return False

    def email_ui_status(self):
        """
        0   -- inbox
        2 -- starred
        3 --- unread
        4 --- Sent
        5 --- Trash
        6 ---  a openned mail conversation
        255 -- for main navigation UI, which can setup a new mail
        """
        if self.wait_for_ui_exists(500, resourceIdMatches='.*compose_button'):
            return 255
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Inbox').exists:
            return 0
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Starred').exists:
            return 1
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Unread').exists:
            return 2
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Outbox').exists:
            return 3
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Sent').exists:
            return 4
        elif self.d(resourceIdMatches='.*mail_toolbar').child_by_text('Trash').exists:
            return 5
        elif self.wait_for_ui_exists(500, resourceIdMatches='.*content_pane'):
            return 6
        else:
            return -1

    def forward_email(self, email_addr):
        # on an openned message
        try:
            self.click_ui(resourceIdMatches='.*overflow')
            self.click_text('Forward')
            if not self.wait_for_ui_exists(1000, textStartsWith='Fwd:'):
                return False
            self.type_text(email_addr, resourceId='com.android.email:id/to')
            time.sleep(0.5)
            self.click_id('com.android.email:id/send')
            time.sleep(2)
            return not self.wait_for_ui_exists(1000, resourceId='com.android.email:id/to')
        except Exception, e:
            print Exception, ':', e
            return False

    def email_goto_main(self):
        status = self.email_ui_status()
        print 'status:', status
        if status == 6:
            self.press_key('back')
        if  self.email_ui_status() != 255:
            print 'sss:', self.email_ui_status()
            self.open_email_app()
        return self.email_ui_status() == 255

    def delete_all_sent_mails(self):
        try:
            if self.email_navigation('Sent'):
                if self.wait_for_ui_exists(300, resourceIdMatches='.*empty_view'):
                    return True
                #try to delete all messages in sent mail
                tryTimes = 1
                while self.d(className='android.widget.ListView').child(className='android.widget.FrameLayout').exists and tryTimes < 100:
                    self.d(className='android.widget.ListView').child(className='android.widget.FrameLayout').long_click()
                    if self.wait_for_ui_exists(500, resourceIdMatches='.*delete'):
                         self.click_ui(resourceIdMatches='.*delete')
                    else:
                        return False
                    tryTimes = tryTimes+1

                return self.wait_for_ui_exists(500, resourceIdMatches='.*empty_view')
            else:
                return False
        except Exception, e:
             print Exception, ':', e
             return False

    def check_sentbox_not_empty(self):
        """
        true is not empty
        false is empty
        """
        return not self.wait_for_ui_exists(500, resourceIdMatches='.*empty_view')

    def setup_email_account(self, username='cloudminds001@sina.com', password='q111111'):
        if self.open_email_app():
            self.logmsg("already exits")
            return True
        else:
            self.type_text(username, resourceIdMatches='.*account_email')
            self.click_ui(resourceIdMatches='.*manual_setup')
            self.click_text('Personal (POP3)')
            self.type_text(password, resourceIdMatches='.*regular_password')
            self.click_ui(resourceIdMatches='.*next')
            self.type_text('pop.sina.com', resourceIdMatches='.*account_server')
            self.scroll_to_find(text='STARTTLS')
            self.click_text('STARTTLS')
            self.click_text('None')
            self.click_ui(resourceIdMatches='.*next')
            time.sleep(5)
            self.type_text('smtp.sina.com', resourceIdMatches='.*account_server')
            self.scroll_to_find(text='STARTTLS')
            self.click_text('STARTTLS')
            self.click_text('None')
            self.click_ui(resourceIdMatches='.*next')
            if self.wait_for_ui_exists(5000, text="Account options"):
                self.click_ui(resourceIdMatches='.*next')
                self.wait_and_click(3000, resourceIdMatches='.*account_name')
                self.type_text('cloudminds',resourceIdMatches='.*account_name')
                self.click_ui(resourceIdMatches='.*next')
                time.sleep(3)
            else:
                return False

            return self.wait_for_ui_exists(3000, resourceIdMatches='.*conversation_list_view')

    def prepare_log_tool(self, operation=None):
        self.open_application('com.android.logtool/.LogTool')
        if not self.wait_for_ui_exists(2000, packageName='com.android.logtool'):
            return False

        if not self.d(resourceIdMatches='.*check_main').checked:
            self.click_ui(resourceIdMatches='.*check_main')
        if not self.d(resourceIdMatches='.*check_radio').checked:
            self.click_ui(resourceIdMatches='.*check_radio')
        if not self.d(resourceIdMatches='.*check_events').checked:
            self.click_ui(resourceIdMatches='.*check_events')
        if not self.d(resourceIdMatches='.*check_system').checked:
            self.click_ui(resourceIdMatches='.*check_system')
        if not self.d(resourceIdMatches='.*check_crash').checked:
            self.click_ui(resourceIdMatches='.*check_crash')
        if not self.d(resourceIdMatches='.*check_kernel').checked:
            self.click_ui(resourceIdMatches='.*check_kernel')

        if operation == 'clean':
            self.click_id('com.android.logtool:id/bt_clean')
        elif operation == 'save':
            self.click_id('com.android.logtool:id/bt_pack')
            time.sleep(10)

    def open_wifi(self, mode):
        """
        on -- open wifi on
        off -- turn wifi off
        """
        self.open_application("com.android.settings/.Settings")
        self.scroll_to_find(text='WLAN')
        self.click_text("WLAN")
        if mode == 'on':
            if self.d(resourceIdMatches='.*switch_widget').checked:
                return True
            self.click_ui(resourceIdMatches='.*switch_widget')
            return self.d(resourceIdMatches='.*switch_widget', checked=True).wait.exists(timeout=3000)
        elif mode == 'off':
            if not self.d(resourceIdMatches='.*switch_widget').checked:
                return True
            self.click_ui(resourceIdMatches='.*switch_widget')
            return self.d(resourceIdMatches='.*switch_widget', checked=False).wait.exists(timeout=3000)
        else:
            print "please confirm you set parameter on or off"
            return False


    def restore_phone(self ):
        try:
            self.open_application('com.android.backup/.MainBackUpActivity')
            self.click_text('Restore')
            self.click_text('System data')
            self.click_ui(textMatches='\d+.*')
            self.click_ui(resourceIdMatches='.*recovery_btn')
            time.sleep(3)
            return True
        except Exception, e:
            print Exception, ':', e
            return False

if __name__ == "__main__":
    import sys
    #p = UiKpiTest('ec8fc2f1')
    p = UiKpiTest('ec8fc231')
    p.restore_phone()
    #print p.open_download_file('')
    #p.open_browser_app()
    #p.open_page('http://192.168.99.188/download.php?file=text.txt')
    #print p.download_save_file(3000)
    #print p.open_camera_app()
    #~ print p.dial_number('10086')
    #~ print p.background_call()
    #~ time.sleep(5)
    #~ print p.end_call()
    #~ print p.open_wifi('on')
    #~ print p.open_wifi('off')
    #~ print p.open_wifi('on')
    #~ print p.open_wifi('off')
    #~ print p.open_wifi('on')
    #~ print p.open_wifi('off')
    #~ print p.open_wifi('on')
    #~ print p.open_wifi('off')
    #~ print p.open_wifi('on')


    #~ print p.delete_all_alarms()
    #~ print p.add_default_alarm()
    #~ print p.delete_all_alarms()

    #p.prepare_log_tool('save')
    #print p.setup_email_account()
    #~ print p.open_email_app()
    #~ print p.email_navigation('Inbox')
    #~ print p.open_email_subject('This is a mail')
    #~ print p.forward_email('alex.qi@cloudminds.com')
    #~ time.sleep(3)
    #~ print p.email_navigation('Sent')
    #~ print p.delete_all_sent_mails()
    #p.open_callendar_app()
    #p.create_callendar_events('This is a callendar events')
    #p.check_callendar_events('This is a callendar events')
    #p.delete_callendar_events()
    #~ print p.open_file_manager()
    #~ print p.filemanager_create_folder('010')
    #~ print p.filemanager_check_file_exists('010')
    #~ print p.filemanager_delete_file('010')
    #~ print p.filemanager_check_file_exists('010')
    #p.crash_watchers()
    #print p.open_app_from_Home('Calendar', 'com.android.calendar')
    #p.open_application_from_Home('WPS Office', packageName='com.android.calendar')
    #p.test()
    #~ print p.open_camera_app()
    #~ p.capture_picture_video('still')
    #~ print p.open_file_from_camera('True')
    #~ p.goto_home()
    #~ print p.open_camera_app()
    #~ p.capture_picture_video('video')
    #~ print p.open_file_from_camera('True')
    #~ #print p.open_camera_mode('still')
    #~ #print p.open_camera_mode('video')
    #~ sys.exit()
    #~ print p.pause_music_playing()
    #~ print p.open_music_app()
    #~ print p.open_ongoing_music()
    #~ print p.play_next_music('5')


    #print p.play_music_shuffle_all()
    #print p.check_record_ui_status()
    #~ p.open_recorder_app()
    #~ print p.delete_record_files()
    #~ print p.record_voice(5)
    #~ print p.play_recorded_voice()
    #p.dial_number('10086')
    #p.wait_end_call()
    #p.add_new_contact("ABCD AAAA", "10086")
    #p.delete_contact("ABCD AAAA")
    #~ print p.open_message_app()
    #~ print p.open_message("This is MMS")
    #~ print p.forward_message('13910573271', 'This is MMS', 'True')
    #~ p.delete_msg_by_phoneNum("3271")
    #~ print p.open_browser_app()
    #~ print p.clear_browser_privacy()
    #~ print p.open_page()
    #~ print p.close_browser_app()
    #print p.click_ui(textContains='139')
    #print p.verify_open('Browser', packageName='com.android.swe.browser')
    #print p.delete_file_in_downloads('weight.jpg')
    #print p.close_browser_app()
    #p.scroll_backward('horiz')
