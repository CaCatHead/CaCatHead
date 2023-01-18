export default defineNuxtRouteMiddleware(to => {
  const token = useToken();
  if (token.value) {
    return navigateTo('/');
  } else {
    return true;
  }
});
