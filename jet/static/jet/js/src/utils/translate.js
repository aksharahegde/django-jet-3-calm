module.exports = function(str) {
    const gettext = django.gettext || window.gettext;
    if (gettext == undefined) {
        return str;
    }
    return gettext(str);
};
