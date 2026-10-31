(function initializeConsentMode(windowObject) {
  const storageKey = 'orbedek_cookie_consent';
  let savedChoice = null;

  try {
    savedChoice = windowObject.localStorage.getItem(storageKey);
  } catch (error) {
    savedChoice = null;
  }

  windowObject.dataLayer = windowObject.dataLayer || [];
  windowObject.gtag = windowObject.gtag || function gtag() {
    windowObject.dataLayer.push(arguments);
  };

  const granted = savedChoice === 'granted';
  windowObject.gtag('consent', 'default', {
    analytics_storage: granted ? 'granted' : 'denied',
    ad_storage: granted ? 'granted' : 'denied',
    ad_user_data: granted ? 'granted' : 'denied',
    ad_personalization: granted ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: savedChoice ? 0 : 500
  });

  windowObject.__orbedekConsent = {
    choice: savedChoice,
    storageKey
  };
})(window);
