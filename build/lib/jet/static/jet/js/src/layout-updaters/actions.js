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
    function show(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.remove('hidden');
            el.style.display = 'block';
        });
    }

    function hide(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.add('hidden');
            el.style.display = 'none';
        });
    }

    function showQuestion(options) {
        hide(options.acrossClears);
        show(options.acrossQuestions);
        hide(options.allContainer);
    }

    function showClear(options) {
        show(options.acrossClears);
        hide(options.acrossQuestions);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
        show(options.allContainer);
        hide(options.counterContainer);
    }

    function reset(options) {
        hide(options.acrossClears);
        hide(options.acrossQuestions);
        hide(options.allContainer);
        show(options.counterContainer);
    }

    function clearAcross(options) {
        reset(options);
        const acrossInputs = document.querySelectorAll(options.acrossInput);
        acrossInputs.forEach(function(acrossInput) {
            acrossInput.value = 0;
        });
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
    }

    function checker(actionCheckboxes, options, checked) {
        if (checked) {
            showQuestion(options);
        } else {
            reset(options);
        }
        actionCheckboxes.forEach(function(el) {
            el.checked = checked;
            el.closest('tr').classList.toggle(options.selectedClass, checked);
        });
    }

    function updateCounter(actionCheckboxes, options) {
        const sel = Array.from(actionCheckboxes).filter(function(el) {
            return el.checked;
        }).length;
        const counter = document.querySelector(options.counterContainer);
        // data-actions-icnt is defined in the generated HTML
        // and contains the total amount of objects in the queryset
        const actions_icnt = Number(counter.dataset.actionsIcnt);
        counter.textContent = interpolate(
            ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                sel: sel,
                cnt: actions_icnt
            }, true);
        const allToggle = document.getElementById(options.allToggleId);
        allToggle.checked = sel === actionCheckboxes.length;
        if (allToggle.checked) {
            showQuestion(options);
        } else {
            clearAcross(options);
        }
    }

    const defaults = {
        actionContainer: "div.actions",
        counterContainer: "span.action-counter",
        allContainer: "div.actions span.all",
        acrossInput: "div.actions input.select-across",
        acrossQuestions: "div.actions span.question",
        acrossClears: "div.actions span.clear",
        allToggleId: "action-toggle",
        selectedClass: "selected"
    };

     function Actions (actionCheckboxes, options) {
        options = Object.assign({}, defaults, options);
        var listEditableChanged = false;
        var lastChecked = null;
        var shiftPressed = false;

        document.addEventListener('keydown', function (event)  {
            shiftPressed = event.shiftKey;
        });

        document.addEventListener('keyup', function (event) {
            shiftPressed = event.shiftKey;
        });

        document.getElementById(options.allToggleId).addEventListener('click', function(event) {
            checker(actionCheckboxes, options, this.checked);
            updateCounter(actionCheckboxes, options);
        });

        document.querySelectorAll(options.acrossQuestions + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                const acrossInputs = document.querySelectorAll(options.acrossInput);
                acrossInputs.forEach(function(acrossInput) {
                    acrossInput.value = 1;
                });
                showClear(options);
            });
        });

        document.querySelectorAll(options.acrossClears + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                document.getElementById(options.allToggleId).checked = false;
                clearAcross(options);
                checker(actionCheckboxes, options, false);
                updateCounter(actionCheckboxes, options);
            });
        });

        function affectedCheckboxes(target, withModifier) {
            const multiSelect = (lastChecked && withModifier && lastChecked !== target);
            if (!multiSelect) {
                return [target];
            }
            const checkboxes = Array.from(actionCheckboxes);
            const targetIndex = checkboxes.findIndex(function(el) {
                return el === target
            });
            const lastCheckedIndex = checkboxes.findIndex(function(el) {
                return el === lastChecked
            });
            const startIndex = Math.min(targetIndex, lastCheckedIndex);
            const endIndex = Math.max(targetIndex, lastCheckedIndex);
            const filtered = checkboxes.filter(function(el, index) { (startIndex <= index) && (index <= endIndex) });
            return filtered;
        };

        Array.from(document.getElementById('result_list').tBodies).forEach(function(el) {
            el.addEventListener('change', function(event) {
                const target = event.target;
                if (target.classList.contains('action-select')) {
                    const checkboxes = affectedCheckboxes(target, shiftPressed);
                    checker(checkboxes, options, target.checked);
                    updateCounter(actionCheckboxes, options);
                    lastChecked = target;
                } else {
                    listEditableChanged = true;
                }
            });
        });


        const btnIndex = document.querySelector('#changelist-form button[name=index]');
        if (btnIndex) {
            btnIndex.addEventListener('click', function(event) {
                if (listEditableChanged) {
                    const confirmed = confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
                    if (!confirmed) {
                        event.preventDefault();
                    }
                }
            });
        }

        const el = document.querySelector('#changelist-form input[name=_save]');
        // The button does not exist if no fields are editable.
        if (el) {
            el.addEventListener('click', function(event) {
                if (document.querySelector('[name=action]').value) {
                    const text = listEditableChanged
                        ? gettext("You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action.")
                        : gettext("You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button.");
                    if (!confirm(text)) {
                        event.preventDefault();
                    }
                }
            });
        }
    };

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
            Actions(actionsEls);
            $('#changelist').each(function() {
                new ActionsUpdater($(this)).run();
            });
        }
    });
}