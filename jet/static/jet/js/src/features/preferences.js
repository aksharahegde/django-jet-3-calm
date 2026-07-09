var $ = require('jquery');
var Cookies = require('js-cookie');

var Preferences = function() {};

Preferences.prototype = {
    initDom: function() {
        if ($('.preferences-panel').length) {
            return;
        }

        var themeOptions = (window.JET_THEMES || []).map(function(theme) {
            return '<option value="' + theme.theme + '">' + theme.title + '</option>';
        }).join('');

        var html = [
            '<div class="preferences-panel">',
            '  <div class="preferences-panel-backdrop"></div>',
            '  <div class="preferences-panel-dialog">',
            '    <h2 class="preferences-panel-title">Preferences</h2>',
            '    <form class="preferences-panel-form">',
            '      <div class="preferences-panel-field">',
            '        <label for="jet-preferences-theme">Theme</label>',
            '        <select id="jet-preferences-theme" name="theme"><option value="">Default</option>' + themeOptions + '</select>',
            '      </div>',
            '      <div class="preferences-panel-field">',
            '        <label><input type="checkbox" name="side_menu_compact" value="true"> Compact side menu</label>',
            '      </div>',
            '      <div class="preferences-panel-field">',
            '        <label><input type="checkbox" name="sidebar_pinned" value="true"> Pin sidebar</label>',
            '      </div>',
            '      <div class="preferences-panel-actions">',
            '        <button type="submit" class="button">Save</button>',
            '      </div>',
            '    </form>',
            '  </div>',
            '</div>'
        ].join('');

        $('body').append(html);
    },
    open: function() {
        var self = this;
        this.initDom();
        this.$panel = $('.preferences-panel');
        this.$panel.addClass('visible');

        $.get(window.JET_GET_PREFERENCES_URL, function(response) {
            if (response.error) {
                return;
            }
            $('#jet-preferences-theme').val(response.theme || '');
            $('input[name="side_menu_compact"]').prop('checked', !!response.side_menu_compact);
            $('input[name="sidebar_pinned"]').prop('checked', !!response.sidebar_pinned);
        });
    },
    close: function() {
        if (this.$panel) {
            this.$panel.removeClass('visible');
        }
    },
    save: function(data) {
        var self = this;
        $.post(window.JET_SAVE_PREFERENCES_URL, data, function(response) {
            if (response.error) {
                return;
            }

            if (response.theme) {
                Cookies.set('JET_THEME', response.theme, {expires: 365, path: '/'});
            } else {
                Cookies.remove('JET_THEME', {path: '/'});
            }

            if (response.sidebar_pinned !== null && response.sidebar_pinned !== undefined) {
                Cookies.set('sidebar_pinned', response.sidebar_pinned, {expires: 365, path: '/'});
            }

            self.close();
            window.location.reload();
        });
    },
    bind: function() {
        var self = this;

        $(document).on('click', '.jet-open-preferences', function(e) {
            e.preventDefault();
            self.open();
        });

        $(document).on('click', '.preferences-panel-backdrop', function() {
            self.close();
        });

        $(document).on('submit', '.preferences-panel-form', function(e) {
            e.preventDefault();
            self.save({
                theme: $('#jet-preferences-theme').val(),
                side_menu_compact: $('input[name="side_menu_compact"]').is(':checked') ? 'true' : 'false',
                sidebar_pinned: $('input[name="sidebar_pinned"]').is(':checked') ? 'true' : 'false',
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').first().val()
            });
        });
    },
    run: function() {
        if (!window.JET_GET_PREFERENCES_URL) {
            return;
        }
        this.bind();
    }
};

$(function() {
    new Preferences().run();
});

module.exports = Preferences;
