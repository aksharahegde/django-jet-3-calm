var $ = require('jquery');
var Cookies = require('js-cookie');

var CommandPalette = function() {};

CommandPalette.prototype = {
    items: [],
    selectedIndex: 0,
    initDom: function() {
        if ($('.command-palette').length) {
            return;
        }

        var html = [
            '<div class="command-palette">',
            '  <div class="command-palette-backdrop"></div>',
            '  <div class="command-palette-dialog">',
            '    <input type="text" class="command-palette-input" placeholder="Search navigation..." autocomplete="off">',
            '    <ul class="command-palette-results"></ul>',
            '    <div class="command-palette-empty" style="display:none;">No results</div>',
            '  </div>',
            '</div>'
        ].join('');

        $('body').append(html);
    },
    open: function() {
        this.initDom();
        this.$palette = $('.command-palette');
        this.$input = this.$palette.find('.command-palette-input');
        this.$results = this.$palette.find('.command-palette-results');
        this.$empty = this.$palette.find('.command-palette-empty');
        this.$palette.addClass('visible');
        this.$input.val('').trigger('focus');
        this.selectedIndex = 0;
        this.search('');
    },
    close: function() {
        if (this.$palette) {
            this.$palette.removeClass('visible');
        }
    },
    search: function(query) {
        var self = this;
        $.get(window.JET_NAVIGATION_LOOKUP_URL, {q: query}, function(response) {
            if (response.error) {
                self.items = [];
            } else {
                self.items = response.items || [];
            }
            self.selectedIndex = 0;
            self.render();
        });
    },
    render: function() {
        var self = this;
        this.$results.empty();

        if (!this.items.length) {
            this.$empty.show();
            return;
        }

        this.$empty.hide();

        $.each(this.items, function(index, item) {
            var $li = $('<li class="command-palette-result"></li>');
            var $link = $('<a href="#"></a>')
                .toggleClass('selected', index === self.selectedIndex)
                .html('<span class="command-palette-result-type">' + item.type + '</span>' + item.label)
                .on('click', function(e) {
                    e.preventDefault();
                    window.location.href = item.url;
                });
            $li.append($link);
            self.$results.append($li);
        });
    },
    moveSelection: function(delta) {
        if (!this.items.length) {
            return;
        }
        this.selectedIndex = (this.selectedIndex + delta + this.items.length) % this.items.length;
        this.render();
    },
    activateSelection: function() {
        if (this.items[this.selectedIndex]) {
            window.location.href = this.items[this.selectedIndex].url;
        }
    },
    bind: function() {
        var self = this;

        $(document).on('keydown', function(e) {
            var key = e.key || String.fromCharCode(e.which);
            if ((e.metaKey || e.ctrlKey) && key.toLowerCase() === 'k') {
                e.preventDefault();
                self.open();
            } else if (self.$palette && self.$palette.hasClass('visible')) {
                if (key === 'Escape') {
                    self.close();
                } else if (key === 'ArrowDown') {
                    e.preventDefault();
                    self.moveSelection(1);
                } else if (key === 'ArrowUp') {
                    e.preventDefault();
                    self.moveSelection(-1);
                } else if (key === 'Enter') {
                    e.preventDefault();
                    self.activateSelection();
                }
            }
        });

        $(document).on('input', '.command-palette-input', function() {
            self.search($(this).val());
        });

        $(document).on('click', '.command-palette-backdrop', function() {
            self.close();
        });
    },
    run: function() {
        if (!window.JET_NAVIGATION_LOOKUP_URL) {
            return;
        }
        this.bind();
    }
};

$(function() {
    new CommandPalette().run();
});

module.exports = CommandPalette;
