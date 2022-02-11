var $ = require('jquery');

var ActionsUpdater = function($changelist) {
    this.$changelist = $changelist;
};

ActionsUpdater.prototype = {
    removeLabel: function($actions) {
        var $input = $actions.find('[name="action"]').first();

        if ($input.length == 0) {
            return;
        }

        var $label = $($input[0].previousSibling);

        if ($label.get(0).nodeType == 3) {
            $label.remove();
        }
    },
    wrapLabels: function($actions) {
        var $wrapper = $('<div>').addClass('labels');
        $actions.find('span.all, span.action-counter, span.clear, span.question')
                .wrapAll($wrapper);
    },
    moveActions: function($actions) {
        var $paginator = this.$changelist.find('.paginator');
        var $wrapper = $('<div>').addClass('changelist-footer');

        $wrapper.insertAfter($paginator);

        $actions.detach();
        $paginator.detach();

        $wrapper
            .append($actions)
            .append($paginator)
            .append($('<div>').addClass('cf'));
    },
    run: function() {
        var $actions = this.$changelist.find('.actions');

        try {
            this.removeLabel($actions);
            this.wrapLabels($actions);
            this.moveActions($actions);
        } catch (e) {
            console.error(e, e.stack);
        }

        $actions.addClass('initialized');
    }
};

/*global gettext, interpolate, ngettext*/
'use strict';
{
    // Call function fn when the DOM is loaded and ready. If it is already
    // loaded, call the function now.
    // http://youmightnotneedjquery.com/#ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function() {
        const actionsEls = document.querySelectorAll('tr input.action-select');
        if (actionsEls.length) {
            $('#changelist').each(function() {
                new ActionsUpdater($(this)).run();
                console.log('ActionsUpdater');
            });
        }
    });
}
