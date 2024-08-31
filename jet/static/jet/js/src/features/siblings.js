var $ = require('jquery');

var Siblings = function($siblings) {
    this.$siblings = $siblings;
};

Siblings.prototype = {
    moveSiblings: function($siblings) {
        $siblings.detach().insertBefore($('.object-tools'));
    },
    run: function() {
        try {
            this.moveSiblings(this.$siblings);
        } catch (e) {
            console.error(e, e.stack);
        }

        this.$siblings.addClass('initialized');
    }
};

$(function() {
    $('.changeform-navigation').each(function() {
        new Siblings($(this)).run();
    });
});
