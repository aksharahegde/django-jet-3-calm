var $ = require('jquery');

var SavedFilters = function() {};

SavedFilters.prototype = {
    getMeta: function() {
        var $changelist = $('#changelist');
        if (!$changelist.length) {
            return null;
        }

        var match = window.location.pathname.match(/\/admin\/([^/]+)\/([^/]+)\/$/);
        if (!match) {
            return null;
        }

        return {
            app_label: match[1],
            model_name: match[2],
            query_string: window.location.search.replace(/^\?/, '')
        };
    },
    render: function(meta) {
        if ($('.saved-filter-views').length) {
            return;
        }

        var $toolbar = $('#toolbar');
        if (!$toolbar.length) {
            return;
        }

        var $container = $('<div class="saved-filter-views"></div>');
        var $label = $('<span class="saved-filter-views-label">Saved views</span>');
        var $select = $('<select class="saved-filter-views-select"><option value="">--</option></select>');
        var $save = $('<a href="#" class="button saved-filter-views-save">Save current</a>');
        var $delete = $('<a href="#" class="button saved-filter-views-delete">Delete</a>');

        $container.append($label, $select, $save, $delete);
        $toolbar.append($container);

        this.$select = $select;
        this.meta = meta;
        this.load();
        this.bind();
    },
    load: function() {
        var self = this;
        $.get(window.JET_LIST_SAVED_FILTER_VIEWS_URL, {
            app_label: this.meta.app_label,
            model_name: this.meta.model_name
        }, function(response) {
            self.$select.find('option:not(:first)').remove();
            if (!response.error) {
                $.each(response.items || [], function(_, item) {
                    self.$select.append(
                        $('<option></option>')
                            .val(item.id)
                            .attr('data-query-string', item.query_string)
                            .text(item.name)
                    );
                });
            }
        });
    },
    bind: function() {
        var self = this;

        this.$select.on('change', function() {
            var query = $(this).find(':selected').attr('data-query-string');
            if (query) {
                window.location.search = '?' + query;
            }
        });

        $('.saved-filter-views-save').on('click', function(e) {
            e.preventDefault();
            var name = window.prompt('Name this filter view');
            if (!name) {
                return;
            }

            $.post(window.JET_SAVE_FILTER_VIEW_URL, {
                app_label: self.meta.app_label,
                model_name: self.meta.model_name,
                name: name,
                query_string: self.meta.query_string,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').first().val()
            }, function(response) {
                if (!response.error) {
                    self.load();
                }
            });
        });

        $('.saved-filter-views-delete').on('click', function(e) {
            e.preventDefault();
            var id = self.$select.val();
            if (!id) {
                return;
            }

            $.post(window.JET_DELETE_SAVED_FILTER_VIEW_URL, {
                id: id,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').first().val()
            }, function(response) {
                if (!response.error) {
                    self.load();
                }
            });
        });
    },
    run: function() {
        if (!window.JET_LIST_SAVED_FILTER_VIEWS_URL) {
            return;
        }

        var meta = this.getMeta();
        if (meta) {
            this.render(meta);
        }
    }
};

$(function() {
    new SavedFilters().run();
});

module.exports = SavedFilters;
