export default defineNuxtRouteMiddleware((to, from) => {
  if (!to.query.redirect && to.path !== from.path) {
    to.query.redirect = from.fullPath;
  }
  return true;
});
