import Foundation
import objc

class MountainLionNotification(Foundation.NSObject):
    # Based on http://stackoverflow.com/questions/12202983/working-with-mountain-lions-notification-center-using-pyobjc

    def init(self):
        self = objc.super(MountainLionNotification, self).init()
        if self is None: return None

        # Get objc references to the classes we need.
        self.NSUserNotification = objc.lookUpClass('NSUserNotification')
        self.NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

        return self

    def clearNotifications(self):
        """Clear any displayed alerts we have posted. Requires Mavericks."""

        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
        NSUserNotificationCenter.defaultUserNotificationCenter().removeAllDeliveredNotifications()

    def notify(self, title, subtitle, info_text, delay=0, sound=False, userInfo={"action":"open_url", "value":"https://calendar.google.com"}):
        """Create a user notification and display it."""

        notification = self.NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(info_text))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setHasActionButton_(True)
        notification.setActionButtonTitle_("View")
        notification.setUserInfo_(userInfo)

        self.NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
        self.NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

        # Note that the notification center saves a *copy* of our object.
        return notification

    # We'll get this if the user clicked on the notification.
    def userNotificationCenter_didActivateNotification_(self, center, notification):
        """Handler a user clicking on one of our posted notifications."""
        userInfo = notification.userInfo()
        print("Open Google Calendar")
        if userInfo["action"] == "open_url":
            import webbrowser
            webbrowser.open("https://calendar.google.com")
# import Foundation
# import objc
# import AppKit
# import sys
#
# NSUserNotification = objc.lookUpClass('NSUserNotification')
# NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
#
# def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={"action":"open_url", "value":"https://calendar.google.com"}):
# 	notification = NSUserNotification.alloc().init()
# 	notification.setTitle_(title)
# 	notification.setSubtitle_(subtitle)
# 	notification.setInformativeText_(info_text)
# 	notification.setUserInfo_(userInfo)
# 	notification.setHasActionButton_(True)
# 	if sound:
# 		notification.setSoundName_("NSUserNotificationDefaultSoundName")
#
# 	notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
# 	NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
#
# # We'll get this if the user clicked on the notification.
# def userNotificationCenter_didActivateNotification_(self, center, notification):
#     """Handler a user clicking on one of our posted notifications."""
#     userInfo = notification.userInfo()
#     if userInfo["action"] == "open_url":
#         import webbrowser
#             # Open the log file with TextEdit.
#         webbrowser.open("https://calendar.google.com")
#notify("Test message", "Subtitle", "This message should appear instantly, with a sound", sound=True)
#sys.stdout.write("Notification sent...\n")
