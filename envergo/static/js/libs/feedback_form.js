/**
 * The feedback forms is displayed in a dialog that is toggled by a button.
 *
 * I tried to reuse the dsfr's internal api to handle the toggling mechanism.
 * Modals and Tabs both inherit from the `Disclosure` internal class, so
 * I tried to reuse that.
 *
 * The API is not really documented, though, so I did my best.
 */
const api = window['dsfr'];

// Use Matomo API for analytics
var _paq = window._paq || [];

const DialogSelector = {
  DIALOG: api.internals.ns.selector('dialog'),
  BODY: api.internals.ns.selector('dialog__body')
};

class DialogButton extends api.core.DisclosureButton {
  constructor() {
    super(api.core.DisclosureType.OPENED);
  }

  static get instanceClassName() {
    return 'DialogButton';
  }
}

class Dialog extends api.core.Disclosure {
  constructor() {
    super(api.core.DisclosureType.OPENED, DialogSelector.DIALOG, DialogButton, 'DialogsGroup');
  }

  static get instanceClassName() {
    return 'Dialog';
  }

  init() {
    super.init();
    this.listenKey(api.core.KeyCodes.ESCAPE, this.conceal.bind(this, false, false), true, true);
  }

  disclose(withhold) {
    if (!super.disclose(withhold)) return false;
    this.setAttribute('aria-dialog', 'true');
    this.setAttribute('open', 'true');

    _paq.push(['trackEvent', 'feedback', 'disclose']);
    return true;
  }

  conceal(withhold, preventFocus) {
    if (!super.conceal(withhold, preventFocus)) return false;
    this.removeAttribute('aria-dialog');
    this.removeAttribute('open');

    _paq.push(['trackEvent', 'feedback', 'conceal']);
    return true;
  }
}

api.dialog = {
  Dialog: Dialog,
  DialogButton: DialogButton,
  DialogSelector: DialogSelector
};

api.internals.register(api.dialog.DialogSelector.DIALOG, api.dialog.Dialog);