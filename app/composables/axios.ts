export const useAxiosFactory = () => {
  const API_BASE = useRuntimeConfig().API_BASE;
  const token = useToken();

  return async () => {
    const { default: axios } = await import('axios');
    return axios.create({
      baseURL: API_BASE,
      headers: {
        Authorization: token.value,
      },
    });
  };
};
