import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/challengeChatBot",
    name: "challengeChatBot",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ChallengeChatBot.vue")
  },
  {
    path: "/challengeAI",
    name: "challengeAI",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ChallengeAI.vue")
  },
  {
    path: "/challengeGame",
    name: "challengeGame",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ChallengeGame.vue")
  },
  {
    path: "/challengeSelfie",
    name: "challengeSelfie",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/ChallengeSelfie.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
