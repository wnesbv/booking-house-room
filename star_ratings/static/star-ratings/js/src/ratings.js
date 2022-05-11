const rest = require('./rest.js');
const utils = require('./utils');

/** *******************
 * Initialise ratings
 ******************** */
function init() {
    const ratingActions = document.querySelectorAll('.star-ratings-rate-action');
        let i;

    // Add click events to stars
    for (i = 0; i < ratingActions.length; i += 1) {
        bindRatings(ratingActions[i]);
    }
}

/** *******************
 * Bind ratings
 ******************** */
function bindRatings(el) {
    el.addEventListener('submit', ratingSubmit);

    el.onmouseenter = function () {
        const maxRating = getMaxRating(this);
        const scoreEl = this.querySelector('[name=score]');

        if (scoreEl) {
            const parent = utils.findParent(this, 'star-ratings');
            parent.querySelector('.star-ratings-rating-foreground').style.width = `${100 / maxRating * scoreEl.value}%`;
        }
    };

    el.onmouseleave = function () {
        const avgRating = getAvgRating(this);
        const maxRating = getMaxRating(this);
        const parent = utils.findParent(this, 'star-ratings');
        const percentage = `${100 / maxRating * avgRating}%`;
        parent.querySelector('.star-ratings-rating-foreground').style.width = percentage;
    };
}

/** *******************
 * Rating click event
 ******************** */
function ratingSubmit(ev) {
    ev.stopPropagation();
    ev.preventDefault();

    const form = ev.target;

    const data = [].reduce.call(form.elements, (data, element) => {
        data[element.name] = element.value;
        return data;
    }, {});

    rate(form.action, data, this);
}

/** *******************
 * Rate instance
 ******************** */
function rate(url, data, sender) {
    rest.post(url, data, (rating) => {
        updateRating(rating, sender);
        dispatchRateSuccessEvent(rating, sender);
    }, (errors) => {
        showError(errors, sender);
        dispatchRateFailEvent(errors, sender);
    });
}

function _getEvent(name, detail) {
    if (typeof CustomEvent === 'undefined') {
        const evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(name, true, true, detail);
        return evt;
    }

        return new CustomEvent(name, {
            detail,
            bubbles: true,
            cancelable: true,
        });
}

function dispatchRateSuccessEvent(rating, sender) {
    sender.dispatchEvent(_getEvent(
        'rate-success',
        {
            sender,
            rating,
        },
    ))
}

function dispatchRateFailEvent(error, sender) {
    sender.dispatchEvent(_getEvent(
        'rate-failed',
        {
            sender,
            error,
        },
    ))
}

function getMaxRating(el) {
    const parent = utils.findParent(el, 'star-ratings');
    if (parent) {
        return parseInt(parent.getAttribute('data-max-rating'));
    }

    return -1;
}

function getAvgRating(el) {
    const parent = utils.findParent(el, 'star-ratings');
    if (parent) {
        return parseFloat(parent.getAttribute('data-avg-rating'));
    }

    return -1;
}

/** *******************
 * Update rating
 ******************** */
function updateRating(rating, sender) {
    const parent = utils.findParent(sender, 'star-ratings');
        let valueElem;

    if (parent === undefined || parent === null) {
        return;
    }

    parent.setAttribute('data-avg-rating', rating.average);
    const avgElem = parent.getElementsByClassName('star-ratings-rating-average')[0];
    if (avgElem) {
        valueElem = avgElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            let average = rating.average.toFixed(2);

            // suppress . if 0.
            if (rating.average === 0) {
                average = 0
            }

            valueElem.innerHTML = average
        }
    }

    const countElem = parent.getElementsByClassName('star-ratings-rating-count')[0];
    if (countElem) {
        valueElem = countElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            valueElem.innerHTML = rating.count;
        }
    }

    const userElem = parent.getElementsByClassName('star-ratings-rating-user')[0];
    const clearElem = parent.getElementsByClassName('star-ratings-clear')[0];
    if (userElem) {
        valueElem = userElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            if (rating.user_rating == null && valueElem.getAttribute('data-when-null', false)) {
                rating.user_rating = valueElem.getAttribute('data-when-null');

                if (clearElem) {
                    clearElem.classList.remove('star-ratings-clear-visible');
                    clearElem.classList.add('star-ratings-clear-hidden');
                }
            } else if (clearElem) {
                    clearElem.classList.remove('star-ratings-clear-hidden');
                    clearElem.classList.add('star-ratings-clear-visible');
                }
            valueElem.innerHTML = rating.user_rating;
        }
    }

    parent.querySelector('.star-ratings-rating-foreground').style.width = `${rating.percentage}%`;
}

function toggleClass(el, cls) {
    if (el.classList.contains(cls)) {
        el.classList.remove(cls);
    } else {
        el.classList.add(cls);
    }
}

function showError(errors, sender) {
    const parent = utils.findParent(sender, 'star-ratings');
    if (parent === undefined || parent === null) {
        return;
    }
    parent.querySelector('.star-ratings-errors').innerHTML = errors.error;
    setTimeout(() => {
        parent.querySelector('.star-ratings-errors').innerHTML = '';
    }, 2500);
}

/** *******************
 * Only initialise ratings
 * if there is something to rate
 ******************** */
document.addEventListener('DOMContentLoaded', (event) => {
    if (document.querySelector('.star-ratings')) {
        init();
    }
});

module.exports = {
    bindRating: bindRatings,
};
