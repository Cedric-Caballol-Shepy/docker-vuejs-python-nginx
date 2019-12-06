import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueI18n from "vue-i18n";

import english from "./lang/en";
import french from "./lang/fr";

Vue.config.productionTip = false;

Vue.use(VueI18n);

const messages = {
  en: english,
  fr: french
};

// Create VueI18n instance with options
const i18n = new VueI18n({
  locale: "fr", // set locale
  messages // set locale messages
});

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount("#app");
