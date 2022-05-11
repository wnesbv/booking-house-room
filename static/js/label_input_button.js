const burst = function (info) {
    const obj = {
        bursts: [],
        html: {
            elements: document.querySelectorAll(info.selector),
            clicked: undefined,
        },
        init() {
            this.listen();
        },
        listen() {
            const that = this;
            for (let i = 0; i < this.html.elements.length; i++) {
                const ele = this.html.elements[i];
                ele.style.overflow = 'hidden';
                const pos = ele.style.position;
                if (pos !== 'relative' || pos !== 'absolute') { ele.style.position = 'relative' }

                ele.addEventListener('mousedown', function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    that.createBurst(this, event.offsetX, event.offsetY);
                })
                ele.addEventListener('touchstart', function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    that.createBurst(this, event.clientX, event.clientY);
                })
                ele.addEventListener('mouseup', () => { that.cancelBurst() })
                ele.addEventListener('mouseout', () => { that.cancelBurst() })
                ele.addEventListener('touchend', () => { that.cancelBurst() })
            }
        },
        cancelBurst() {
            this.held = false;
            this.update();
        },
        createBurst(ele, x, y) {
            this.held = true;
            const span = document.createElement('span')
            span.classList.add('burst')
            span.style.left = `${x}px`
            span.style.top = `${y}px`
            ele.appendChild(span);
            this.bursts.push({
                html: span,
                grow: false,
                removed: false,
                time: Date.now(),
            })
            const that = this;
            setTimeout(() => { that.update() }, 0);
            setTimeout(() => { that.update() }, 400);
        },
        update() {
            const that = this;
            this.bursts.forEach((burst) => {
                if (!burst.grow) { that.grow(burst) }

                if (Date.now() - burst.time > 400 && !burst.removed && !that.held) {
                    burst.html.classList.add('fade');
                }
            })
        },
        grow(burst) {
            // Get the hypotnuse
            const a = burst.html.parentElement.offsetWidth;
            const b = burst.html.parentElement.offsetHeight;
            const c = Math.sqrt(a * a + b * b) * 2;
            burst.html.style.width = `${c}px`;
            burst.html.style.height = `${c}px`;
            burst.html.classList.add('grow')
            burst.grow = true;
        },
    };
    obj.init();
    return obj;
}

burst({ selector: '.m_btn' });
