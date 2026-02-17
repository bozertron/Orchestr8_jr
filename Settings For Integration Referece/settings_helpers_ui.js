/**
 * Settings Helper Functions - UI Configuration
 * Pattern Bible: Extracted from settings_helpers.js for hyper-modular architecture
 * Purpose: Build UI configuration objects for settings.js
 */

function buildNotificationsConfig() {
  return {
    enabled: getToggle('notifications-enabled'),
    sound_enabled: getToggle('notification-sound'),
    show_previews: getToggle('show-previews'),
    do_not_disturb_start: null,
    do_not_disturb_end: null
  };
}

function buildUIConfig() {
  return {
    theme: {
      mode: getValue('theme-mode'),
      accent_color: getValue('accent-color'),
      font_size: getSlider('font-size')
    },
    language: {
      locale: getValue('language'),
      date_format: 'YYYY-MM-DD',
      time_format: getValue('time-format')
    },
    notifications: buildNotificationsConfig(),
    layout: {
      sidebar_width: getNumber('sidebar-width'),
      message_density: getValue('message-density'),
      show_timestamps: getToggle('show-timestamps'),
      show_avatars: getToggle('show-avatars')
    },
    behavior: {
      auto_scroll_on_new_message: getToggle('auto-scroll'),
      focus_input_on_send: getToggle('focus-input-on-send')
    }
  };
}

