import axios from 'axios';

const post = async (url: string, data: any) => {
  try {
    const env: any = useRuntimeConfig();
    const response = await axios.post(env.public.API_URL + url, data, {
      timeout: env.public.REQUEST_TIMEOUT,
    });
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export { post };
