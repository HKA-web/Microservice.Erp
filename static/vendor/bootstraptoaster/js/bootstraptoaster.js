const TOAST_CONTAINER = document.createElement('div');
TOAST_CONTAINER.id = 'toastContainer';
TOAST_CONTAINER.className = 'position-fixed top-0 right-0';
TOAST_CONTAINER.setAttribute('aria-live', 'polite');
document.body.appendChild(TOAST_CONTAINER);
const TOAST_TEMPLATE = document.createElement('div');
TOAST_TEMPLATE.className = 'toast';
TOAST_TEMPLATE.setAttribute('role', 'status');
TOAST_TEMPLATE.setAttribute('aria-live', 'polite');
TOAST_TEMPLATE.setAttribute('aria-atomic', 'true');
TOAST_TEMPLATE.setAttribute('data-autohide', 'false');
TOAST_TEMPLATE.innerHTML = `
        <div class='toast-header'>
            <span class='status-icon bi mr-2' aria-hidden='true'></span>
            <strong class='mr-auto toast-title'></strong>
            <small class='timer' aria-hidden='true'></small>
            <button type='button' class='ml-2 mb-1 close' data-dismiss='toast' aria-label='Close'>
                <span aria-hidden='true'>&times;</span>
            </button>
        </div>
        <div class='toast-body'></div>`;
var TOAST_STATUS;
(function(TOAST_STATUS) {
  TOAST_STATUS[TOAST_STATUS['SUCCESS'] = 1] = 'SUCCESS';
  TOAST_STATUS[TOAST_STATUS['DANGER'] = 2] = 'DANGER';
  TOAST_STATUS[TOAST_STATUS['WARNING'] = 3] = 'WARNING';
  TOAST_STATUS[TOAST_STATUS['INFO'] = 4] = 'INFO';
})(TOAST_STATUS || (TOAST_STATUS = {}));
var TOAST_PLACEMENT;
(function(TOAST_PLACEMENT) {
  TOAST_PLACEMENT[TOAST_PLACEMENT['TOP_LEFT'] = 1] = 'TOP_LEFT';
  TOAST_PLACEMENT[TOAST_PLACEMENT['TOP_CENTER'] = 2] = 'TOP_CENTER';
  TOAST_PLACEMENT[TOAST_PLACEMENT['TOP_RIGHT'] = 3] = 'TOP_RIGHT';
  TOAST_PLACEMENT[TOAST_PLACEMENT['MIDDLE_LEFT'] = 4] = 'MIDDLE_LEFT';
  TOAST_PLACEMENT[TOAST_PLACEMENT['MIDDLE_CENTER'] = 5] = 'MIDDLE_CENTER';
  TOAST_PLACEMENT[TOAST_PLACEMENT['MIDDLE_RIGHT'] = 6] = 'MIDDLE_RIGHT';
  TOAST_PLACEMENT[TOAST_PLACEMENT['BOTTOM_LEFT'] = 7] = 'BOTTOM_LEFT';
  TOAST_PLACEMENT[TOAST_PLACEMENT['BOTTOM_CENTER'] = 8] = 'BOTTOM_CENTER';
  TOAST_PLACEMENT[TOAST_PLACEMENT['BOTTOM_RIGHT'] = 9] = 'BOTTOM_RIGHT';
})(TOAST_PLACEMENT || (TOAST_PLACEMENT = {}));
var TOAST_THEME;
(function(TOAST_THEME) {
  TOAST_THEME[TOAST_THEME['LIGHT'] = 1] = 'LIGHT';
  TOAST_THEME[TOAST_THEME['DARK'] = 2] = 'DARK';
})(TOAST_THEME || (TOAST_THEME = {}));
var TOAST_TIMERS;
(function(TOAST_TIMERS) {
  TOAST_TIMERS[TOAST_TIMERS['DISABLED'] = 0] = 'DISABLED';
  TOAST_TIMERS[TOAST_TIMERS['ELAPSED'] = 1] = 'ELAPSED';
  TOAST_TIMERS[TOAST_TIMERS['COUNTDOWN'] = 2] = 'COUNTDOWN';
})(TOAST_TIMERS || (TOAST_TIMERS = {}));

class Toast {
  static configure(options) {
    this.setMaxCount(options === null || options === void 0 ? void 0 : options.maxToasts);
    this.setPlacement(options === null || options === void 0 ? void 0 : options.placement);
    this.setTheme(options === null || options === void 0 ? void 0 : options.theme);
    this.enableTimers(options === null || options === void 0 ? void 0 : options.enableTimers);
    this.enableQueue(options === null || options === void 0 ? void 0 : options.enableQueue);
  }

  static setMaxCount(maxToasts) {
    if (maxToasts !== null) {
      if (maxToasts > 0) {
        this.maxToastCount = maxToasts;
      } else {
        console.error('The maximum number of toasts must be greater than 0. Reverting to default.');
      }
    }
  }

  static setPlacement(placement) {
    TOAST_CONTAINER.className = 'toast-container position-fixed';
    switch (placement) {
      case TOAST_PLACEMENT.TOP_LEFT:
        TOAST_CONTAINER.classList.add('top-0', 'left-0');
        break;
      case TOAST_PLACEMENT.TOP_CENTER:
        TOAST_CONTAINER.classList.add('top-0', 'left-50', 'translate-middle-x');
        break;
      case TOAST_PLACEMENT.TOP_RIGHT:
        TOAST_CONTAINER.classList.add('top-0', 'right-0');
        break;
      case TOAST_PLACEMENT.MIDDLE_LEFT:
        TOAST_CONTAINER.classList.add('top-50', 'left-0', 'translate-middle-y');
        break;
      case TOAST_PLACEMENT.MIDDLE_CENTER:
        TOAST_CONTAINER.classList.add('top-50', 'left-50', 'translate-middle');
        break;
      case TOAST_PLACEMENT.MIDDLE_RIGHT:
        TOAST_CONTAINER.classList.add('top-50', 'right-0', 'translate-middle-y');
        break;
      case TOAST_PLACEMENT.BOTTOM_LEFT:
        TOAST_CONTAINER.classList.add('bottom-0', 'left-0');
        break;
      case TOAST_PLACEMENT.BOTTOM_CENTER:
        TOAST_CONTAINER.classList.add('bottom-0', 'left-50', 'translate-middle-x');
        break;
      case TOAST_PLACEMENT.BOTTOM_RIGHT:
        TOAST_CONTAINER.classList.add('bottom-0', 'right-0');
        break;
      default:
        TOAST_CONTAINER.classList.add('top-0', 'right-0');
        break;
    }
  }

  static setTheme(theme = null) {
    let header = TOAST_TEMPLATE.querySelector('.toast-header');
    let close = header.querySelector('.close');
    switch (theme) {
      case TOAST_THEME.LIGHT:
        TOAST_TEMPLATE.style.backgroundColor = 'var(--body-bg-color-light)';
        TOAST_TEMPLATE.style.color = 'var(--text-color-light)';
        header.style.color = 'var(--header-color-light)';
        close.style.color = 'var(--text-color-light)';
        break;
      case TOAST_THEME.DARK:
        TOAST_TEMPLATE.style.backgroundColor = 'var(--body-bg-color-dark)';
        TOAST_TEMPLATE.style.color = 'var(--text-color-dark)';
        header.style.color = 'var(--header-color-dark)';
        close.style.color = 'var(--text-color-dark)';
        break;
      default:
        TOAST_TEMPLATE.removeAttribute('style');
        header.removeAttribute('style');
        close.removeAttribute('style');
        break;
    }
  }

  static enableTimers(type) {
    this.timersEnabled = type;
  }

  static enableQueue(enabled = true) {
    this.queueEnabled = enabled;
    if (!enabled)
      this.queue = [];
  }

  static create(toastOptions) {
    let toastEl = TOAST_TEMPLATE.cloneNode(true);
    let toastTitle = toastEl.querySelector('.toast-title');
    toastTitle.innerText = toastOptions.title;
    let toastBody = toastEl.querySelector('.toast-body');
    toastBody.innerHTML = toastOptions.message;
    this.setStatus(toastEl, toastOptions.status);
    if (this.currentToastCount >= this.maxToastCount) {
      if (!this.queueEnabled)
        return;
      const toastToQueue = {
        toast: toastEl,
        timeout: toastOptions.timeout,
        pauseDelayOnHover: toastOptions.pauseDelayOnHover,
        onHidden: toastOptions.onHidden,
      };
      this.queue.push(toastToQueue);
      return;
    }
    const toastInfo = {
      toast: toastEl,
      timeout: toastOptions.timeout,
      pauseDelayOnHover: toastOptions.pauseDelayOnHover,
      onHidden: toastOptions.onHidden,
    };
    this.render(toastInfo);
  }

  static setStatus(toastEl, status) {
    let header = toastEl.querySelector('.toast-header');
    let statusIcon = toastEl.querySelector('.status-icon');
    switch (status) {
      case TOAST_STATUS.SUCCESS:
        header.style.backgroundImage = 'var(--header-bg-color-success-light)';
        statusIcon.classList.add('text-success', 'bi-check-circle-fill');
        break;
      case TOAST_STATUS.DANGER:
        header.style.backgroundImage = 'var(--header-bg-color-danger-light)';
        statusIcon.classList.add('text-danger', 'bi-x-circle-fill');
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        break;
      case TOAST_STATUS.WARNING:
        header.style.backgroundImage = 'var(--header-bg-color-warning-light)';
        statusIcon.classList.add('text-warning', 'bi-exclamation-circle-fill');
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        break;
      case TOAST_STATUS.INFO:
        header.style.backgroundImage = 'var(--header-bg-color-info-light)';
        statusIcon.classList.add('text-info', 'bi-info-circle-fill');
        break;
      default:
        statusIcon.classList.add('d-none');
        break;
    }
  }

  static render(toastInfo) {
    let paused = false;
    if (toastInfo.timeout > 0) {
      toastInfo.toast.setAttribute('data-delay', toastInfo.timeout.toString());
      toastInfo.toast.setAttribute('data-autohide', 'true');
      if (toastInfo.pauseDelayOnHover) {
        toastInfo.toast.removeAttribute('data-delay');
        toastInfo.toast.setAttribute('data-autohide', 'false');
        var delay = Math.floor(Date.now() / 1000) + (toastInfo.timeout / 1000);
        toastInfo.toast.setAttribute('data-hide-after', delay.toString());
      }
    }
    if (toastInfo.pauseDelayOnHover) {
      setTimeout(function() {
        if (!paused) {
          $(toastInfo.toast).toast('hide');
        }
      }, toastInfo.timeout);
      $(toastInfo.toast).on('mouseover', function() {
        paused = true;
      });
      $(toastInfo.toast).on('mouseleave', function() {
        const current = Math.floor(Date.now() / 1000),
          future = parseInt($(this).data('hideAfter'));
        paused = false;
        if (current >= future) {
          $(toastInfo.toast).toast('hide');
        }
      });
    }
    this.renderTimer(toastInfo);
    TOAST_CONTAINER.appendChild(toastInfo.toast);
    $(toastInfo.toast).toast('show');
    this.currentToastCount++;
    $(toastInfo.toast).on('hidden.bs.toast', () => {
      if (toastInfo.onHidden) {
        toastInfo.onHidden(toastInfo.toast);
      }
      TOAST_CONTAINER.removeChild(toastInfo.toast);
      this.currentToastCount--;
      if (this.queueEnabled && this.queue.length > 0 && this.currentToastCount < this.maxToastCount) {
        const queuedToast = this.queue.shift();
        this.render(queuedToast);
      }
    });
  }

  static renderTimer(toastInfo) {
    let timer = toastInfo.toast.querySelector('.timer');
    switch (this.timersEnabled) {
      case TOAST_TIMERS.ELAPSED: {
        timer.innerText = 'just now';
        let minutes = 1;
        let elapsedTimer = setInterval(() => {
          timer.innerText = `${minutes}m ago`;
          minutes++;
        }, 60 * 1000);
        $(toastInfo.toast).on('hidden.bs.toast', () => {
          clearInterval(elapsedTimer);
        });
        break;
      }
      case TOAST_TIMERS.COUNTDOWN: {
        if (toastInfo.timeout > 0) {
          let seconds = toastInfo.timeout / 1000;
          timer.innerText = `${seconds}s`;
          let countdownTimer = setInterval(() => {
            timer.innerText = `${seconds - 1 < 0 ? Math.abs(seconds) : seconds - 1}s`;
            seconds--;
          }, 1000);
          $(toastInfo.toast).on('hidden.bs.toast', () => {
            clearInterval(countdownTimer);
          });
          break;
        }
      }
      default: {
        let toastHeader = toastInfo.toast.querySelector('.toast-header');
        toastHeader.removeChild(timer);
        break;
      }
    }
  }

  static oldConfigure(maxToasts = null, placement = TOAST_PLACEMENT.TOP_RIGHT, theme = null, enableTimers = true) {
    const configuration = {
      maxToasts: maxToasts,
      placement: placement,
      theme: theme,
      enableTimers: enableTimers ? TOAST_TIMERS.ELAPSED : TOAST_TIMERS.DISABLED,
    };
    this.configure(configuration);
  }

  static oldCreate(title, message, status = 0, timeout = 0) {
    const toast = {
      title: title,
      message: message,
      status: status,
      timeout: timeout,
    };
    this.create(toast);
  }

  static oldEnableTimers(enabled) {
    this.timersEnabled = enabled ? TOAST_TIMERS.ELAPSED : TOAST_TIMERS.DISABLED;
  }
}

Toast.maxToastCount = 6;
Toast.currentToastCount = 0;
Toast.timersEnabled = TOAST_TIMERS.ELAPSED;
Toast.queueEnabled = true;
Toast.queue = [];
